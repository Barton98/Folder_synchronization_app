import sys
import time
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

def log_action(log_file, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(log_file, 'a') as f:
        f.write(full_message + '\n')

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def folder_sync(source, replica, log_file):
    source = Path(source)
    replica = Path(replica)

    for item in replica.rglob("*"):
        try:
            relative_path = item.relative_to(replica)
            source_item = source / relative_path
            if not source_item.exists():
                if item.is_file():
                    item.unlink()
                    log_action(log_file, f"Removed file: {item}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    log_action(log_file, f"Removed directory: {item}")
        except PermissionError:
            log_action(log_file, f"Permission denied when removing: {item}")

    for item in source.rglob("*"):
        try:
            relative_path = item.relative_to(source)
            replica_item = replica / relative_path
            if item.is_dir():
                if not replica_item.exists():
                    replica_item.mkdir(parents=True)
                    log_action(log_file, f"Created directory: {replica_item}")
            else:
                if not replica_item.exists() or calculate_md5(item) != calculate_md5(replica_item):
                    shutil.copy2(item, replica_item)
                    log_action(log_file, f"Copied/Updated file: {item} -> {replica_item}")
        except PermissionError:
            log_action(log_file, F"Permission denied when writing: {replica_item}")

def main():
    if len(sys.argv) != 6:
        print("Usage: python folder_sync.py <source_folder> <replica_folder> <interval> <sync_count> <log_file>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    try:
        interval = int(sys.argv[3])
        sync_count = int(sys.argv[4])
    except ValueError:
        print("Interval and synchronization_count must be integers.")
        sys.exit(1)
    log_file = sys.argv[5]

    for i in range(sync_count):
        log_action(log_file, f"Starting synchronization {i + 1} of {sync_count}")
        folder_sync(source_folder, replica_folder, log_file)
        if i < sync_count - 1:
            time.sleep(interval)

if __name__ == "__main__":
    main()

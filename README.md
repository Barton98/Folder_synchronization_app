# Folder_synchronization_app
📂 Folder Synchronization Script
This Python script synchronizes the contents of two folders: a source and a replica.
The replica folder will always be kept as an exact copy of the source folder.

🛠 How it works
The user should create a main directory (with the same name as the script file).
Inside this main folder, two subfolders are required:
source/ – where the original files are stored,
replica/ – this folder will mirror the contents of the source.
When the script starts, it automatically creates a log.txt file to log all synchronization actions.

The script:
copies new or updated files from the source to the replica,
deletes files from the replica that no longer exist in the source,
logs every action (file copied, deleted, updated, etc.) to both the console and the log file.

⚙ Command-line usage
python folder_sync.py <source_folder> <replica_folder> <interval_in_seconds> <number_of_syncs> <log_file_path>

Arguments (in order):
Path to the source folder
Path to the replica folder
Interval between synchronizations (in seconds)
Number of synchronizations to perform
Path to the log file (e.g., log.txt)

✅ Example
python folder_sync.py ./source ./replica 10 5 ./log.txt
This will synchronize the folders every 10 seconds, 5 times in total, and log all actions in log.txt.

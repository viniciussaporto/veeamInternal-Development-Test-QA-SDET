# Veeam Internal Development in QA (SDET) Team - Test Task

This is a Python script that helps you synchronize the contents of two folders - a source folder and a replica folder. It continuously monitors the source folder for changes and copies new or modified files to the replica folder, ensuring that both folders remain in sync.

## Features

- Monitors the source folder for changes and synchronizes with the replica folder.
- Copies new files from the source folder to the replica folder.
- Updates modified files in the replica folder based on file size and modification time.
- Removes files and directories from the replica folder that are not present in the source folder.
- Logs synchronization actions to a specified log file and displays them on the console.

## Requirements

- Python 3.x

## Usage

1. Clone this repository or download the source code files.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script files are located.
4. Run the following command to execute the script:

   ```shell
   python sync.py /path/to/source/folder/ /path/to/replica/folder/ interval_in_seconds log_file.txt
   ```
Replace the following placeholders with the appropriate values:

    /path/to/source/folder/: The path to the source folder.
    /path/to/replica/folder/: The path to the replica folder.
    interval_in_seconds: The synchronization interval in seconds (e.g., 5 for syncing every 5 seconds).
	log_file.txt: The path to the log file for storing synchronization actions.

Example:
```
python sync.py /path/to/source /path/to/replica 10 sync_log.txt
```

The script will perform an initial synchronization and then continuously monitor the source folder at the specified interval to keep the replica folder updated.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.


If you have any further questions or need assistance, feel free to ask!
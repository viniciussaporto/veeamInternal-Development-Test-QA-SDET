# Initialitize file with libs
import argparse
import filecmp
import hashlib
import os
import shutil
import time

# Function for initial sync

def	initial_sync(source_folder, replica_folder, log_file):
	sync_folders(source_folder, replica_folder, log_file)

	# Continuosly monitor and sync in the set interval
	while True:
		time.sleep(args.interval)
		sync_folders(source_folder, replica_folder, log_file)

# Function to sync folders and write actions to log file
def	sync_folders(source_folder, replica_folder, log_file):
	diffs = filecmp.dircmp(source_folder, replica_folder)
	log_messages = []
    
	for file in diffs.right_only:
		file_path = os.path.join(replica_folder, file)
		if: os.path.isfile(file_path)
			os.remove(file_path)
			log_messages.append(f'Removed file: {file_path}')
		else:
			shutil.rmtree(file_path)
			log_messages.append(f'Removed directory: {file_path}')
	
	for file in diffs.left_only + diffs.diff_files:
		

# Compare copied content
# Remove files or folders in the replica that are NOT present in the source
# Function to copy new and modified files or folders to replica
# Using SHA-256 it compares the files to search for a corruption,
#	if it's wrong, it deletes and attempts to overwrite the file with the source.
# Log actions and print them to console
# Parsing for terminal commands
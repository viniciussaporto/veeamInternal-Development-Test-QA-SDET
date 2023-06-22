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
		src_file = os.path.join(source_folder, file)
		dst_file = os.path.join(replica_folder, file)
		if os.path.isfile(src_file):
			shutil.copy2(src_file, dst_file)
			log_messages.append(f'Copied file: {src_file} to {dst_file}')

			# Calculate SHA-256
			src_hash = calculate_sha256_hash(src_file)
			dst_hash = calculate_sha256_hash(dst_file)
			if src_hash == dst_hash:
				log_messages.append(f'Hash match for: {dst_file}')
			else:
				log_messages.append(f'Hash mismatch for: {dst_file}')
				# Handle mismatch and retry
				attempts = 0
				while attempts <= 3:
					shutil.copy2(src_file, dst_file)
					log_messages.append(f'Overwrote mismatched file: {dst_file}')
					dst_hash = calculate_sha256_hash(dst_file)
					if src_hash == dst_hash:
						log_messages.append(f'Hash matched after {attempts} attemps for file: {dst_file}')
						break
					attempts += 1
				else:
					log_messages.append(f'Failed to overwrite file after 3 attemps: {dst_file}, try rerunning program')
		else:
			shutil.copytree(src_file, dst_file)
			log_messages.append(f'Copied directory: {src_file} > {dst_file}')
	# Log every action to console and log file
	log_to_file(log_file, log_messages)
	log_to_console(log_messages)

def	calculate_sha256_hash(file_path):
	with open(file_path, 'rb') as file:
		hasher = hashlib.sha256()
		while True:
			data = file.read(8192)
			if not data:
				break
			hasher.update(data)
	return hasher.hexdigest()

def	log_to_file():

def	log_to_console():

# Compare copied content
# Remove files or folders in the replica that are NOT present in the source
# Function to copy new and modified files or folders to replica
# Using SHA-256 it compares the files to search for a corruption,
#	if it's wrong, it deletes and attempts to overwrite the file with the source.
# Log actions and print them to console
# Parsing for terminal commands
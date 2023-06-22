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
	# Function to copy new and modified files or folders to replica
	while True:
		time.sleep(int(args.interval))
		sync_folders(source_folder, replica_folder, log_file)

# Function to sync folders and write actions to log file
def	sync_folders(source_folder, replica_folder, log_file):
	diffs = filecmp.dircmp(source_folder, replica_folder) #os.scandir can be more efficient
	log_messages = []
    
	for file in diffs.right_only:
		file_path = os.path.join(replica_folder, file)
		# Remove files or folders in the replica that are NOT present in the source
		if os.path.isfile(file_path):
			os.remove(file_path)
			log_messages.append(f'Removed file: {file_path}')
		else:
			shutil.rmtree(file_path)
			log_messages.append(f'Removed directory: {file_path}')
	
	for file in diffs.left_only + diffs.diff_files:
		src_file = os.path.join(source_folder, file)
		dst_file = os.path.join(replica_folder, file)
		if os.path.isfile(src_file):
			shutil.copy2(src_file, dst_file) # It's possible to use shutil.copy for files that don't require metadata preservation
			log_messages.append(f'Copied file: {src_file} to {dst_file}')

			# It's possible to avoid unnecessary rehashing of every file, and only do it if 'modified date' or 'size' changes
			# Calculate SHA-256
			src_hash = calc_sha256(src_file)
			dst_hash = calc_sha256(dst_file)
			# Compare copied content
			if src_hash == dst_hash:
				log_messages.append(f'Hash match for: {dst_file}')
			else:
				# Handle mismatch
				log_messages.append(f'Hash mismatch for: {dst_file}')
				attempts = 0
				# Using SHA-256 it compares the files to search for a corruption,
				#	if it's wrong, it attempts to overwrite the file with the source.
				while attempts <= 3:
					shutil.copy2(src_file, dst_file)
					log_messages.append(f'Overwrote mismatched file: {dst_file}')
					dst_hash = calc_sha256(dst_file)
					if src_hash == dst_hash:
						log_messages.append(f'Hash matched after {attempts} attemps for file: {dst_file}')
						break
					attempts += 1
				else:
					log_messages.append(f'Failed to overwrite file after 3 attemps: {dst_file}, try rerunning program')
		else:
			shutil.copytree(src_file, dst_file)
			log_messages.append(f'Copied directory: {src_file} > {dst_file}')
	# Log actions and print them to console and log file
	log_to_file(log_file, log_messages)
	log_to_console(log_messages)

def	calc_sha256(file_path):
	with open(file_path, 'rb') as file:
		hasher = hashlib.sha256()
		while True:
			data = file.read(8192)
			if not data:
				break
			hasher.update(data)
	return hasher.hexdigest()

def	log_to_file(log_file, messages):
	with open(log_file, 'a') as file:
		for message in messages:
			file.write(message + '\n')

def	log_to_console(messages):
	for message in messages:
		print(message)

if __name__ == '__main__':
	# Parsing for terminal commands
	parser = argparse.ArgumentParser('Folder Sync Program')
	parser.add_argument('source', help='Path to source folder')
	parser.add_argument('replica', help='Path to replica folder')
	parser.add_argument('interval', help='Sync interval in seconds')
	parser.add_argument('log_file', help='Path to log file')
	args = parser.parse_args()

	#Running
	initial_sync(args.source, args.replica, args.log_file)
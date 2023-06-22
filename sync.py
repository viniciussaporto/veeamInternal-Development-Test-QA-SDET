# Initialitize file with libs
import argparse
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
def sync_folders(source_folder, replica_folder, log_file):
    log_messages = []

    # Compare directories using os.scandir() for better performance
    src_files = {entry.name: entry for entry in os.scandir(source_folder)}
    dst_files = {entry.name: entry for entry in os.scandir(replica_folder)}

    # Remove files/folders in replica that are not in source
    for file_name, dst_entry in dst_files.items():
        dst_path = os.path.join(replica_folder, file_name)
        if file_name not in src_files:
            if dst_entry.is_file():
                os.remove(dst_path)
                log_messages.append(f'Removed file: {dst_path}')
            else:
                shutil.rmtree(dst_path)
                log_messages.append(f'Removed directory: {dst_path}')

    # Copy new or modified files/folders from source to replica
    for file_name, src_entry in src_files.items():
        src_path = os.path.join(source_folder, file_name)
        dst_path = os.path.join(replica_folder, file_name)

        if file_name not in dst_files:
            if src_entry.is_file():
                shutil.copy2(src_path, dst_path)
                log_messages.append(f'Copied file: {src_path} -> {dst_path}')
            else:
                shutil.copytree(src_path, dst_path)
                log_messages.append(f'Copied directory: {src_path} -> {dst_path}')
        else:
            dst_entry = dst_files[file_name]

            if src_entry.is_file() and dst_entry.is_file():
                # Compare file size and modification time for synchronization
                if src_entry.stat().st_size != dst_entry.stat().st_size or \
                   src_entry.stat().st_mtime > dst_entry.stat().st_mtime:
                    src_hash = calc_sha256(src_path)
                    dst_hash = calc_sha256(dst_path)

                    if src_hash != dst_hash:
                        shutil.copy2(src_path, dst_path)
                        log_messages.append(f'Updated file: {src_path} -> {dst_path}')

    # Log the synchronization operations to both console and log file
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
			file.flush() # In case of program crashing, it writes the logs instantly

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
# Initialitize file with libs
# Function for initial sync
# Function to continuosly monitor and sync in the set interval
# Function to sync folders and write actions to log file
# Compare copied content
# Remove files or folders in the replica that are NOT present in the source
# Function to copy new and modified files or folders to replica
# Using SHA-256 it compares the files to search for a corruption,
#	if it's wrong, it deletes and attempts to overwrite the file with the source.
# Log actions and print them to console
# Parsing for terminal commands
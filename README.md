# Simple Backup Script For Phyton

It is a quite simple, but effective, backup script for python3.

Just run:
```console
python3 backup.py source destination
```
where `source` is the folder to backup and `destination` the folder to backup into.

The scripts create a folder, with today's name, in the destination folder and backups all files from source in it. 

At the end, if requested, it checks whatever there are any duplicates files in the `destination` folder and removes them, to free space, while leaving the most recent files undeleted. But it will show you first the files and then will ask you for confirmation before deletion. 

It also asks you whatever you want to remove all empty folders in `destination`.

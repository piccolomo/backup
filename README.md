# backup

It is a quite simple, but effective, backup script for python3.

Just run:
```python
python3 backup.py source destination
```
where `source` is the folder to backup and `destination` the folder to backup into.

The scripts create a folder, with today's name, in the destination folder and backups all files from source in it. 

At the end it check whatever there are any duplicates files in `destination` and removes them, to free space, if requested.



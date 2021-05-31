# sfsfsf

### simple fast file sharing sans frustration.

`sfsfsf` is a simple file sharing service to synchronize directories across servers.

### Requirements

- linux
- rsync (included with most linux distributions)
- python requirements (inotify)

### Usage

`python main.py` will create a `sandbox` directory with four directories
that represent servers. Copy, move, and edit files in one directory, and the 
changes will be instantly synchronized across all directories.
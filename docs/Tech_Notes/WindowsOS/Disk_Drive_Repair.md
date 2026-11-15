# Sometimes CHKDSK can fix minor corruption without formatting:
	chkdsk X: /f /r /x

	- Replace X: with your USB drive letter.
	- /f fixes file system errors.
	- /r locates bad sectors and recovers readable data.
	- /x forces dismount before scanning.


# Use DiskPart to clean and rebuild the partition:
	diskpart
	list disk
	select disk X 			← Replace X with your USB disk number	
	clean
	create partition primary
	format fs=ntfs quick 
	assign
	exit
	
	- UDF = Universal Disk Format.  Used for optical media(DVDs, Blu-ray)
	- ReFS = Resilient File System.  Designed for data integrity and large-scale storage. 	Available on Windows Server and some Pro editions. 
	
# Format a Disk to exFAT Using DiskPart
	list disk
	select disk X           ← Replace X with your USB disk number
	list partition
	select partition Y       ← Replace Y with the partition number (or create one if needed)
	format fs=exfat label="BackupDrive" quick
	assign
	exit

# DiskPart format parameters
	- fs= → File system type (ntfs, fat, fat32, exfat, udf, refs)
	- label= → Volume label (optional)
	- unit= → Allocation unit size in bytes (e.g., 512, 1024, 2048, 4096, 8192, 64K)
	- quick → Performs a quick format (optional)
	- compress → Enables NTFS compression (optional, NTFS only)
	- override → Forces format even if volume is in use (use with caution)



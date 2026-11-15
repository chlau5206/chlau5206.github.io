When you clone a hard drive sector-by-sector, the cloned disk inherits an exact duplicate of the original disk's **Disk Signature** (on MBR disks) or **Disk GUID** (on GPT disks). Because Windows requires unique identifiers for every attached storage device to prevent data corruption and drive conflicts, it will automatically "offline" or hide the duplicate disk if both are connected to the same system at the same time.

To make the cloned disk visible and accessible alongside the original, you need to change its disk signature/ID using Windows built-in disk management tools.

### Method 1: Using PowerShell (Recommended)

You can view and update the disk signature quickly using PowerShell running with Administrator privileges.

**1.Open PowerShell as Administrator:**Prerequisite.

Press the **Windows Key**, type `powershell`, right-click **Windows PowerShell** or **Terminal**, and select **Run as administrator**.

_Verification:_ The title bar of the window displays "Administrator: Windows PowerShell".

**2.Identify the Disk Number:**2 min.

Run the following command to list your connected drives and find the disk number of your cloned drive:

PowerShell

```
Get-Disk | Select-Object Number, FriendlyName, OperationalStatus, TotalSize
```

_Verification:_ Note the **Number** associated with your cloned disk (e.g., Disk 1 or Disk 2). Make sure you do not confuse it with your active source/system disk.

**3.Initialize the Signature Change:**1 min.

To assign a new unique ID (signature/GUID) to the cloned disk, run the following command (replace `[DiskNumber]` with your actual disk number, such as `1`):

PowerShell

```
Set-Disk -Number [DiskNumber] -UniqueId
```

_Verification:_ PowerShell completes without throwing an error, indicating a new unique signature has been generated and written to the disk.

**4.Bring the Disk Online:**1 min.

If the disk is currently marked as offline or hidden, bring it online by running:

PowerShell

```
Set-Disk -Number [DiskNumber] -IsOffline $false
```

_Verification:_ Open **Disk Management** (`diskmgmt.msc`) and confirm that the disk status changes from "Offline" to "Online".

### Method 2: Using DiskPart (Alternative Command Line)

If you prefer using the classic DiskPart utility, you can change the disk signature manually.

**1.Open Command Prompt as Administrator:**Prerequisite.

Press **Win + R**, type `cmd`, and press **Ctrl + Shift + Enter** to open an elevated Command Prompt.

_Verification:_ Window header reads "Administrator: Command Prompt".

**2.Launch DiskPart and Select the Cloned Disk:**2 min.

Type `diskpart` and press Enter. Then list your disks and select the clone:

Plaintext

```
list disk
select disk X
```

_(Replace `X` with the correct disk number of your clone)._

_Verification:_ DiskPart responds with `Disk X is now the selected disk.`

**3.Change the Disk ID/Signature:**1 min.

Depending on whether your disk uses MBR or GPT partitioning, enter the appropriate command:

- **For MBR disks:**
    

Plaintext

```
uniqueid disk id=<New8HexCharacters>
```

_(Example: `uniqueid disk id=12345678`)_

- **For GPT disks:**
    

Plaintext

```
uniqueid disk ID={12345678-1234-1234-1234-123456789abc}
```

_Verification:_ DiskPart confirms that the disk identifier has been successfully changed.

# Important Safety Note
If you cloned your boot drive and plan to boot directly from the new cloned disk, it is usually best to **shut down the PC, physically disconnect the old source drive, and boot with only the cloned drive attached** first. This avoids Windows confusion over duplicate partition signatures during the initial boot sequence.


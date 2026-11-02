powershell

```
# Set the target folder path
$folderPath = "C:\Your\Folder\Path"

# Get all files in the folder and rename them to uppercase
Get-ChildItem -Path $folderPath -File | ForEach-Object {
    $newName = $_.BaseName.ToUpper() + $_.Extension
    Rename-Item -Path $_.FullName -NewName $newName
}
```
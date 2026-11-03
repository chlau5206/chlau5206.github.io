---
title: Capitalize All File Names In A Folder

category: Tech_Notes

tags:
  - Tech_Notes
  - Deveplement

status: completed

created: 2026-10-29
updated: 2026-11-02
---

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
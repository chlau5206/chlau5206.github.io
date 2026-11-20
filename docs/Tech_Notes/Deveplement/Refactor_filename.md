---
title: Refactor Filename
category: Tech_Notes
tags:
  - Tech_Notes
  - Deveplement
status: in progress
created: 2026-11-15
updated: 2026-11-15
---
### Refined Transformation & Sanitization Block Example

Here is how you can polish that section to ensure perfect execution order and clean separation of base vs. extension:

PowerShell

```
    # --- Initial base/ext & Trim ---
    $base = [System.IO.Path]::GetFileNameWithoutExtension($oldName).Trim()
    $ext  = [System.IO.Path]::GetExtension($oldName)
    $newName = $base + $ext

    # --- 1. Remove Prefix (Best done at the start) ---
    if ($RemovePrefix -ne "") {
        if ($base.StartsWith($RemovePrefix)) {
            $base = $base.Substring($RemovePrefix.Length)
            $newName = $base + $ext
        }
    }

    # --- 2. Regex rename ---
    if ($Pattern -ne "") {
        try {
            $newName = [regex]::Replace($newName, $Pattern, $Replacement)
            $base = [System.IO.Path]::GetFileNameWithoutExtension($newName)
            $ext  = [System.IO.Path]::GetExtension($newName)
        }
        catch {
            $SkippedCount++
            return
        }
    }
    
    # --- 3. Remove suffix ---
    if ($RemoveSuffix -ne "") {
        if ($base.EndsWith($RemoveSuffix)) {
            $base = $base.Substring(0, $base.Length - $RemoveSuffix.Length)
            $newName = $base + $ext
            $base = [System.IO.Path]::GetFileNameWithoutExtension($newName)
            $ext  = [System.IO.Path]::GetExtension($newName)
        }
    }

    # --- 4. Add suffix ---
    if ($AddSuffix -ne "") {
        $newName = $base + $AddSuffix + $ext
        $base = [System.IO.Path]::GetFileNameWithoutExtension($newName)
        $ext  = [System.IO.Path]::GetExtension($newName)
    }

    # --- 5. Change extension ---
    if ($NewExtension -ne "") {
        if ($NewExtension.StartsWith(".")) {
            $newName = $base + $NewExtension
        } else {
            $newName = $base + "." + $NewExtension
        }
        $base = [System.IO.Path]::GetFileNameWithoutExtension($newName)
        $ext  = [System.IO.Path]::GetExtension($newName)
    }

    # --- 6. Add Prefix ---
    if ($Prefix -ne "") {
        $newName = $Prefix + $newName
        # Recompute base/ext if needed for final sanitization bounds
        $base = [System.IO.Path]::GetFileNameWithoutExtension($newName)
        $ext  = [System.IO.Path]::GetExtension($newName)
    }

    # Skip if unchanged
    if ($newName -eq $oldName) {
        $SkippedCount++
        return
    }

    # --- Unicode & Character Sanitization ---
    # Sanitize invalid filename characters across the whole name
    foreach ($char in $InvalidChars) {
        $newName = $newName.Replace($char, '_')
    }

    # Target space replacement specifically on the base name or handle safely
    # Re-extract base/ext post-transformations
    $base = [System.IO.Path]::GetFileNameWithoutExtension($newName).Trim()
    $ext  = [System.IO.Path]::GetExtension($newName)

    # Replace spaces with underscores and collapse multiple underscores on the base name
    $base = $base -replace '\s+', '_'
    $base = $base -replace '_+', '_'
    
    $newName = $base + $ext
```

### Summary of Strengths in Your Current Build:

- **Robust Logging & Debugging:** Using the `-DEBUG` switch alongside timestamped logging handles feedback visibility perfectly.
    
- **Safety First:** The collision check (`Test-Path $newPath`) and final invalid character sanity check prevent accidental data overwrites or file corruption.
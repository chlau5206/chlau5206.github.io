This block of text is known as **Comment-Based Help** (or a **Help Documentation Block**) in PowerShell. It allows scripts and functions to have built-in documentation that users can access directly in the console using commands like `Get-Help .\MediaMaster.ps1`.

```
<#  MediaMaster.ps1
    --------------------------------
.SYNOPSIS
    Semi-automatic controller for Merge, Split, and Encode operations.

.DESCRIPTION
    MediaMaster.ps1 orchestrates the full media pipeline:
        Merge --> Split --> Encode

.PARAMETER StartFolder
    The working directory for all operations. Default is current directory.

.PARAMETER Mode
    One or more pipeline stages: Merge, Split, Encode. Default: all three.
 
.PARAMETER SegmentLength
    Segment duration in seconds for splitting (default: 3000).
  
.PARAMETER TimestampFile
    Optional text file containing timestamps for splitting.
  
.PARAMETER Type
    Video filter preset for EncodeMedia ("anime", "ai-anime", "hybrid", "live"). Default: ai-anime.
 
.PARAMETER MaxParallel
    Maximum number of parallel encoding jobs (default: 2).
 
.PARAMETER DebugMode
    Enable verbose debugging output.
#>
```
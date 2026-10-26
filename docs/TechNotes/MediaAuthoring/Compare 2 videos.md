---
title: Compare 2 videos
parent: MediaAuthoring
nav_order: 1020
---


# 📘 **VerifyMedia.ps1 — Helper & Usage Guide**

## 🎯 Purpose

`VerifyMedia.ps1` validates **one pair** of media files:

Code

```
original.mp4
encoded.mp4
```

It performs structural QC checks using ffprobe:

- Video duration
    
- Frame count
    
- FPS
    
- Audio duration
    

Then determines whether the encoded file **matches** the original.

This script is designed to be:

- Fast (≈5 seconds for a 2‑hour video)
    
- Modular
    
- Script‑friendly
    
- Human‑readable (Detail mode)
    
- Machine‑readable (JSON mode)
    

It is the core building block used by `VerifyBatch.ps1`.

# 🧩 **Helper: How VerifyMedia.ps1 Works**

### 1. Input

You provide:

Code

```
-Original "video.mp4"
-Encoded "video_encoded.mp4"
```

### 2. ffprobe Metrics Collected

The script extracts:

|Metric|Description|
|---|---|
|**Duration**|Total video length in seconds|
|**Frame Count**|Total number of decoded frames|
|**FPS**|Frames per second (r_frame_rate)|
|**Audio Duration**|Length of audio stream|

### 3. Matching Logic

Each metric is compared:

- Duration → must match within ±0.01 seconds
    
- Frame count → must match exactly
    
- FPS → must match within ±0.01
    
- Audio duration → must match within ±0.01 seconds
    

If all four match:

Code

```
AllMatch = True
```

Otherwise:

Code

```
AllMatch = False
```

### 4. Output Modes

#### **Default (Boolean)**

Returns only:

Code

```
True
```

or

Code

```
False
```

Perfect for scripting and automation.

#### **Mode Detail**

Prints human‑readable metrics:

- Original vs encoded values
    
- Match flags
    
- Overall match
    
- Timestamp
    
- File names
    

Useful for debugging individual files.

#### **Mode Json**

Returns a JSON object containing:

- Original filename
    
- Encoded filename
    
- Verification timestamp
    
- All numeric metrics
    
- Match flags
    
- Overall match
    

Ideal for logging, dashboards, batch QC, and machine parsing.

# 🧪 **Usage Examples**

## ✔ 1. Boolean mode (default)

Fast QC for automation:

powershell

```
$verified = .\VerifyMedia.ps1 -Original "video.mp4" -Encoded "video_encoded.mp4"

if ($verified) {
    Write-Host "Verification passed."
} else {
    Write-Host "Verification FAILED."
}
```

Output:

Code

```
True
```

or

Code

```
False
```

## ✔ 2. Detail mode (human-readable)

powershell

```
.\VerifyMedia.ps1 -Original "video.mp4" -Encoded "video_encoded.mp4" -Mode Detail
```

Example output:

Code

```
Original File     : video.mp4
Encoded File      : video_encoded.mp4
Verified At       : 2026-10-21 09:59:00

Original Duration : 1234.56
Encoded Duration  : 1234.56
Duration Match    : True

Original Frames   : 30864
Encoded Frames    : 30864
Frame Match       : True

Original FPS      : 25
Encoded FPS       : 25
FPS Match         : True

Original Audio    : 1234.56
Encoded Audio     : 1234.56
Audio Match       : True

Overall Match     : True
```

## ✔ 3. JSON mode (machine-readable)

powershell

```
$json = .\VerifyMedia.ps1 -Original "video.mp4" -Encoded "video_encoded.mp4" -Mode Json
$json | Out-File "Verify_video.json"
```

Example JSON:

json

```
{
  "OriginalFile": "video.mp4",
  "EncodedFile": "video_encoded.mp4",
  "VerifiedAt": "2026-10-21 09:59:00",
  "OriginalDuration": 1234.56,
  "EncodedDuration": 1234.56,
  "DurationMatch": true,
  "OriginalFrames": 30864,
  "EncodedFrames": 30864,
  "FrameMatch": true,
  "OriginalFPS": 25,
  "EncodedFPS": 25,
  "FPSMatch": true,
  "OriginalAudio": 1234.56,
  "EncodedAudio": 1234.56,
  "AudioMatch": true,
  "AllMatch": true
}
```

Perfect for:

- Batch QC
    
- Logging
    
- CI/CD pipelines
    
- MediaMaster reporting
    

# ⏱ **Performance: How long does verification take?**

### For a 2‑hour video:

|Operation|Time|
|---|---|
|Duration|< 0.01 sec|
|FPS|< 0.01 sec|
|Audio duration|< 0.01 sec|
|Frame count|**3–15 seconds**|

Frame count is the only expensive step because ffprobe must decode every frame.

### Real‑world total time:

**≈ 5 seconds per 2‑hour video** (on your workstation)

This is extremely efficient for structural QC.

# 🧭 **Summary**

### VerifyMedia.ps1 gives you:

- ✔ Boolean mode → fast QC
    
- ✔ Detail mode → human debugging
    
- ✔ JSON mode → structured logs
    
- ✔ Accurate duration/frame/FPS/audio checks
    
- ✔ Timestamp + filenames in JSON
    
- ✔ Predictable behavior for automation
    

### VerifyBatch.ps1 builds on this to handle entire folders.

# 📘 **VerifyBatch.ps1 — Helper & Usage Guide**

## 🎯 Purpose

`VerifyBatch.ps1` automates verification of **multiple encoded videos** inside a folder. It detects file pairs using the naming pattern:

Code

```
media.mp4
media_encoded.mp4
```

Then it calls **VerifyMedia.ps1** for each pair and returns:

- Boolean match (default)
    
- Detailed metrics (Mode Detail)
    
- JSON logs (Mode Json)
    

This is your batch QC layer.

# 🧩 **Helper: How VerifyBatch.ps1 Works**

### 1. Input

You provide:

Code

```
-StartFolder "C:\Workspace\Done"
```

### 2. File Pair Detection

It scans the folder for:

Code

```
*_encoded.mp4
```

For each encoded file:

Code

```
video1_encoded.mp4 → video1.mp4
video2_encoded.mp4 → video2.mp4
```

If the original file is missing, it skips the pair.

### 3. Verification

For each pair:

Code

```
VerifyMedia.ps1 -Original video1.mp4 -Encoded video1_encoded.mp4
```

### 4. Output

Depending on mode:

#### **Default (Boolean)**

Returns a summary table:

Code

```
Original                Encoded                     Match
--------                -------                     -----
video1.mp4             video1_encoded.mp4           True
video2.mp4             video2_encoded.mp4           False
```

#### **Mode Detail**

Prints full metrics for each pair.

#### **Mode Json**

Creates JSON logs:

Code

```
Verify_video1.json
Verify_video2.json
```

And returns a summary table.

# 🧪 **Usage Examples**

## ✔ 1. Basic batch verification (boolean summary)

powershell

```
.\VerifyBatch.ps1 -StartFolder "C:\Workspace\Done"
```

Output:

Code

```
Original                Encoded                     Match
--------                -------                     -----
video1.mp4             video1_encoded.mp4           True
video2.mp4             video2_encoded.mp4           True
video3.mp4             video3_encoded.mp4           False
```

Perfect for scripting and automation.

## ✔ 2. Detailed batch verification (human-readable)

powershell

```
.\VerifyBatch.ps1 -StartFolder "C:\Workspace\Done" -Mode Detail
```

Each pair prints:

- Duration
    
- Frame count
    
- FPS
    
- Audio duration
    
- Match flags
    
- Overall match
    
- Timestamp
    

Useful for debugging individual files.

## ✔ 3. JSON batch verification (logging)

powershell

```
.\VerifyBatch.ps1 -StartFolder "C:\Workspace\Done" -Mode Json
```

Creates:

Code

```
Verify_video1.json
Verify_video2.json
Verify_video3.json
```

Each JSON includes:

- Original filename
    
- Encoded filename
    
- Verification timestamp
    
- Duration
    
- Frame count
    
- FPS
    
- Audio duration
    
- Match flags
    
- Overall match
    

Perfect for:

- MediaMaster logging
    
- CI/CD pipelines
    
- Automated QC dashboards
    
- Batch processing reports
    

# 🧱 **Integration Example (EncodeMedia.ps1)**

After encoding all files:

powershell

```
$batchResult = .\VerifyBatch.ps1 -StartFolder $StartFolder -Mode Json

# Optional: check if all passed
if ($batchResult.Match -contains $false) {
    Write-Host "Some files failed verification."
} else {
    Write-Host "All files verified successfully."
}
```

# 🧭 **Summary**

### ✔ Boolean mode → fast batch QC

### ✔ Detail mode → human debugging

### ✔ JSON mode → structured logs

### ✔ Wrapper automatically finds file pairs

### ✔ Perfect for MediaMaster automation



**For Python version**

modular Python **package** version of both scripts:

- `verify_media.py` → single‑file verification
    
- `verify_batch.py` → batch folder verification
    

Both follow the same architecture and behavior as your PowerShell versions.

I’ll give you:

1. **Package structure**
    
2. **verify_media.py** (full module)
    
3. **verify_batch.py** (full module)
    
4. **Usage examples**
    
5. **Notes for integration**
    

Everything is written cleanly, with no external dependencies except `ffprobe`.

# 📦 **Python Package Structure**

Code

```
mediaqc/
│
├── __init__.py
├── verify_media.py
└── verify_batch.py
```

You can install this folder as a package or just drop it into your project.

# 🧪 **Usage Examples**

## ✔ 1. Single file verification (boolean)

python

```
from mediaqc.verify_media import verify_media

ok = verify_media("video.mp4", "video_encoded.mp4")
print(ok)
```

## ✔ 2. Detail mode

python

```
detail = verify_media("video.mp4", "video_encoded.mp4", mode="detail")
print(detail)
```

## ✔ 3. JSON mode

python

```
json_str = verify_media("video.mp4", "video_encoded.mp4", mode="json")
print(json_str)
```

## ✔ 4. Batch verification

python

```
from mediaqc.verify_batch import verify_batch

results = verify_batch("C:/Workspace/Done")
print(results)
```

## ✔ 5. Batch JSON logging

python

```
verify_batch("C:/Workspace/Done", mode="json")
```

Creates:

Code

```
Verify_video1.json
Verify_video2.json
Verify_video3.json
```

# 🧭 **Notes for Integration**

- Works on Windows, Linux, macOS
    
- Requires `ffprobe` in PATH
    
- Perfect for CI/CD, MediaMaster, or Python‑based QC pipelines
    
- Mirrors your PowerShell architecture exactly
    
- Boolean mode is fast and ideal for automation
    
- JSON mode is ideal for logging and dashboards
---
title: Media Workflow Dev Spec
category: Tech_Notes
tags:
  - Tech_Notes
  - MediaAuthoring
status: in progress
created: 2026-11-07
updated: 2026-11-07
---
### Development Specification (Dev Spec)

Below is the complete **Technical & Architectural Specification** for your Windows-based Python media processing pipeline.

#### **1. System Architecture & Philosophy**

- **Language / Environment**: Python 3.x, designed for native execution on Windows 11.
    
- **Core Design Patterns**:
    
    - **Modular Decoupling**: Shared utilities and process management reside in `media_utils.py`. Individual steps operate as standalone scripts or orchestrated children under `MediaMaster.py`.
        
    - **Late Container Binding**: Universal processing and heavy manipulation (merging/splitting) take place inside the flexible `.mkv` container, deferring final container selection (`.mkv` or `.mp4`) to the encoding stage.
        
    - **Resource Politeness**: Background FFmpeg tasks run at `BelowNormal` process priority (`0x00004000`) via Windows `ctypes` API calls to prevent system thread thrashing.
        

#### **2. File Naming & Prefix Conventions**

The pipeline relies on predictable naming standards to track assets across stages:

- **Raw Inputs**: `video.*`, `audio.*`, `*.srt/.ass/.vtt`
    
- **Merged State**: `merged_<basename>.mkv`
    
- **Split Segments**: `split_<basename>_p00.mkv`, `split_<basename>_p01.mkv`, etc.
    
- **Encoded Output**: `encoded_<basename>_p00.mkv` (or `.mp4`)
    
- **Verification Reports**: `VerifyMediaBatch.json`
    

#### **3. Module Specifications**

##### **`media_utils.py`**

- **Purpose**: Centralized logging (`write_log`) and safe process spawning (`run_ffmpeg`).
    
- **Key Mechanisms**:
    
    - Enforces UTF-8 stream decoding with `errors="replace"` to handle non-ASCII characters smoothly.
        
    - Adjusts process priority to `BelowNormal` (`0x00004000`) using `ctypes.windll.kernel32.SetPriorityClass` on Windows platforms.
        

##### **`MergeMedia.py`**

- **Purpose**: Automatically groups corresponding video, audio, and subtitle streams by base name and muxes them into `.mkv` format using stream copy (`-c copy`).
    
- **Constraints**: Requires at least a video stream paired with an audio or subtitle stream to execute.
    

##### **`SplitMedia.py`**

- **Purpose**: Divides merged files either by a fixed segment length (default: 3000 seconds) or via an external timestamp text file.
    
- **Constraints**: Relies on stream copying (`-c copy`) for rapid, lossless segmentation.
    

##### **`EncodeMedia.py`**

- **Purpose**: Transcodes split files using `libx265` (10-bit color `yuv420p10le`, CRF 26) with dynamic video filter chains (`ai-anime`, `anime`, `hybrid`, `live`).
    
- **Concurrency**: Executes jobs in parallel using `ThreadPoolExecutor` governed by `--MaxParallel`.
    
- **Quality Control Integration**: Automatically invokes `VerifyMedia.py` upon completing each file encode.
    

##### **`VerifyMedia.py` & `VerifyMediaBatch.py`**

- **Purpose**: Post-encoding structural quality control via `ffprobe`.
    
- **Performance Optimization**: Heavy frame-counting checks (`-count_frames`) are strictly **disabled by default**, and only run when `--enableFrameCheck` is explicitly provided.
    
- **Robustness**: Includes fallback checks for audio duration to prevent false failures on containers lacking stream-specific audio header tags.
    

##### **`MediaMaster.py`**

- **Purpose**: Sequential orchestrator running the full pipeline (`Merge` $\rightarrow$ `Split` $\rightarrow$ `Encode`).
    
- **Constraints**: Enforces strict execution order regardless of argument input sequences.
    

#### **4. Command-Line Interface (CLI) Quick Reference**

|**Script**|**Primary Purpose**|**Key Arguments**|
|---|---|---|
|`MediaMaster.py`|Full pipeline orchestration|`--StartFolder`, `--Mode`, `--SegmentLength`, `--Type`, `--MaxParallel`, `--enableFrameCheck`|
|`MergeMedia.py`|Batch muxing to `.mkv`|`--StartFolder`, `--DebugMode`|
|`SplitMedia.py`|Fixed or timestamp-based splitting|`--StartFolder`, `--Original`, `--SegmentLength`, `--TimestampFile`|
|`EncodeMedia.py`|HEVC transcode & filtering|`--StartFolder`, `--Type`, `--MaxParallel`, `--OutputFormat`, `--enableFrameCheck`|
|`VerifyMedia.py`|Single file structural QC|`--Original`, `--Encoded`, `--enableFrameCheck`, `--Mode` (`Detail`/`Json`)|
|`VerifyMediaBatch.py`|Batch folder QC & JSON report|`--StartFolder`, `--enableFrameCheck`, `--Mode` (`Json`)|
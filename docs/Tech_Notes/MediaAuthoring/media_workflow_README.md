---
title: Media Workflow Readme
category: Tech_Notes
tags:
  - Tech_Notes
  - MediaAuthoring
status: in progress
created: 2026-11-07
updated: 2026-11-07
---
# Media Processing Workflow Toolset

This document details the complete Python-based media processing pipeline refactored for high performance, Windows priority management, non-ASCII metadata resilience, and automated verification.

---

## 1. `media_utils.py`

* **Purpose**: Serves as the core utility module shared across all scripts. It standardizes log formatting, guarantees UTF-8 safe execution of subprocesses (preventing non-ASCII encoding crashes), and manages Windows process priority.
* **Usage**: Imported as a library module by other Python scripts (`from media_utils import write_log, run_ffmpeg`).
* **Constraints**:
  * Must reside in the same directory as the executing scripts.
  * Operating System: Windows (`ctypes.windll.kernel32` used for `BelowNormal` process priority; falls back to `os.nice` on UNIX).
  * Requires `ffmpeg` and `ffprobe` to be accessible in the system's `PATH`.

---

## 2. `MergeMedia.py`

* **Purpose**: Scans a directory for matching media components (video, audio, subtitles) grouped by base filename and stream-copies them into unified `.mkv` container files.
* **Usage**:
  ```bash
  python MergeMedia.py --StartFolder "D:\MediaFolder" [--DebugMode]
  ```
* **Constraints**:
  * Automatically ignores files starting with `merged_`, `MergeMedia_`, or `SplitMedia_`.
  * Preserves original stream codecs using `-c copy`.
  * Subtitle files (`.srt`, `.ass`, `.vtt`) should be encoded in UTF-8 to prevent container-level character mapping issues.
  * Output files follow the naming convention `merged_<basename>.mkv`.

---

## 3. `SplitMedia.py`

* **Purpose**: Batch splits media files into smaller segments using either fixed-length durations or exact timestamp sequences.
* **Usage**:
  * **Fixed-length mode**:
    ```bash
    python SplitMedia.py --StartFolder "D:\MediaFolder" --SegmentLength 3000
    ```
  * **Timestamp-based mode**:
    ```bash
    python SplitMedia.py --StartFolder "D:\MediaFolder" --TimestampFile "timestamps.txt"
    ```
* **Constraints**:
  * Automatically target-matches files prefixed with `merged_` when `--Original` is not explicitly declared.
  * Stream-copies video without re-encoding (`-c copy`).
  * Output segment pattern follows `split_<basename>_p00.mkv`.
  * Timestamp files must contain at least two valid timestamp lines (`HH:MM:SS` or seconds).

---

## 4. `EncodeMedia.py`

* **Purpose**: Encodes video segments using `libx265` (10-bit color depth) and configurable video filtering presets (`ai-anime`, `anime`, `hybrid`, `live`) with parallel processing support.
* **Usage**:
  ```bash
  python EncodeMedia.py --StartFolder "D:\MediaFolder" --Type ai-anime --MaxParallel 2 --OutputFormat mkv [--enableFrameCheck] [--DebugMode]
  ```
* **Constraints**:
  * Automatically scans for target input files starting with `split_`.
  * Outputs files with the prefix `encoded_<basename>.<format>`.
  * Requires sufficient CPU/GPU capacity depending on the `--MaxParallel` threshold.
  * Automatically triggers `VerifyMedia.py` post-encoding for quality assurance.

---

## 5. `VerifyMedia.py`

* **Purpose**: Performs structural quality control checks on a pair of media files (original vs. encoded) by inspecting stream metadata via `ffprobe`. Validates video duration, frame rate (FPS), audio duration, and frame counts.
* **Usage**:
  ```bash
  python VerifyMedia.py --Original "split_file_p00.mkv" --Encoded "encoded_file_p00.mkv" [--enableFrameCheck] [--Mode Detail|Json]
  ```
* **Constraints**:
  * Frame count verification (`--enableFrameCheck`) requires reading all video frames with `ffprobe` (`-count_frames`) and is disabled by default for optimal performance.
  * Falls back to global container format duration if individual stream duration headers are missing or evaluate to 0.

---

## 6. `VerifyMediaBatch.py`

* **Purpose**: Discovers all `encoded_*` files within a directory, pairs them with their corresponding `split_*` source files, runs validation checks, and compiles summary reports or aggregated JSON logs.
* **Usage**:
  ```bash
  python VerifyMediaBatch.py --StartFolder "D:\MediaFolder" [--enableFrameCheck] [--Mode Json]
  ```
* **Constraints**:
  * Expects file naming alignment (`encoded_<name>` matching back to `split_<name>`).
  * Generates `VerifyMediaBatch.json` in the target directory when run in `Json` mode.

---

## 7. `MediaMaster.py`

* **Purpose**: Pipeline controller that orchestrates the entire workflow (`Merge` $\rightarrow$ `Split` $\rightarrow$ `Encode`) in strict sequence while validating component presence before each stage.
* **Usage**:
  ```bash
  python MediaMaster.py --StartFolder "D:\MediaFolder" --Mode Merge Split Encode --Type ai-anime --MaxParallel 2
  ```
* **Constraints**:
  * Enforces fixed execution ordering regardless of input parameter sequence.
  * Skips stages dynamically if required prerequisites (`video.*/audio.*`, `merged_*`, `split_*`) are absent from `--StartFolder`.
  * Calls sub-scripts as standalone Python subprocesses within the working runtime environment.

---
### Overview of Generated Metadata:

- **`media_utils.py`**: Details UTF-8 stream decoding, process priority management (`0x00004000` for `BelowNormal`), and shared logger mechanics.
    
- **`MergeMedia.py` / `SplitMedia.py` / `EncodeMedia.py`**: Covers dynamic parameters, file discovery rules, input/output prefixes (`merged_`, `split_`, `encoded_`), and encoding specifications.
    
- **`VerifyMedia.py` / `VerifyMediaBatch.py`**: Summarizes performance considerations (bypassing `-count_frames` by default), fallback audio metadata checks, and JSON output structures.
    
- **`MediaMaster.py`**: Explains stage validation and pipeline automation logic.

---


**If you just want to change containers (e.g., `.mkv` to `.mp4`) instantly **without quality loss or re-encoding**. For a quick, lossless container switch, a simple one-line FFmpeg copy command is much faster:
	ffmpeg -i input.mkv -c copy output.mp4
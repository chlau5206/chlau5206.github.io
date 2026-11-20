### FFmpeg (no re-encoding, fastest)
If both videos have the same:
- Codec (H.264, HEVC, etc.)
- Resolution
- FPS
- Audio format

Use FFmpeg's **concat demuxer**:
Create `filelist.txt`

``` Plain Text
file 'video1.mp4'
file 'video2.mp4'
```
Then:

```  Shell
ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4
```

Advantages:
- Very fast
- No quality loss
- No re-encoding
- Ideal for your MediaMaster workflow

---
If Videos don't match
```  Shell
ffmpeg \
-i video1.mp4 \
-i video2.mp4 \
-filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
-map "[v]" \
-map "[a]" \
-c:v libx265 \
-c:a aac \
merged.mp4
```

---
 This is a standalone utility
 - **TestMediaCompatibility.py**
       - Analyze files
       - Checks whether files can be merged using `ffmpeg -c copy`
    - Can be run independently
- **MergeVideos.py**
       - Calls the compatibility checker
    - Generates `filelist.txt`
    - Runs FFmpeg concat
    - Produces merged output
 
 
 ## Test-MediaCompatibility.ps1
```  Python
"""
TestMediaCompatibility.py
-------------------------

Determine whether media files can be merged using:

    ffmpeg -c copy

Checks:
    - Video Codec
    - Audio Codec
    - Width
    - Height
    - FPS
    - Sample Rate
    - Audio Channels

Returns:
    Compatible (True/False)
    Detailed media profiles
"""

import json
import subprocess
from pathlib import Path


def ffprobe_json(file_path: str):

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries",
        "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json",
        file_path
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )

    return json.loads(result.stdout)


def get_media_profile(file_path: str):

    data = ffprobe_json(file_path)

    video = next(
        (s for s in data["streams"]
         if s["codec_type"] == "video"),
        {}
    )

    audio = next(
        (s for s in data["streams"]
         if s["codec_type"] == "audio"),
        {}
    )

    return {
        "file": Path(file_path).name,

        "video_codec": video.get("codec_name"),
        "width": video.get("width"),
        "height": video.get("height"),
        "fps": video.get("r_frame_rate"),

        "audio_codec": audio.get("codec_name"),
        "sample_rate": audio.get("sample_rate"),
        "channels": audio.get("channels")
    }


def test_media_compatibility(files):

    if len(files) < 2:
        raise ValueError("At least two files required.")

    reference = get_media_profile(files[0])

    results = []

    compatible = True

    for file in files:

        current = get_media_profile(file)

        match = (
            current["video_codec"] == reference["video_codec"]
            and current["width"] == reference["width"]
            and current["height"] == reference["height"]
            and current["fps"] == reference["fps"]
            and current["audio_codec"] == reference["audio_codec"]
            and current["sample_rate"] == reference["sample_rate"]
            and current["channels"] == reference["channels"]
        )

        current["compatible"] = match

        if not match:
            compatible = False

        results.append(current)

    return {
        "compatible": compatible,
        "reference": reference,
        "results": results
    }
```

MergeVideos.ps1
```  Python
"""
MergeVideos.py
--------------

Automatically merge videos.

Strategy:

    Compatible files
        -> ffmpeg concat -c copy

    Incompatible files
        -> ffmpeg concat + re-encode

Usage:

    python MergeVideos.py

    python MergeVideos.py --folder D:\\Videos

    python MergeVideos.py --extension .mkv

"""

import argparse
import subprocess
from pathlib import Path

from TestMediaCompatibility import test_media_compatibility


def create_filelist(files, filelist_path):

    with open(filelist_path, "w", encoding="utf-8") as f:

        for file in files:
            f.write(f"file '{file.resolve()}'\n")


def merge_copy(filelist, output_file):

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-f", "concat",
        "-safe", "0",
        "-i", str(filelist),
        "-c", "copy",
        str(output_file)
    ]

    return subprocess.run(cmd).returncode


def merge_reencode(filelist, output_file):

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-f", "concat",
        "-safe", "0",
        "-i", str(filelist),

        "-c:v", "libx265",
        "-crf", "26",
        "-preset", "medium",

        "-c:a", "aac",
        "-b:a", "64k",

        str(output_file)
    ]

    return subprocess.run(cmd).returncode


def main():

    parser = argparse.ArgumentParser()

	parser.add_argument(
	    "-s",
	    "--StartFolder",
	    default=".",
	    help="Source folder"
	)

	parser.add_argument(
	    "-e",
	    "--extension",
	    default=".mkv",
	    help="Video extension"
	)
	
	parser.add_argument(
	    "-o",
	    "--output",
	    default=None,
	    help="Output file"
	)

    args = parser.parse_args()

    folder = Path(args.folder)

    videos = sorted(
        folder.glob(f"*{args.extension}")
    )

    if len(videos) < 2:
        raise RuntimeError("Need at least two files.")

    if args.output:
        output_file = Path(args.output)
    else:
        output_file = folder / f"merged{args.extension}"

    compatibility = test_media_compatibility(
        [str(v) for v in videos]
    )

    filelist = folder / "filelist.txt"

    create_filelist(videos, filelist)

    try:

        if compatibility["compatible"]:

            print("\nCompatible files detected.")
            print("Using FFmpeg concat copy mode.\n")

            exit_code = merge_copy(
                filelist,
                output_file
            )

        else:

            print("\nCompatibility mismatch detected.")
            print("Falling back to re-encode merge.\n")

            exit_code = merge_reencode(
                filelist,
                output_file
            )

    finally:

        if filelist.exists():
            filelist.unlink()

    if exit_code == 0:
        print(f"\n[DONE] {output_file}")
    else:
        print(f"\n[FAIL] ExitCode={exit_code}")


if __name__ == "__main__":
    main()

```


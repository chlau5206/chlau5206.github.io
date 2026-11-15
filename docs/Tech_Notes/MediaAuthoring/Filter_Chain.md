```
 def get_video_filter(video_type: str, log_file: Path, debug_mode: bool) -> str:

    # Returns the appropriate video filter chain based on the video type preset.

        # resize video to 854 x 480

        preset = "format=yuv420p,
        scale='if(gte(iw,ih),min(iw,960),-2)':'if(gte(iw,ih),-2,min(ih,960))',"

        v_type = video_type.lower()

  

        if v_type == "anime":

            filters = preset + "unsharp=3:3:0.5,hqdn3d=1.0:1.0:4:4"

        elif v_type == "ai-anime":

            filters = preset + "unsharp=3:3:0.4,hqdn3d=1.2:1.2:5:5"

        elif v_type == "hybrid":

            filters = preset + "unsharp=3:3:0.35,hqdn3d=0.9:0.9:4:4"

        elif v_type == "live":

            filters = preset + "unsharp=3:3:0.3,hqdn3d=0.7:0.7:3:3"

        else:

            write_log(log_file, "WARNING", f"Unknown type '{video_type}'. Using 'ai-anime' preset.", debug_mode)

            filters = preset + "unsharp=3:3:0.4,hqdn3d=1.2:1.2:5:5"

  

        return filters
```


```
 filter_chain = get_video_filter(video_type, log_file, debug_mode)
 ffmpeg_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", loglevel,
        "-report",
        "-i", str(file_path),
        "-vf", filter_chain,
        "-c:v", "libx265",
        "-pix_fmt", "yuv420p10le",
        "-crf", "26",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "64k",
        str(out_path)
		}
```
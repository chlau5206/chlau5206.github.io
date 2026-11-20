### Python argparse

```  Python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f",
    "--folder",
    default=".",
    help="Input folder"
)

args = parser.parse_args()

print(args.folder)

# Usage: 
#      python MergeVideos.py -f D:\Videos
#   or python MergeVideos.py --folder D:\Videos
```

For Boolean Flags
```  Python
parser.add_argument(
    "--enable-Debug",
    action="store_true",
    help="Enable Debug"
)
```
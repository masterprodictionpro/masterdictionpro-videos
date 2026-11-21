# Master Diction Pro - video queue

- `videos/` - ready-to-post 9:16 tongue-twister videos (public raw URLs are used by Facebook/Instagram).
- `captions.txt` - caption + hashtags for each video, keyed by file name.
- `posted.log` - one line per video already posted (file | date | post ids). Post the first video in `videos/` (sorted by name) that is not in this log.
- `make_videos.py` - renders new batches (edit the RAW list; outputs to /home/claude/out).

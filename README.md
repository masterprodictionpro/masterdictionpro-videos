# Master Diction Pro - video queue

- `videos/` - ready-to-post 9:16 tongue-twister videos (public raw URLs are used by Facebook/Instagram).
- `captions.txt` - caption + hashtags for each video, keyed by file name.
- `posted.log` - one line per video already posted (file | date | post ids). Post the first video in `videos/` (sorted by name) that is not in this log.
- `make_videos.py` - renders new batches (edit the RAW list; outputs to /home/claude/out). `python3 make_videos.py 21 22` renders only those numbers.
- Every video starts with a 1.5s hook screen (big text per level, see HOOKS) to cut early swipe-aways. The hook shows "DAY N" (N = video number) and a follow line. Videos 04-20 were re-rendered with it on 2026-11-23; 01-03 were posted without it.
- `music.py` - original background music made from code (no samples, no license needed); make_videos.py adds it to every video.
- Captions from video 04 on: "Day N of the daily tongue twister!" + level line + a 💡 pronunciation tip + comment ask + follow ask; hashtags include #ESL #speakenglish #englishspeaking.

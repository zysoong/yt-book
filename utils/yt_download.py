import os
from yt_dlp import YoutubeDL, DownloadError
from yt_dlp.utils import ExtractorError

base_dir = os.path.join("../", "downloaded_videos")
ydl_opts = {
    #"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
    "outtmpl": os.path.join(base_dir, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s"),
    "restrictfilenames": True
}
URLS = ["https://www.youtube.com/watch?v=QAgR4uQ15rc&list=PLS01nW3RtgopsNLeM936V4TNSsvvVglLc"]
with YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download(URLS)
    except ExtractorError as e:
        print(e)
    except DownloadError as e:
        print(e)
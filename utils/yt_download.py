import os
from typing import Any

from yt_dlp import YoutubeDL, DownloadError
from yt_dlp.utils import ExtractorError


def download_videos(video_or_playlist_url: str, target_dir: str, is_best_quality: bool = False):
    ydl_opts_download: dict[str, Any] = {
        "outtmpl": os.path.join(target_dir, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s"),
        "restrictfilenames": True
    }

    if is_best_quality:
        ydl_opts_download["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"

    with YoutubeDL(ydl_opts_download) as ydl:
        try:
            ydl.download(video_or_playlist_url)
        except (ExtractorError, DownloadError) as e:
            print(e)


def extract_information(video_or_playlist_url: str) -> dict[str, Any]:
    ydl_opts_extract_info = {
        "skip_download": True,
        "ignoreerrors": True,
        "quiet": True,
        "no_warnings": True
    }
    with YoutubeDL(ydl_opts_extract_info) as ydl:
        return ydl.extract_info(video_or_playlist_url, download=False)

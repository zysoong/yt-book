import os
from typing import Any

from yt_dlp import YoutubeDL, DownloadError
from yt_dlp.utils import ExtractorError


def download_videos_from_playlist(playlist_url: str, is_best_quality: bool):
    base_dir = os.path.join("../", "downloaded_videos")
    ydl_opts_download: dict[str, Any] = {
        "outtmpl": os.path.join(base_dir, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s"),
        "restrictfilenames": True
    }

    if is_best_quality:
        ydl_opts_download["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"

    with YoutubeDL(ydl_opts_download) as ydl:
        try:
            ydl.download(playlist_url)
        except (ExtractorError, DownloadError) as e:
            print(e)


def extract_information_from_playlist(playlist_url: str) -> dict[str, Any]:
    ydl_opts_extract_info = {
        "ignoreerrors": True
    }
    with YoutubeDL(ydl_opts_extract_info) as ydl:
        return ydl.extract_info(playlist_url, download=False)

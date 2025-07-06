import asyncio

import os
from typing import Any

import yt_dlp
from yt_dlp import DownloadError
from yt_dlp.utils import ExtractorError

async def download_from_youtube_url(
        url: str,
        output_dir: str,
        is_best_quality: bool = False
):
    tasks = [
        asyncio.create_task(__download_youtube_single_video(video_url, output_dir, is_best_quality))
        for video_url in __generate_youtube_single_video_urls(url)
    ]
    results = await asyncio.gather(*tasks)
    print(results)


def __generate_youtube_single_video_urls(
        url: str,
) -> list[str]:
    ydl_opts_extract = {
        'extract_flat': False,
        'quiet': True,
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts_extract) as ydl:
        try:
            info: dict[str, Any] = ydl.extract_info(url, download=False)
        except (ExtractorError, DownloadError) as e:
            print(f"Error extracting info: {e}. Download will be terminated")
            return []

    if 'entries' in info:
        video_urls = [entry['original_url']
                      for entry in info.get('entries', []) if entry is not None and 'url' in entry]
        print(f"Found {len(video_urls)} videos in playlist")
    else:
        video_urls = [url]
        print(f"Found single video: {info.get('title', 'Unknown')}")

    return video_urls



async def __download_youtube_single_video(
        video_url: str,
        output_dir: str,
        is_best_quality: bool
) -> dict[str, Any]:
    def _download() -> dict[str, Any]:
        ydl_opts_download = {
            'outtmpl': os.path.join(output_dir, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s'),
            'quiet': False
        }

        if is_best_quality:
            ydl_opts_download["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"

        with yt_dlp.YoutubeDL(ydl_opts_download) as video_ydl:
            download_info = video_ydl.extract_info(video_url, download=True)
            result = {
                'title': download_info.get('title', 'Unknown'),
                'id': download_info.get('id', ''),
                'duration': download_info.get('duration', 0),
                'uploader': download_info.get('uploader', ''),
                'upload_date': download_info.get('upload_date', ''),
                'view_count': download_info.get('view_count', 0),
                'filename': download_info.get('filename', ''),
                'filesize': download_info.get('filesize', 0) or download_info.get('filesize_approx', 0),
            }
            return result

    print("Start downloading video " + video_url)
    return await asyncio.to_thread(_download)




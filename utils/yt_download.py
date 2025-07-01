import os
from typing import Any, Generator

import yt_dlp
from yt_dlp import YoutubeDL, DownloadError
from yt_dlp.utils import ExtractorError


def download_yt_videos_v2(url: str, output_dir: str) -> Generator[dict[str, Any], None, None]:
    """
    Download a YouTube playlist or single video and yield information immediately after each video completes.

    Args:
        url: URL of the YouTube playlist or single video
        output_dir: Directory to save downloaded videos

    Yields:
        Dict containing video information for each completed download
        :param url: URL link of Youtube video or playlist
        :param output_dir: Output dir of downloaded videos
    """
    ydl_opts_extract = {
        'extract_flat': False,
        'quiet': True,
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts_extract) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            if 'entries' in info:
                video_urls = [entry['url'] for entry in info.get('entries', []) if entry is not None and 'url' in entry]
                print(f"Found {len(video_urls)} videos in playlist")
            else:
                video_urls = [url]
                print(f"Found single video: {info.get('title', 'Unknown')}")

            for i, video_url in enumerate(video_urls, 1):
                print(f"Downloading video {i}/{len(video_urls)}...")

                ydl_opts_download = {
                    'outtmpl': os.path.join(output_dir, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s'),
                    'format': 'best[height<=720]',
                    'quiet': False
                }

                with yt_dlp.YoutubeDL(ydl_opts_download) as video_ydl:
                    try:
                        video_info = video_ydl.extract_info(video_url, download=True)
                        yield_info = {
                            'title': video_info.get('title', 'Unknown'),
                            'id': video_info.get('id', ''),
                            'duration': video_info.get('duration', 0),
                            'uploader': video_info.get('uploader', ''),
                            'upload_date': video_info.get('upload_date', ''),
                            'view_count': video_info.get('view_count', 0),
                            'filename': video_info.get('filename', ''),
                            'filesize': video_info.get('filesize', 0) or video_info.get('filesize_approx', 0),
                            'progress': f"{i}/{len(video_urls)}",
                            'is_playlist': len(video_urls) > 1
                        }
                        yield yield_info

                    except (ExtractorError, DownloadError) as e:
                        print(f"Error downloading video {i}: {e}. Skipped")
                        continue

        except (ExtractorError, DownloadError) as e:
            print(f"Error extracting info: {e}. Download will be terminated")
            return

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

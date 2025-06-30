import os
from utils.yt_download import download_videos, extract_information


def main():
    base_dir: str = os.path.join("./", "downloaded_videos")
    url: str = "https://www.youtube.com/watch?v=QAgR4uQ15rc"
    #info = download_videos(
    #    video_or_playlist_url=url,
    #    target_dir=base_dir
    #)
    print("#########: " + extract_information(url).get("title"))


if __name__ == "__main__":
    main()

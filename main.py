import os
from utils.yt_download import download_videos_from_playlist


def main():
    base_dir: str = os.path.join("./", "downloaded_videos")
    download_videos_from_playlist(playlist_url="https://www.youtube.com/watch?v=QAgR4uQ15rc",
                                  target_dir=base_dir)


if __name__ == "__main__":
    main()

import os
from utils.yt_download import download_yt_videos_v2


def main():
    base_dir: str = os.path.join("./", "downloaded_videos")
    url: str = "https://www.youtube.com/watch?v=QAgR4uQ15rc&list=PLS01nW3RtgopsNLeM936V4TNSsvvVglLc"
    #extract_information(url)

    for video_info in download_yt_videos_v2(url=url, output_dir=base_dir):
        print(f"✓ Downloaded: {video_info['title']}")
        print(f"  Uploader: {video_info['uploader']}")
        print(f"  Views: {video_info['view_count']:,}")
        print("-" * 50)


if __name__ == "__main__":
    main()

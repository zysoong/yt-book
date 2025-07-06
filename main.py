import asyncio

import os
from utils.yt_download import download_from_youtube_url


async def main():
    base_dir: str = os.path.join("./", "downloaded_videos")
    url: str = "https://www.youtube.com/watch?v=QAgR4uQ15rc&list=PLS01nW3RtgopsNLeM936V4TNSsvvVglLc"
    await download_from_youtube_url(url=url, output_dir=base_dir)


if __name__ == "__main__":
    asyncio.run(main())

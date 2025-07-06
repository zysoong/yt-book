import asyncio

import os

from utils.transcribe_audios import transcribe_mp3_folder
from utils.video_audio_conversion import convert_to_mp3
from utils.yt_download import download_from_youtube_url


async def main():
    base_dir_download: str = os.path.join("./", "downloaded_videos")
    base_dir_convert: str = os.path.join("./", "converted_audios")
    base_dir_transcription: str = os.path.join("./", "transcriptions")
    url: str = "https://www.youtube.com/watch?v=QAgR4uQ15rc&list=PLS01nW3RtgopsNLeM936V4TNSsvvVglLc"
    await download_from_youtube_url(url=url, output_dir=base_dir_download)
    await convert_to_mp3(input_folder=os.path.join(base_dir_download, "NA"), output_folder=base_dir_convert)
    transcribe_mp3_folder(
        input_folder=base_dir_convert,
        output_folder=base_dir_transcription,
        device="cuda",
        compute_type="int8"
    )


if __name__ == "__main__":
    asyncio.run(main())

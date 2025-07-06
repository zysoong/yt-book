import asyncio

import os

from utils.file_path_utils import get_tmp_directory
from utils.gather_data.transcribe_audios import transcribe_mp3_folder
from utils.gather_data.video_audio_conversion import convert_to_mp3
from utils.gather_data.yt_download import download_from_youtube_url


async def main():
    url_test1: str = "https://www.youtube.com/watch?v=QAgR4uQ15rc&list=PLS01nW3RtgopsNLeM936V4TNSsvvVglLc"
    url_test2: str = "https://www.youtube.com/watch?v=sLdJTcBnO3c"
    url: str = url_test2

    tmp_dir: str = get_tmp_directory(url=url, tmp_basedir="./tmp")
    tmp_dir_download: str = os.path.join(tmp_dir, "downloaded_videos")
    tmp_dir_convert: str = os.path.join(tmp_dir, "converted_audios")
    tmp_dir_transcription: str = os.path.join(tmp_dir, "transcriptions")
    await download_from_youtube_url(url=url, output_dir=tmp_dir_download)
    await convert_to_mp3(input_folder=os.path.join(tmp_dir_download, "NA"), output_folder=tmp_dir_convert)
    transcribe_mp3_folder(
        input_folder=tmp_dir_convert,
        output_folder=tmp_dir_transcription,
        device="cuda",
        compute_type="int8"
    )


if __name__ == "__main__":
    asyncio.run(main())

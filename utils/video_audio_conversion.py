import asyncio
from pathlib import Path
from moviepy import VideoFileClip

async def convert_to_mp3(
        input_folder: str,
        output_folder: str,
):
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    mp4_files: list[Path] = (
            list(Path(input_folder).glob("*.mp4")) + list(Path(input_folder).glob("*.MP4")) +
            list(Path(input_folder).glob("*.ogv")) + list(Path(input_folder).glob("*.OGV")) +
            list(Path(input_folder).glob("*.webm")) + list(Path(input_folder).glob("*.WEBM")) +
            list(Path(input_folder).glob("*.webm")) + list(Path(input_folder).glob("*.OGG"))
    )
    if not mp4_files:
        print("No Video files found in the specified folder.")
        return
    print(f"Found {len(mp4_files)} MP4 file(s) to convert...")

    tasks = [
        asyncio.create_task(__convert_video_file_to_mp3(
            str(mp4_file), str(Path(output_folder) / f"{mp4_file.name}.mp3"))
        )
        for mp4_file in mp4_files
    ]
    results = await asyncio.gather(*tasks)
    print(results)



async def __convert_video_file_to_mp3(
        video_file_path: str,
        mp3_output_path: str
):
    def _convert():
        mp4_file = Path(video_file_path)
        video_clip = VideoFileClip(str(mp4_file))
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(
            str(mp3_output_path),
            codec="libmp3lame"
        )
        audio_clip.close()
        video_clip.close()
        print(f"✓ Successfully converted to: {mp3_output_path}")

    print("Start converting video to audio" + video_file_path)
    return await asyncio.to_thread(_convert)
from pathlib import Path
from moviepy import VideoFileClip


def batch_convert_mp4_to_mp3(input_folder: str, output_folder: str=None):
    """
    Convert all MP4 files in a folder to MP3 format.

    Args:
        input_folder (str): Path to folder containing MP4 files
        output_folder (str): Path to output folder (optional, default to input_folder)
    """
    input_path = Path(input_folder)

    if output_folder is None:
        output_path = input_path
    else:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

    mp4_files = list(input_path.glob("*.mp4")) + list(input_path.glob("*.MP4"))

    if not mp4_files:
        print("No MP4 files found in the specified folder.")
        return

    print(f"Found {len(mp4_files)} MP4 file(s) to convert...")

    for mp4_file in mp4_files:
        try:
            # Create output filename
            mp3_filename = mp4_file.stem + ".mp3"
            output_file = output_path / mp3_filename

            print(f"Converting: {mp4_file.name} -> {mp3_filename}")

            # Load video and extract audio
            video_clip = VideoFileClip(str(mp4_file))
            audio_clip = video_clip.audio

            # Write audio to MP3 file
            audio_clip.write_audiofile(
                str(output_file),
                verbose=False,  # Reduce output verbosity
                logger=None  # Suppress progress bars
            )

            # Clean up
            audio_clip.close()
            video_clip.close()

            print(f"✓ Successfully converted: {mp3_filename}")

        except Exception as e:
            print(f"✗ Error converting {mp4_file.name}: {str(e)}")
            continue


def convert_mp4_to_mp3(mp4_path: str, mp3_path: str=None):
    """
    Convert a single MP4 file to MP3.

    Args:
        mp4_path (str): Path to the MP4 file
        mp3_path (str): Output path for MP3 file (optional)
    """
    mp4_file = Path(mp4_path)

    if not mp4_file.exists():
        print(f"File not found: {mp4_path}")
        return

    # Generate output filename if not provided
    if mp3_path is None:
        mp3_path = mp4_file.with_suffix('.mp3')

    try:
        print(f"Converting: {mp4_file.name}")

        video_clip = VideoFileClip(str(mp4_file))
        audio_clip = video_clip.audio

        audio_clip.write_audiofile(
            str(mp3_path),
            verbose=False,
            logger=None
        )

        audio_clip.close()
        video_clip.close()

        print(f"✓ Successfully converted to: {mp3_path}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")
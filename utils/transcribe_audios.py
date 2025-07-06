import json
import os
import torch
from faster_whisper import WhisperModel, BatchedInferencePipeline


def transcribe_mp3_folder(
    input_folder: str,
    output_folder: str,
    model_size: str = "base",
    device: str | None= None,
    compute_type: str = "float16"
) -> None:
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    os.makedirs(output_folder, exist_ok=True)
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    pipeline = BatchedInferencePipeline(model=model)

    files_to_be_transcribed: list[str] = [
        filename for filename in os.listdir(input_folder) if filename.lower().endswith(".mp3")
    ]
    for filename in files_to_be_transcribed:

        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(output_folder, output_filename)

        if os.path.exists(output_path):
            print(f"Transcription {output_path} already exists. Skipped. ")
        else:
            print(f"Transcribing {filename}...")
            segments, info = pipeline.transcribe(input_path, beam_size=5)
            output = {
                "language": info.language,
                "segments": [
                    {"start": seg.start, "end": seg.end, "text": seg.text}
                    for seg in segments
                ]
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)
            print(f"Saved transcription to {output_path}")
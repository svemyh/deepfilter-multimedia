"""Core functionality for audio and video processing."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional
from df.enhance import enhance, init_df, load_audio, save_audio


def extract_audio_from_video(video_path: str, output_audio_path: str) -> bool:
    """
    Extract audio from video using ffmpeg.

    Args:
        video_path: Path to input video file
        output_audio_path: Path to save extracted audio

    Returns:
        True if successful

    Raises:
        RuntimeError: If ffmpeg extraction fails
    """
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '48000',
        '-ac', '2',
        '-y',
        output_audio_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg audio extraction failed: {result.stderr}")
    return True


def reassemble_video_with_audio(
    original_video_path: str,
    enhanced_audio_path: str,
    output_video_path: str
) -> bool:
    """
    Reassemble video with enhanced audio.

    Args:
        original_video_path: Path to original video file
        enhanced_audio_path: Path to enhanced audio file
        output_video_path: Path to save output video

    Returns:
        True if successful

    Raises:
        RuntimeError: If ffmpeg reassembly fails
    """
    cmd = [
        'ffmpeg', '-i', original_video_path, '-i', enhanced_audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '320k',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        '-avoid_negative_ts', 'make_zero',
        '-y',
        output_video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg video reassembly failed: {result.stderr}")
    return True


def process_audio_file(
    input_path: str,
    output_path: str,
    model=None,
    df_state=None,
    verbose: bool = True
) -> None:
    """
    Process audio file with noise reduction.

    Args:
        input_path: Path to input audio file
        output_path: Path to save enhanced audio
        model: Pre-loaded DeepFilterNet model (optional)
        df_state: Pre-loaded DeepFilterNet state (optional)
        verbose: Print progress messages
    """
    if verbose:
        print(f"Processing audio: {input_path}")

    # Load model if not provided
    if model is None or df_state is None:
        if verbose:
            print("Loading DeepFilterNet model...")
        model, df_state, _ = init_df()

    # Load and enhance audio
    if verbose:
        print("Enhancing audio...")
    audio, _ = load_audio(input_path, sr=df_state.sr())
    enhanced = enhance(model, df_state, audio)

    # Save enhanced audio
    if verbose:
        print("Saving enhanced audio...")
    save_audio(output_path, enhanced, df_state.sr())

    if verbose:
        print(f"Processing complete: {output_path}")


def process_video_file(
    input_path: str,
    output_path: str,
    model=None,
    df_state=None,
    verbose: bool = True
) -> None:
    """
    Process video file with noise reduction.

    Args:
        input_path: Path to input video file
        output_path: Path to save enhanced video
        model: Pre-loaded DeepFilterNet model (optional)
        df_state: Pre-loaded DeepFilterNet state (optional)
        verbose: Print progress messages
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_audio_path = os.path.join(temp_dir, "extracted_audio.wav")
        temp_enhanced_path = os.path.join(temp_dir, "enhanced_audio.wav")

        if verbose:
            print(f"Processing video: {input_path}")
            print(f"Output: {output_path}")

        # Extract audio
        if verbose:
            print("Extracting audio...")
        extract_audio_from_video(input_path, temp_audio_path)

        # Load model if not provided
        if model is None or df_state is None:
            if verbose:
                print("Loading DeepFilterNet model...")
            model, df_state, _ = init_df()

        # Enhance audio
        if verbose:
            print("Enhancing audio...")
        audio, _ = load_audio(temp_audio_path, sr=df_state.sr())
        enhanced = enhance(model, df_state, audio)

        # Save enhanced audio
        if verbose:
            print("Saving enhanced audio...")
        save_audio(temp_enhanced_path, enhanced, df_state.sr())

        # Reassemble video
        if verbose:
            print("Reassembling video...")
        reassemble_video_with_audio(input_path, temp_enhanced_path, output_path)

        if verbose:
            print(f"Processing complete: {output_path}")


def process_file(
    input_path: str,
    output_path: Optional[str] = None,
    verbose: bool = True
) -> str:
    """
    Automatically detect file type and process accordingly.

    Args:
        input_path: Path to input file
        output_path: Path to save output (optional, auto-generated if None)
        verbose: Print progress messages

    Returns:
        Path to output file

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If file type is unsupported
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Auto-generate output path if not provided
    if output_path is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{input_path.stem}_enhanced{input_path.suffix}"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Detect file type and process
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv', '.m4v'}
    audio_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac', '.wma'}

    file_ext = input_path.suffix.lower()

    if file_ext in video_extensions:
        process_video_file(str(input_path), str(output_path), verbose=verbose)
    elif file_ext in audio_extensions:
        process_audio_file(str(input_path), str(output_path), verbose=verbose)
    else:
        raise ValueError(
            f"Unsupported file type: {file_ext}\n"
            f"Supported video: {', '.join(sorted(video_extensions))}\n"
            f"Supported audio: {', '.join(sorted(audio_extensions))}"
        )

    return str(output_path)

import os
import subprocess
import tempfile
from pathlib import Path
from df.enhance import enhance, init_df, load_audio, save_audio

def extract_audio_from_video(video_path, output_audio_path):
    """Extract audio from video using ffmpeg."""
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

def reassemble_video_with_audio(original_video_path, enhanced_audio_path, output_video_path):
    """Reassemble video with enhanced audio."""
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

def process_video_with_noise_reduction(input_video_path, output_video_path):
    """Process video with noise reduction pipeline."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_audio_path = os.path.join(temp_dir, "extracted_audio.wav")
        temp_enhanced_path = os.path.join(temp_dir, "enhanced_audio.wav")
        
        print(f"Processing video: {input_video_path}")
        print(f"Output: {output_video_path}")
        
        print("Extracting audio...")
        extract_audio_from_video(input_video_path, temp_audio_path)
        
        print("Loading DeepFilterNet model...")
        model, df_state, _ = init_df()
        
        print("Enhancing audio...")
        audio, _ = load_audio(temp_audio_path, sr=df_state.sr())
        enhanced = enhance(model, df_state, audio)
        
        print("Saving enhanced audio...")
        save_audio(temp_enhanced_path, enhanced, df_state.sr())
        
        print("Reassembling video...")
        reassemble_video_with_audio(input_video_path, temp_enhanced_path, output_video_path)
        
        print(f"Processing complete: {output_video_path}")

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    input_video = "data/2025-10-06_21-41-37.mkv"
    output_video = "output/2025-10-06_21-41-37_enhanced.mkv"
    
    if not os.path.exists(input_video):
        print(f"Error: Input video file '{input_video}' not found.")
        exit(1)
    
    try:
        process_video_with_noise_reduction(input_video, output_video)
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        exit(1)

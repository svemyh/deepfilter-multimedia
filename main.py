from df.enhance import enhance, init_df, load_audio, save_audio
from df.utils import download_file

if __name__ == "__main__":
    # Load default model
    model, df_state, _ = init_df()
    # Download and open some audio file. You use your audio files here
    audio_path = "/home/sve/rnd/audio-filtering/data/rec.wav"
    audio, _ = load_audio(audio_path, sr=df_state.sr())
    # Denoise the audio
    enhanced = enhance(model, df_state, audio)
    # Save for listening
    if not os.path.exists("./output"):
        os.makedirs("./output")
    save_audio("output/enhanced.wav", enhanced, df_state.sr())

# DeepFilter Multimedia

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Remove noise from audio and video files using [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet). This CLI tool (`dfm`) provides a simple interface for applying state-of-the-art deep learning-based noise reduction to multimedia files.

## Features

- **Audio Support**: WAV, MP3, FLAC, OGG, M4A, AAC, WMA
- **Video Support**: MP4, MKV, AVI, MOV, WebM, FLV, WMV, M4V
- **Easy CLI**: Simple command-line interface (`dfm`)
- **Auto-detection**: Automatically detects file type
- **Batch Processing**: Process multiple files at once

## Installation

### From PyPI (when published)

```bash
pip install deepfilter-multimedia
```

### From Source

```bash
# Clone the repository
git clone https://github.com/svemyh/deepfilter-multimedia.git
cd deepfilter-multimedia

# Install dependencies
pip install -e .
```

### Requirements

- Python 3.8+
- PyTorch 1.9+
- FFmpeg (for video processing)
- DeepFilterNet

Install FFmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Usage

### Basic Usage

Process a single audio or video file:

```bash
dfm input.mp4
```

The enhanced file will be saved to `output/input_enhanced.mp4`.

### Specify Output Path

```bash
dfm input.mp4 -o output/clean.mp4
```

### Process Multiple Files

```bash
dfm video1.mp4 video2.mkv audio1.wav
```

All files will be saved to the `output/` directory.

### Quiet Mode

Disable progress messages:

```bash
dfm input.mp4 -q
```

### Help

```bash
dfm --help
```

## Examples

### Clean noisy interview recording
```bash
dfm noisy_interview.mp4 -o clean_interview.mp4
```

### Process podcast audio
```bash
dfm podcast_episode.mp3
```

### Batch process multiple videos
```bash
dfm video1.mkv video2.mp4 video3.avi
```

### Use as Python module
```python
from deepfilter_multimedia.core import process_file

# Process a file
output_path = process_file("noisy_video.mp4", "clean_video.mp4")
print(f"Enhanced video saved to: {output_path}")
```

## How It Works

1. **For Videos**:
   - Extracts audio track (48kHz, stereo)
   - Applies DeepFilterNet noise reduction
   - Reassembles video with enhanced audio
   - Keeps original video quality

2. **For Audio**:
   - Loads audio file
   - Applies DeepFilterNet noise reduction
   - Saves enhanced audio

### Model Download
On first run, DeepFilterNet will download the pretrained model (~50MB). This may take a few moments.

## Supported Formats

### Video
MP4, MKV, AVI, MOV, WebM, FLV, WMV, M4V

### Audio
WAV, MP3, FLAC, OGG, M4A, AAC, WMA

## Attribution

This project is based on [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) by Hendrik Schröter et al.

If you use this tool, please cite the original DeepFilterNet papers:

```bibtex
@inproceedings{schroeter2022deepfilternet,
  title={{DeepFilterNet}: A Low Complexity Speech Enhancement Framework for Full-Band Audio based on Deep Filtering},
  author={Schröter, Hendrik and Escalante-B., Alberto N. and Rosenkranz, Tobias and Maier, Andreas},
  booktitle={ICASSP 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2022},
  organization={IEEE}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

DeepFilterNet is dual-licensed under MIT and Apache 2.0 licenses.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [DeepFilterNet Repository](https://github.com/Rikorose/DeepFilterNet)
- [DeepFilterNet Paper](https://arxiv.org/abs/2110.05588)
- [Report Issues](https://github.com/svemyh/deepfilter-multimedia/issues)
- [Changelog](CHANGELOG.md)

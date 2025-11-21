# Whisper Audio Transcriber

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Whisper](https://img.shields.io/badge/Whisper-openai-whisper-brightgreen)

Transcribe audio and video files to text using OpenAI's Whisper model. Supports multiple output formats and batch processing of directories.

## Features

- 🎙️ **Multiple model sizes**: `tiny`, `base`, `small`, `medium`, `large`
- 📁 **Batch processing**: Transcribe entire directories of audio/video files
- 📝 **Multiple output formats**:
  - Plain text (`.txt`)
  - Subtitles (`.srt`)
  - JSON with full metadata (`.json`)
- 🌐 **Language specification**: Force transcription in specific languages
- ⚡ **GPU acceleration**: Automatically uses CUDA when available
- 📊 **Processing statistics**: Shows duration and character count for each transcription

## Installation

### Prerequisites
- Python 3.7+
- PyTorch (automatically installed via pip)
- FFmpeg (required for audio processing)

### Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/whisper-transcriber.git
cd whisper-transcriber

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface (Recommended)
```bash
python transcriber.py \
  --input ./audio_files \
  --output ./transcriptions \
  --model medium \
  --language es \
  --format srt
```

#### Arguments:
| Argument | Short | Default | Description |
|----------|-------|---------|-------------|
| `--input` | `-i` | `.` | Input directory containing audio/video files |
| `--output` | `-o` | `./transcripciones` | Output directory for transcriptions |
| `--model` | `-m` | `medium` | Model size: `tiny`, `base`, `small`, `medium`, `large` |
| `--language` | `-l` | *auto-detect* | Language code (e.g., `es`, `en`, `fr`) |
| `--format` | `-f` | `txt` | Output format: `txt`, `srt`, `json` |

### Simple API (For Quick Scripts)
```python
from transcriber import transcribir_carpeta_simple

# Transcribe all audio files in ./wav directory
transcribir_carpeta_simple(
    carpeta_audio="./wav",
    modelo="large",
    idioma="es"
)
```

## Supported File Formats
Audio: `.wav`, `.mp3`, `.m4a`, `.flac`, `.aac`, `.ogg`  
Video: `.mp4`, `.avi`, `.mov`, `.mkv`

## Examples

### 1. Transcribe all MP3s in current directory to Spanish text files
```bash
python transcriber.py --language es --format txt
```

### 2. Generate subtitles for all videos in a folder
```bash
python transcriber.py \
  --input ./videos \
  --output ./subtitles \
  --model small \
  --format srt
```

### 3. Create JSON transcripts with full metadata
```bash
python transcriber.py --format json --model base
```

## Performance Notes
- **GPU Recommended**: For large models (medium/large), a NVIDIA GPU with at least 10GB VRAM is recommended
- **Model Size Trade-offs**:
  | Model | Relative Speed | VRAM Usage | Accuracy |
  |-------|----------------|------------|----------|
  | tiny | 32x | ~1GB | Low |
  | base | 16x | ~1GB | Medium |
  | small | 6x | ~2GB | Good |
  | medium | 2x | ~5GB | High |
  | large | 1x | ~10GB | Highest |

## Dependencies
- `openai-whisper` (main transcription engine)
- `torch` (PyTorch for GPU acceleration)
- `ffmpeg-python` (audio/video processing)
- Standard libraries: `os`, `pathlib`, `argparse`, `json`

Install all dependencies with:
```bash
pip install openai-whisper torch ffmpeg-python
```
---

> **Note**: First run will download the Whisper model (~486MB for medium model). Subsequent runs will use the cached model.
> 
> For large batches, consider using smaller models first to test configuration before running with larger models.

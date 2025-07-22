# Video Learning Gamification System

Transform NeetCode System Design videos into interactive learning materials with AI-generated quizzes, flashcards, and summaries.

## Features

- **Video to Audio**: Extract high-quality audio from MP4 videos using FFmpeg
- **Speech Recognition**: Transcribe audio using OpenAI Whisper (95%+ accuracy)
- **AI Learning Materials**: Generate quizzes, flashcards, and summaries using GPT-4
- **Batch Processing**: Handle all 20 videos automatically
- **Structured Output**: Organized folders with JSON and text formats

## Directory Structure

```
transcription-system/
├── audio/                 # Extracted audio files (.wav)
├── transcripts/          # Generated transcriptions (.txt, .json)
├── learning-materials/   # AI-generated learning content
│   └── [topic]/         # Per-topic directories
│       ├── summary.json     # Topic overview and objectives
│       ├── quiz.json        # Multiple choice, T/F, short answer
│       └── flashcards.json  # Study flashcards
├── scripts/             # Processing scripts
└── requirements.txt     # Python dependencies
```

## Setup

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **OpenAI API Key** (Required for learning materials generation)

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Full Pipeline (All Videos)

```bash
cd transcription-system
python scripts/main_pipeline.py
```

### Test Mode (Single Video)

```bash
python scripts/main_pipeline.py test
python scripts/main_pipeline.py test "0 - Computer Architecture.mp4"
```

### Individual Steps

```bash
# Step 1: Convert videos to audio
python scripts/video_to_audio.py

# Step 2: Transcribe audio to text  
python scripts/audio_to_text.py

# Step 3: Generate learning materials (requires OpenAI API key)
python scripts/generate_learning_materials.py
```

## Output

Each video topic generates:

- **Summary**: Key concepts, learning objectives, difficulty level
- **Quiz**: 10 questions (multiple choice, true/false, short answer)
- **Flashcards**: 15 cards covering important terms and concepts

Perfect for spaced repetition learning and self-assessment!

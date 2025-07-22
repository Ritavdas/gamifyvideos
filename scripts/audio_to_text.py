#!/usr/bin/env python3
"""
Audio to Text Transcription Script
Uses OpenAI Whisper to transcribe audio files to text
"""

import os
import sys
import json
from pathlib import Path
import whisper

class AudioTranscriber:
    def __init__(self, model_size="base"):
        """Initialize Whisper model"""
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("✓ Whisper model loaded")
    
    def transcribe_audio(self, audio_path, output_dir):
        """Transcribe a single audio file"""
        audio_file = Path(audio_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Output file paths
        text_file = output_dir / f"{audio_file.stem}.txt"
        json_file = output_dir / f"{audio_file.stem}.json"
        
        try:
            print(f"Transcribing {audio_file.name}...")
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                str(audio_file),
                language="en",  # Force English for technical content
                task="transcribe",
                word_timestamps=True  # Get word-level timestamps
            )
            
            # Save plain text transcription
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(result["text"].strip())
            
            # Save detailed JSON with timestamps
            transcription_data = {
                "file": audio_file.name,
                "language": result.get("language", "en"),
                "duration": result.get("duration", 0),
                "text": result["text"].strip(),
                "segments": result["segments"]
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(transcription_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Transcribed {audio_file.name} -> {text_file.name}")
            return str(text_file), str(json_file)
            
        except Exception as e:
            print(f"✗ Error transcribing {audio_file.name}: {e}")
            return None, None
    
    def batch_transcribe(self, audio_dir, output_dir):
        """Transcribe all audio files in directory"""
        audio_dir = Path(audio_dir)
        
        # Find all WAV files
        audio_files = list(audio_dir.glob("*.wav"))
        
        if not audio_files:
            print("No WAV files found in the audio directory")
            return []
        
        print(f"Found {len(audio_files)} audio files")
        
        transcribed_files = []
        for audio_file in sorted(audio_files):
            text_file, json_file = self.transcribe_audio(audio_file, output_dir)
            if text_file and json_file:
                transcribed_files.append({
                    "audio": str(audio_file),
                    "text": text_file,
                    "json": json_file
                })
        
        print(f"\nTranscription complete: {len(transcribed_files)}/{len(audio_files)} files transcribed")
        return transcribed_files

def main():
    # Setup paths
    current_dir = Path.cwd()
    audio_dir = current_dir / "audio"
    transcripts_dir = current_dir / "transcripts"
    
    print("=== Audio to Text Transcription ===")
    print(f"Audio directory: {audio_dir}")
    print(f"Transcripts directory: {transcripts_dir}")
    
    # Check if audio files exist
    if not audio_dir.exists():
        print("Audio directory doesn't exist. Run video_to_audio.py first.")
        sys.exit(1)
    
    # Initialize transcriber (using 'base' model for speed, 'large' for accuracy)
    transcriber = AudioTranscriber(model_size="base")
    
    # Batch transcribe
    transcribed_files = transcriber.batch_transcribe(audio_dir, transcripts_dir)
    
    if transcribed_files:
        print(f"\n✓ Successfully transcribed {len(transcribed_files)} audio files")
        
        # Save transcription summary
        summary_file = transcripts_dir / "transcription_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(transcribed_files, f, indent=2)
        print(f"✓ Transcription summary saved to {summary_file}")
    else:
        print("\n✗ No files were transcribed")
        sys.exit(1)

if __name__ == "__main__":
    main()
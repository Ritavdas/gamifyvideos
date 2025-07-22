#!/usr/bin/env python3
"""
Video to Audio Conversion Script
Converts MP4 videos to high-quality WAV audio files using FFmpeg
"""

import os
import subprocess
import sys
from pathlib import Path

def convert_video_to_audio(video_path, audio_output_dir):
    """Convert a single video file to audio"""
    video_file = Path(video_path)
    audio_file = Path(audio_output_dir) / f"{video_file.stem}.wav"
    
    # FFmpeg command for high-quality audio extraction
    cmd = [
        'ffmpeg',
        '-i', str(video_file),
        '-vn',  # No video output
        '-acodec', 'pcm_s16le',  # Uncompressed 16-bit PCM
        '-ar', '16000',  # 16kHz sample rate (optimal for Whisper)
        '-ac', '1',  # Mono audio
        '-y',  # Overwrite output files
        str(audio_file)
    ]
    
    try:
        print(f"Converting {video_file.name} to audio...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Created {audio_file.name}")
        return str(audio_file)
    except subprocess.CalledProcessError as e:
        print(f"✗ Error converting {video_file.name}")
        print(f"Command: {' '.join(cmd)}")
        print(f"Error output: {e.stderr}")
        return None

def batch_convert_videos(video_dir, audio_output_dir):
    """Convert all MP4 videos in directory to audio"""
    video_dir = Path(video_dir)
    audio_output_dir = Path(audio_output_dir)
    
    # Create output directory
    audio_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all MP4 files
    video_files = list(video_dir.glob("*.mp4"))
    
    if not video_files:
        print("No MP4 files found in the directory")
        return []
    
    print(f"Found {len(video_files)} video files")
    
    converted_files = []
    for video_file in sorted(video_files):
        audio_file = convert_video_to_audio(video_file, audio_output_dir)
        if audio_file:
            converted_files.append(audio_file)
    
    print(f"\nConversion complete: {len(converted_files)}/{len(video_files)} files converted")
    return converted_files

if __name__ == "__main__":
    # Get directories
    current_dir = Path.cwd()
    video_dir = current_dir.parent  # Parent directory contains the MP4 files
    audio_dir = current_dir / "audio"
    
    print("=== Video to Audio Conversion ===")
    print(f"Video directory: {video_dir}")
    print(f"Audio output directory: {audio_dir}")
    
    converted_files = batch_convert_videos(video_dir, audio_dir)
    
    if converted_files:
        print(f"\n✓ Successfully converted {len(converted_files)} videos to audio")
    else:
        print("\n✗ No files were converted")
        sys.exit(1)
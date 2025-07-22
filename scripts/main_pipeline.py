#!/usr/bin/env python3
"""
Main Processing Pipeline
Orchestrates the complete video-to-learning-materials conversion process
"""

import os
import sys
import time
from pathlib import Path

# Add scripts directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import our processing modules
from video_to_audio import batch_convert_videos
from audio_to_text import AudioTranscriber
from generate_learning_materials import LearningMaterialsGenerator

def run_complete_pipeline():
    """Run the complete processing pipeline"""
    start_time = time.time()
    
    print("=" * 60)
    print("🎓 VIDEO LEARNING GAMIFICATION SYSTEM")
    print("=" * 60)
    
    # Setup paths
    current_dir = Path.cwd()
    parent_dir = current_dir.parent  # Contains the MP4 files
    audio_dir = current_dir / "audio"
    transcripts_dir = current_dir / "transcripts"
    learning_materials_dir = current_dir / "learning-materials"
    
    print(f"📁 Working directory: {current_dir}")
    print(f"📹 Video source: {parent_dir}")
    print(f"🔊 Audio output: {audio_dir}")
    print(f"📝 Transcripts: {transcripts_dir}")
    print(f"🎯 Learning materials: {learning_materials_dir}")
    print()
    
    # Step 1: Convert videos to audio
    print("🎬 STEP 1: Converting videos to audio")
    print("-" * 40)
    try:
        converted_files = batch_convert_videos(parent_dir, audio_dir)
        if not converted_files:
            print("❌ No videos were converted. Exiting.")
            return False
        print(f"✅ Converted {len(converted_files)} videos to audio")
    except Exception as e:
        print(f"❌ Error in video conversion: {e}")
        return False
    
    print()
    
    # Step 2: Transcribe audio to text
    print("🎤 STEP 2: Transcribing audio to text")
    print("-" * 40)
    try:
        transcriber = AudioTranscriber(model_size="base")  # Use "large" for better accuracy
        transcribed_files = transcriber.batch_transcribe(audio_dir, transcripts_dir)
        if not transcribed_files:
            print("❌ No audio files were transcribed. Exiting.")
            return False
        print(f"✅ Transcribed {len(transcribed_files)} audio files")
    except Exception as e:
        print(f"❌ Error in transcription: {e}")
        return False
    
    print()
    
    # Step 3: Generate learning materials
    print("🧠 STEP 3: Generating learning materials")
    print("-" * 40)
    try:
        generator = LearningMaterialsGenerator()
        processed_files = generator.batch_process_transcripts(transcripts_dir, learning_materials_dir)
        if not processed_files:
            print("❌ No learning materials were generated. Exiting.")
            return False
        print(f"✅ Generated learning materials for {len(processed_files)} topics")
    except Exception as e:
        print(f"❌ Error generating learning materials: {e}")
        return False
    
    # Final summary
    end_time = time.time()
    processing_time = end_time - start_time
    
    print()
    print("=" * 60)
    print("🎉 PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"⏱️  Total processing time: {processing_time:.1f} seconds")
    print(f"📹 Videos processed: {len(converted_files)}")
    print(f"📝 Transcripts created: {len(transcribed_files)}")
    print(f"🎯 Learning topics: {len(processed_files)}")
    print()
    print("📚 Generated materials for each topic:")
    for topic in processed_files:
        print(f"  • {topic['topic']}: {', '.join(topic['materials_generated'])}")
    
    print()
    print("🚀 Your learning materials are ready!")
    print(f"📂 Check the '{learning_materials_dir.name}' directory")
    
    return True

def run_single_video_test(video_name=None):
    """Test the pipeline with a single video"""
    print("🧪 TESTING MODE: Processing single video")
    print("-" * 40)
    
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    
    # Find available videos
    video_files = list(parent_dir.glob("*.mp4"))
    if not video_files:
        print("❌ No MP4 files found in parent directory")
        return False
    
    # Select video to test
    if video_name:
        test_video = parent_dir / video_name
        if not test_video.exists():
            print(f"❌ Video '{video_name}' not found")
            return False
    else:
        # Use the first video for testing
        test_video = sorted(video_files)[0]
    
    print(f"🎬 Testing with: {test_video.name}")
    
    # Create temporary directories
    test_audio_dir = current_dir / "test_audio"
    test_transcripts_dir = current_dir / "test_transcripts"  
    test_materials_dir = current_dir / "test_learning_materials"
    
    try:
        # Step 1: Convert single video
        from video_to_audio import convert_video_to_audio
        audio_file = convert_video_to_audio(test_video, test_audio_dir)
        if not audio_file:
            return False
        
        # Step 2: Transcribe single audio
        transcriber = AudioTranscriber(model_size="base")
        text_file, json_file = transcriber.transcribe_audio(audio_file, test_transcripts_dir)
        if not text_file:
            return False
        
        # Step 3: Generate learning materials
        generator = LearningMaterialsGenerator()
        result = generator.process_transcript(text_file, test_materials_dir)
        if not result:
            return False
        
        print(f"✅ Test completed successfully!")
        print(f"📂 Test results in: test_* directories")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Test mode with single video
            video_name = sys.argv[2] if len(sys.argv) > 2 else None
            success = run_single_video_test(video_name)
        else:
            print("Usage: python main_pipeline.py [test] [video_name]")
            print("  test: Run in test mode with single video")
            print("  video_name: Specific video to test (optional)")
            sys.exit(1)
    else:
        # Full pipeline
        success = run_complete_pipeline()
    
    sys.exit(0 if success else 1)
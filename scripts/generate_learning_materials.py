#!/usr/bin/env python3
"""
Learning Materials Generator
Uses OpenAI GPT to generate quizzes, flashcards, and learning materials from transcripts
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


class LearningMaterialsGenerator:
    def __init__(self):
        """Initialize OpenAI client"""
        load_dotenv()
        self.client = OpenAI(api_key="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")

    def generate_quiz_questions(self, transcript_text, topic):
        """Generate quiz questions from transcript"""
        prompt = f"""
        Based on this {topic} transcript, generate 10 quiz questions that test understanding of the key concepts.
        
        Include a mix of:
        - 5 multiple choice questions (4 options each)
        - 3 true/false questions
        - 2 short answer questions
        
        Format as JSON with this structure:
        {{
            "multiple_choice": [
                {{
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 0,
                    "explanation": "Why this answer is correct"
                }}
            ],
            "true_false": [
                {{
                    "question": "Statement to evaluate",
                    "correct_answer": true,
                    "explanation": "Explanation of the answer"
                }}
            ],
            "short_answer": [
                {{
                    "question": "Question requiring explanation",
                    "sample_answer": "Example good answer",
                    "key_points": ["point1", "point2"]
                }}
            ]
        }}
        
        Transcript:
        {transcript_text[:3000]}...
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating quiz questions: {e}")
            return None

    def generate_flashcards(self, transcript_text, topic):
        """Generate flashcards from transcript"""
        prompt = f"""
        Based on this {topic} transcript, create 15 flashcards covering the most important concepts.
        
        Format as JSON:
        {{
            "flashcards": [
                {{
                    "front": "Term or question",
                    "back": "Definition or answer",
                    "category": "concept category",
                    "difficulty": "easy|medium|hard"
                }}
            ]
        }}
        
        Focus on:
        - Key technical terms and definitions
        - Important concepts and principles
        - Practical applications
        - Common misconceptions to clarify
        
        Transcript:
        {transcript_text[:3000]}...
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return None

    def generate_summary(self, transcript_text, topic):
        """Generate topic summary and key takeaways"""
        prompt = f"""
        Based on this {topic} transcript, create a comprehensive summary.
        
        Format as JSON:
        {{
            "summary": "2-3 paragraph overview of the topic",
            "key_concepts": ["concept1", "concept2", "..."],
            "learning_objectives": ["After studying this, you will understand...", "..."],
            "difficulty_level": "beginner|intermediate|advanced",
            "estimated_study_time": "X minutes",
            "prerequisites": ["required knowledge"],
            "related_topics": ["topics to study next"]
        }}
        
        Transcript:
        {transcript_text}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    def process_transcript(self, transcript_file, output_dir):
        """Process a single transcript and generate all learning materials"""
        transcript_path = Path(transcript_file)
        topic = transcript_path.stem.replace("_", " ").title()

        # Read transcript
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()

        if not transcript_text.strip():
            print(f"Empty transcript: {transcript_path.name}")
            return None

        print(f"Processing {topic}...")

        # Create output directory for this topic
        topic_dir = Path(output_dir) / transcript_path.stem
        topic_dir.mkdir(parents=True, exist_ok=True)

        results = {}

        # Generate summary
        print(f"  Generating summary...")
        summary = self.generate_summary(transcript_text, topic)
        if summary:
            with open(topic_dir / "summary.json", "w") as f:
                json.dump(summary, f, indent=2)
            results["summary"] = summary

        # Generate quiz questions
        print(f"  Generating quiz questions...")
        quiz = self.generate_quiz_questions(transcript_text, topic)
        if quiz:
            with open(topic_dir / "quiz.json", "w") as f:
                json.dump(quiz, f, indent=2)
            results["quiz"] = quiz

        # Generate flashcards
        print(f"  Generating flashcards...")
        flashcards = self.generate_flashcards(transcript_text, topic)
        if flashcards:
            with open(topic_dir / "flashcards.json", "w") as f:
                json.dump(flashcards, f, indent=2)
            results["flashcards"] = flashcards

        print(f"✓ Generated learning materials for {topic}")
        return results

    def batch_process_transcripts(self, transcripts_dir, output_dir):
        """Process all transcript files"""
        transcripts_dir = Path(transcripts_dir)
        output_dir = Path(output_dir)

        # Find all text transcripts
        transcript_files = list(transcripts_dir.glob("*.txt"))

        if not transcript_files:
            print("No transcript files found")
            return []

        print(f"Found {len(transcript_files)} transcript files")

        processed_files = []
        for transcript_file in sorted(transcript_files):
            result = self.process_transcript(transcript_file, output_dir)
            if result:
                processed_files.append(
                    {
                        "transcript": str(transcript_file),
                        "topic": transcript_file.stem,
                        "materials_generated": list(result.keys()),
                    }
                )

        print(
            f"\nProcessing complete: {len(processed_files)}/{len(transcript_files)} files processed"
        )
        return processed_files


def main():
    # Setup paths
    current_dir = Path.cwd()
    transcripts_dir = current_dir / "transcripts"
    learning_materials_dir = current_dir / "learning-materials"

    print("=== Learning Materials Generation ===")
    print(f"Transcripts directory: {transcripts_dir}")
    print(f"Output directory: {learning_materials_dir}")

    # Check if transcripts exist
    if not transcripts_dir.exists():
        print("Transcripts directory doesn't exist. Run audio_to_text.py first.")
        sys.exit(1)

    # Initialize generator
    try:
        generator = LearningMaterialsGenerator()
    except SystemExit:
        return

    # Process all transcripts
    processed_files = generator.batch_process_transcripts(
        transcripts_dir, learning_materials_dir
    )

    if processed_files:
        print(
            f"\n✓ Successfully generated learning materials for {len(processed_files)} topics"
        )

        # Save processing summary
        summary_file = learning_materials_dir / "generation_summary.json"
        with open(summary_file, "w") as f:
            json.dump(processed_files, f, indent=2)
        print(f"✓ Generation summary saved to {summary_file}")
    else:
        print("\n✗ No learning materials were generated")
        sys.exit(1)


if __name__ == "__main__":
    main()

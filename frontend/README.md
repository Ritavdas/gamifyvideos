# NeetCode System Design Learning Hub - Frontend

A gamified web interface for studying system design concepts with AI-generated quizzes and flashcards.

## Features

🎯 **Interactive Learning**
- Topic overview with progress tracking
- AI-generated quizzes with immediate feedback
- Flip-able flashcards for active recall
- Progress statistics and streaks

🎮 **Gamification**
- Score tracking across all topics
- Study streaks and achievements
- Progress bars for visual motivation
- Difficulty-based flashcard categorization

📱 **Modern UI**
- Clean, responsive design with Tailwind CSS
- Smooth animations and transitions
- Mobile-friendly interface
- Dark/light theme support

## Setup & Usage

1. **Copy Learning Materials**
```bash
cd frontend
python3 copy-data.py
```

2. **Start Local Server**
```bash
python3 -m http.server 8000
```

3. **Open in Browser**
```
http://localhost:8000
```

## Features Overview

### 📚 Topics View
- Grid view of all 20 system design topics
- Progress indicators for each topic
- Quick access to quizzes and flashcards
- Completion status tracking

### ❓ Quiz Mode
- Multiple choice, true/false, and short answer questions
- Real-time progress tracking
- Immediate scoring and feedback
- Retake functionality
- Score persistence

### 🗂️ Flashcards
- Interactive flip cards
- Shuffle functionality
- Topic-based categorization
- Difficulty indicators
- Study progress tracking

### 📊 Progress Dashboard
- Overall completion statistics
- Average scores across topics
- Study streak tracking
- Detailed per-topic progress

## Data Structure

The frontend loads JSON data from:
```
data/
├── 0 - Computer Architecture/
│   ├── summary.json
│   ├── quiz.json
│   └── flashcards.json
├── 1 - Application Architecture/
└── ... (all 20 topics)
```

## Local Storage

Progress is automatically saved to browser localStorage:
- Quiz scores and completion status
- Study streaks and achievements
- Last study dates
- Flashcard progress

## Customization

The interface can be easily customized by:
- Modifying Tailwind classes in `index.html`
- Updating color schemes and animations in the CSS
- Adding new gamification features in `app.js`
- Extending the data structure for additional content types

Perfect for self-paced learning with built-in motivation through gamification!
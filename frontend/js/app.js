// Learning Hub Application
class LearningHub {
    constructor() {
        this.topics = [];
        this.currentTopic = null;
        this.currentQuiz = null;
        this.currentQuizIndex = 0;
        this.currentFlashcardIndex = 0;
        this.userAnswers = [];
        this.progress = this.loadProgress();
        
        this.init();
    }

    async init() {
        this.showLoading();
        await this.loadTopics();
        this.setupEventListeners();
        this.hideLoading();
        this.showView('topics');
        this.updateStats();
    }

    // Data Loading
    async loadTopics() {
        try {
            // Since we can't directly read from file system in browser,
            // we'll create a topics list and load data dynamically
            const topicNames = [
                "0 - Computer Architecture",
                "1 - Application Architecture", 
                "2 - Design Requirements",
                "3 - Networking Basics",
                "4 - TCP and UDP",
                "5 - DNS",
                "6 - HTTP",
                "7 - WebSockets",
                "8 - API Paradigms",
                "9 - API Design",
                "10 - Caching",
                "11 - CDNs",
                "12 - Proxies and Load Balancing",
                "13 - Consistent Hashing",
                "14 - SQL",
                "15 - NoSQL",
                "16 - Replication and Sharding",
                "17 - CAP Theorem",
                "18 - Object Storage",
                "19 - Message Queues"
            ];

            this.topics = topicNames.map((name, index) => ({
                id: index,
                name: name,
                displayName: name.replace(/^\d+\s*-\s*/, ''),
                fileName: name.replace(/\s+/g, '_').replace(/-/g, '_'),
                completed: this.progress.completedTopics.includes(index),
                quizScore: this.progress.quizScores[index] || 0,
                flashcardsStudied: this.progress.flashcardsStudied[index] || 0
            }));

            this.renderTopics();
        } catch (error) {
            console.error('Error loading topics:', error);
            this.showError('Failed to load topics');
        }
    }

    async loadTopicData(topic) {
        try {
            // Fetch from the copied data directory
            const summary = await this.fetchJSON(`data/${topic.name}/summary.json`);
            const quiz = await this.fetchJSON(`data/${topic.name}/quiz.json`);
            const flashcards = await this.fetchJSON(`data/${topic.name}/flashcards.json`);

            return { summary, quiz, flashcards };
        } catch (error) {
            console.error(`Error loading data for ${topic.name}:`, error);
            return this.getFallbackData(topic);
        }
    }

    async fetchJSON(url) {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to fetch ${url}`);
        return await response.json();
    }

    getFallbackData(topic) {
        // Fallback data structure when files aren't available
        return {
            summary: {
                summary: `Learn about ${topic.displayName} and its key concepts in system design.`,
                key_concepts: ["Core concepts", "Implementation", "Best practices"],
                learning_objectives: [`Understand ${topic.displayName}`, "Apply concepts in real scenarios"],
                difficulty_level: "intermediate",
                estimated_study_time: "30 minutes"
            },
            quiz: {
                multiple_choice: [
                    {
                        question: `What is a key characteristic of ${topic.displayName}?`,
                        options: ["Option A", "Option B", "Option C", "Option D"],
                        correct_answer: 0,
                        explanation: "This is the correct answer because..."
                    }
                ],
                true_false: [
                    {
                        question: `${topic.displayName} is essential for system design.`,
                        correct_answer: true,
                        explanation: "True, it plays a crucial role."
                    }
                ],
                short_answer: [
                    {
                        question: `Explain the main benefits of ${topic.displayName}.`,
                        sample_answer: "The main benefits include...",
                        key_points: ["Benefit 1", "Benefit 2"]
                    }
                ]
            },
            flashcards: {
                flashcards: [
                    {
                        front: topic.displayName,
                        back: `Key concept related to ${topic.displayName}`,
                        category: "fundamentals",
                        difficulty: "medium"
                    }
                ]
            }
        };
    }

    // UI Rendering
    renderTopics() {
        const grid = document.getElementById('topicsGrid');
        grid.innerHTML = '';

        this.topics.forEach(topic => {
            const card = this.createTopicCard(topic);
            grid.appendChild(card);
        });
    }

    createTopicCard(topic) {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer';
        
        const completedClass = topic.completed ? 'text-green-500' : 'text-gray-400';
        const progressWidth = topic.quizScore ? `${topic.quizScore}%` : '0%';

        card.innerHTML = `
            <div class="flex items-start justify-between mb-4">
                <h3 class="text-lg font-bold text-gray-800 line-clamp-2">${topic.displayName}</h3>
                <i class="fas fa-check-circle text-xl ${completedClass}"></i>
            </div>
            <div class="mb-4">
                <div class="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>${topic.quizScore}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full transition-all" style="width: ${progressWidth}"></div>
                </div>
            </div>
            <div class="flex justify-between items-center">
                <div class="flex space-x-2">
                    <button class="quiz-btn bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600" data-topic-id="${topic.id}">
                        <i class="fas fa-question-circle mr-1"></i>Quiz
                    </button>
                    <button class="flashcards-btn bg-purple-500 text-white px-3 py-1 rounded text-sm hover:bg-purple-600" data-topic-id="${topic.id}">
                        <i class="fas fa-layer-group mr-1"></i>Cards
                    </button>
                </div>
                <div class="text-xs text-gray-500">
                    ${topic.flashcardsStudied} cards studied
                </div>
            </div>
        `;

        // Add click handlers
        card.querySelector('.quiz-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.startQuiz(topic.id);
        });

        card.querySelector('.flashcards-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.startFlashcards(topic.id);
        });

        card.addEventListener('click', () => {
            this.showTopicSummary(topic.id);
        });

        return card;
    }

    // Quiz Functionality
    async startQuiz(topicId) {
        this.showLoading();
        const topic = this.topics[topicId];
        this.currentTopic = topic;
        
        try {
            const data = await this.loadTopicData(topic);
            this.currentQuiz = this.flattenQuizQuestions(data.quiz);
            this.currentQuizIndex = 0;
            this.userAnswers = [];
            
            this.showView('quiz');
            this.showQuizInterface();
            this.renderCurrentQuestion();
        } catch (error) {
            console.error('Error starting quiz:', error);
            this.showError('Failed to load quiz');
        }
        this.hideLoading();
    }

    flattenQuizQuestions(quiz) {
        const questions = [];
        
        // Multiple choice questions
        quiz.multiple_choice?.forEach(q => {
            questions.push({
                type: 'multiple_choice',
                question: q.question,
                options: q.options,
                correct_answer: q.correct_answer,
                explanation: q.explanation
            });
        });

        // True/false questions
        quiz.true_false?.forEach(q => {
            questions.push({
                type: 'true_false',
                question: q.question,
                options: ['True', 'False'],
                correct_answer: q.correct_answer ? 0 : 1,
                explanation: q.explanation
            });
        });

        // Short answer questions
        quiz.short_answer?.forEach(q => {
            questions.push({
                type: 'short_answer',
                question: q.question,
                sample_answer: q.sample_answer,
                key_points: q.key_points
            });
        });

        return questions;
    }

    showQuizInterface() {
        document.getElementById('quizTopicSelection').classList.add('hidden');
        document.getElementById('quizInterface').classList.remove('hidden');
        document.getElementById('quizResults').classList.add('hidden');
        document.getElementById('quizTopicTitle').textContent = this.currentTopic.displayName;
    }

    renderCurrentQuestion() {
        const question = this.currentQuiz[this.currentQuizIndex];
        const container = document.getElementById('questionContainer');
        const counter = document.getElementById('questionCounter');
        
        counter.textContent = `Question ${this.currentQuizIndex + 1} of ${this.currentQuiz.length}`;
        this.updateQuizProgress();

        if (question.type === 'short_answer') {
            container.innerHTML = `
                <div class="mb-6">
                    <h4 class="text-xl font-semibold text-gray-800 mb-4">${question.question}</h4>
                    <textarea class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                              rows="6" placeholder="Type your answer here..."></textarea>
                </div>
            `;
        } else {
            const optionsHTML = question.options.map((option, index) => `
                <label class="flex items-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                    <input type="radio" name="answer" value="${index}" class="mr-3">
                    <span class="text-gray-800">${option}</span>
                </label>
            `).join('');

            container.innerHTML = `
                <div class="mb-6">
                    <h4 class="text-xl font-semibold text-gray-800 mb-6">${question.question}</h4>
                    <div class="space-y-3">
                        ${optionsHTML}
                    </div>
                </div>
            `;
        }

        // Update navigation buttons
        document.getElementById('prevQuestion').disabled = this.currentQuizIndex === 0;
        const nextBtn = document.getElementById('nextQuestion');
        nextBtn.textContent = this.currentQuizIndex === this.currentQuiz.length - 1 ? 'Finish Quiz' : 'Next';
    }

    updateQuizProgress() {
        const progress = (this.currentQuizIndex + 1) / this.currentQuiz.length;
        const circumference = 2 * Math.PI * 40;
        const offset = circumference - (progress * circumference);
        
        document.querySelector('.progress-ring-circle').style.strokeDashoffset = offset;
    }

    // Flashcards Functionality
    async startFlashcards(topicId) {
        this.showLoading();
        const topic = this.topics[topicId];
        this.currentTopic = topic;
        
        try {
            const data = await this.loadTopicData(topic);
            this.currentFlashcards = data.flashcards.flashcards || [];
            this.currentFlashcardIndex = 0;
            
            this.showView('flashcards');
            this.showFlashcardInterface();
            this.renderCurrentFlashcard();
        } catch (error) {
            console.error('Error starting flashcards:', error);
            this.showError('Failed to load flashcards');
        }
        this.hideLoading();
    }

    showFlashcardInterface() {
        document.getElementById('flashcardTopicSelection').classList.add('hidden');
        document.getElementById('flashcardInterface').classList.remove('hidden');
        document.getElementById('flashcardTopicTitle').textContent = this.currentTopic.displayName;
    }

    renderCurrentFlashcard() {
        if (!this.currentFlashcards.length) return;
        
        const flashcard = this.currentFlashcards[this.currentFlashcardIndex];
        const counter = document.getElementById('flashcardCounter');
        
        counter.textContent = `Card ${this.currentFlashcardIndex + 1} of ${this.currentFlashcards.length}`;
        
        document.getElementById('flashcardFront').innerHTML = `
            <div class="text-lg font-semibold text-gray-800">${flashcard.front}</div>
            <div class="text-sm text-gray-500 mt-2">${flashcard.category}</div>
        `;
        
        document.getElementById('flashcardBack').innerHTML = `
            <div class="text-lg text-gray-800">${flashcard.back}</div>
            <div class="text-sm text-gray-500 mt-2">Difficulty: ${flashcard.difficulty}</div>
        `;

        // Reset flip state
        document.getElementById('flashcard').classList.remove('flipped');

        // Update navigation buttons
        document.getElementById('prevFlashcard').disabled = this.currentFlashcardIndex === 0;
        document.getElementById('nextFlashcard').disabled = this.currentFlashcardIndex === this.currentFlashcards.length - 1;
    }

    // Navigation & Event Handlers
    setupEventListeners() {
        // Navigation buttons
        document.getElementById('topicsBtn').addEventListener('click', () => this.showView('topics'));
        document.getElementById('quizBtn').addEventListener('click', () => this.showView('quiz'));
        document.getElementById('flashcardsBtn').addEventListener('click', () => this.showView('flashcards'));
        document.getElementById('progressBtn').addEventListener('click', () => this.showView('progress'));

        // Quiz navigation
        document.getElementById('prevQuestion').addEventListener('click', () => this.prevQuestion());
        document.getElementById('nextQuestion').addEventListener('click', () => this.nextQuestion());
        document.getElementById('retakeQuiz').addEventListener('click', () => this.retakeQuiz());
        document.getElementById('backToTopics').addEventListener('click', () => this.showView('topics'));

        // Flashcard navigation
        document.getElementById('flashcard').addEventListener('click', () => this.flipFlashcard());
        document.getElementById('prevFlashcard').addEventListener('click', () => this.prevFlashcard());
        document.getElementById('nextFlashcard').addEventListener('click', () => this.nextFlashcard());
        document.getElementById('shuffleFlashcards').addEventListener('click', () => this.shuffleFlashcards());
        document.getElementById('backToFlashcardTopics').addEventListener('click', () => this.showView('flashcards'));
    }

    showView(viewName) {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => view.classList.add('hidden'));
        
        // Show selected view
        document.getElementById(`${viewName}View`).classList.remove('hidden');
        
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.className = 'nav-btn bg-gray-300 text-gray-700 px-6 py-2 rounded-lg font-semibold transition-colors hover:bg-gray-400';
        });
        document.getElementById(`${viewName}Btn`).className = 'nav-btn bg-blue-500 text-white px-6 py-2 rounded-lg font-semibold transition-colors hover:bg-blue-600';

        // Load view-specific content
        if (viewName === 'progress') {
            this.renderProgress();
        }
    }

    // Quiz Navigation
    prevQuestion() {
        if (this.currentQuizIndex > 0) {
            this.saveCurrentAnswer();
            this.currentQuizIndex--;
            this.renderCurrentQuestion();
        }
    }

    nextQuestion() {
        this.saveCurrentAnswer();
        
        if (this.currentQuizIndex < this.currentQuiz.length - 1) {
            this.currentQuizIndex++;
            this.renderCurrentQuestion();
        } else {
            this.finishQuiz();
        }
    }

    saveCurrentAnswer() {
        const question = this.currentQuiz[this.currentQuizIndex];
        let answer = null;

        if (question.type === 'short_answer') {
            answer = document.querySelector('textarea').value;
        } else {
            const selected = document.querySelector('input[name="answer"]:checked');
            answer = selected ? parseInt(selected.value) : null;
        }

        this.userAnswers[this.currentQuizIndex] = answer;
    }

    finishQuiz() {
        const score = this.calculateScore();
        this.saveQuizProgress(score);
        this.showQuizResults(score);
    }

    calculateScore() {
        let correct = 0;
        let total = 0;

        this.currentQuiz.forEach((question, index) => {
            if (question.type !== 'short_answer') {
                total++;
                if (this.userAnswers[index] === question.correct_answer) {
                    correct++;
                }
            }
        });

        return { correct, total, percentage: total > 0 ? Math.round((correct / total) * 100) : 0 };
    }

    showQuizResults(score) {
        document.getElementById('quizInterface').classList.add('hidden');
        document.getElementById('quizResults').classList.remove('hidden');
        
        document.getElementById('finalScore').textContent = `${score.percentage}%`;
        document.getElementById('correctAnswers').textContent = score.correct;
        document.getElementById('incorrectAnswers').textContent = score.total - score.correct;
        document.getElementById('totalQuestions').textContent = score.total;
    }

    retakeQuiz() {
        this.currentQuizIndex = 0;
        this.userAnswers = [];
        this.showQuizInterface();
        this.renderCurrentQuestion();
    }

    // Flashcard Navigation
    flipFlashcard() {
        document.getElementById('flashcard').classList.toggle('flipped');
    }

    prevFlashcard() {
        if (this.currentFlashcardIndex > 0) {
            this.currentFlashcardIndex--;
            this.renderCurrentFlashcard();
        }
    }

    nextFlashcard() {
        if (this.currentFlashcardIndex < this.currentFlashcards.length - 1) {
            this.currentFlashcardIndex++;
            this.renderCurrentFlashcard();
        }
    }

    shuffleFlashcards() {
        for (let i = this.currentFlashcards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.currentFlashcards[i], this.currentFlashcards[j]] = [this.currentFlashcards[j], this.currentFlashcards[i]];
        }
        this.currentFlashcardIndex = 0;
        this.renderCurrentFlashcard();
    }

    // Progress & Statistics
    renderProgress() {
        const completedCount = this.progress.completedTopics.length;
        const totalScore = Object.values(this.progress.quizScores).reduce((sum, score) => sum + score, 0);
        const averageScore = completedCount > 0 ? Math.round(totalScore / completedCount) : 0;

        document.getElementById('completedTopics').textContent = completedCount;
        document.getElementById('averageScore').textContent = `${averageScore}%`;
        document.getElementById('studyStreak').textContent = this.progress.streak;

        this.renderTopicProgress();
    }

    renderTopicProgress() {
        const container = document.getElementById('topicProgressList');
        container.innerHTML = '';

        this.topics.forEach(topic => {
            const progressBar = document.createElement('div');
            progressBar.className = 'flex items-center justify-between p-4 bg-gray-50 rounded-lg';
            
            const progress = topic.quizScore || 0;
            progressBar.innerHTML = `
                <div class="flex-1">
                    <div class="flex justify-between items-center mb-2">
                        <span class="font-semibold text-gray-800">${topic.displayName}</span>
                        <span class="text-sm text-gray-600">${progress}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-blue-500 h-2 rounded-full transition-all" style="width: ${progress}%"></div>
                    </div>
                </div>
            `;

            container.appendChild(progressBar);
        });
    }

    updateStats() {
        const totalScore = Object.values(this.progress.quizScores).reduce((sum, score) => sum + score, 0);
        document.getElementById('totalScore').textContent = totalScore;
        document.getElementById('streakCount').textContent = this.progress.streak;
    }

    // Progress Persistence
    loadProgress() {
        const saved = localStorage.getItem('learningHubProgress');
        return saved ? JSON.parse(saved) : {
            completedTopics: [],
            quizScores: {},
            flashcardsStudied: {},
            streak: 0,
            lastStudyDate: null
        };
    }

    saveProgress() {
        localStorage.setItem('learningHubProgress', JSON.stringify(this.progress));
    }

    saveQuizProgress(score) {
        if (!this.progress.completedTopics.includes(this.currentTopic.id)) {
            this.progress.completedTopics.push(this.currentTopic.id);
        }
        this.progress.quizScores[this.currentTopic.id] = score.percentage;
        
        // Update streak
        const today = new Date().toDateString();
        if (this.progress.lastStudyDate !== today) {
            this.progress.streak++;
            this.progress.lastStudyDate = today;
        }

        this.saveProgress();
        this.updateStats();
        
        // Update topic card
        this.topics[this.currentTopic.id].completed = true;
        this.topics[this.currentTopic.id].quizScore = score.percentage;
    }

    // Utility Functions
    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('hidden');
    }

    showError(message) {
        alert(`Error: ${message}`);
    }

    showTopicSummary(topicId) {
        // This would show a modal with topic summary
        // For now, just navigate to the topic
        console.log(`Show summary for topic ${topicId}`);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new LearningHub();
});
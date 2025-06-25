#!/usr/bin/env python3
"""
Interactive Quiz System for Learning Buddy
Provides real-time quiz experience with immediate feedback
"""

import json
import random
import time
from typing import Dict, List, Any
from user_profile import UserProfile

class InteractiveQuiz:
    """Interactive quiz system with real-time Q&A"""
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.current_score = 0
        self.total_questions = 0
        self.correct_answers = 0
        self.quiz_data = None
        
    def generate_quiz_questions(self, topic: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions for a topic"""
        mastery_level = self.user_profile.progress.get("mastery_levels", {}).get(topic, "beginner")
        
        # Sample quiz questions database - you can expand this
        question_bank = {
            "Machine Learning": {
                "beginner": [
                    {
                        "type": "multiple-choice",
                        "question": "What is Machine Learning?",
                        "options": ["A) A programming language", "B) A subset of Artificial Intelligence", "C) A type of database", "D) A web framework"],
                        "correct": "B",
                        "explanation": "Machine Learning is a subset of Artificial Intelligence that enables computers to learn and make decisions from data without being explicitly programmed."
                    },
                    {
                        "type": "multiple-choice", 
                        "question": "Which of the following is a supervised learning algorithm?",
                        "options": ["A) K-means clustering", "B) Linear Regression", "C) Principal Component Analysis", "D) Association Rules"],
                        "correct": "B",
                        "explanation": "Linear Regression is a supervised learning algorithm that predicts continuous values based on labeled training data."
                    },
                    {
                        "type": "true-false",
                        "question": "Machine Learning models can only work with numerical data.",
                        "options": ["True", "False"],
                        "correct": "False",
                        "explanation": "Machine Learning models can work with various types of data including text, images, categorical data, and numerical data."
                    },
                    {
                        "type": "multiple-choice",
                        "question": "What is overfitting in Machine Learning?",
                        "options": ["A) When a model performs well on training data but poorly on new data", "B) When a model is too simple", "C) When there's too little training data", "D) When the algorithm runs too fast"],
                        "correct": "A",
                        "explanation": "Overfitting occurs when a model learns the training data too well, including noise, making it perform poorly on new, unseen data."
                    },
                    {
                        "type": "multiple-choice",
                        "question": "Which of these is NOT a type of Machine Learning?",
                        "options": ["A) Supervised Learning", "B) Unsupervised Learning", "C) Reinforcement Learning", "D) Deterministic Learning"],
                        "correct": "D",
                        "explanation": "Deterministic Learning is not a recognized type of Machine Learning. The main types are Supervised, Unsupervised, and Reinforcement Learning."
                    }
                ],
                "intermediate": [
                    {
                        "type": "multiple-choice",
                        "question": "What is the purpose of cross-validation?",
                        "options": ["A) To increase training speed", "B) To assess model performance and prevent overfitting", "C) To reduce dataset size", "D) To normalize data"],
                        "correct": "B",
                        "explanation": "Cross-validation is used to assess how well a model will generalize to new data and helps prevent overfitting by testing on multiple data splits."
                    },
                    {
                        "type": "multiple-choice",
                        "question": "Which metric is most appropriate for evaluating a classification model with imbalanced classes?",
                        "options": ["A) Accuracy", "B) F1-Score", "C) Mean Squared Error", "D) R-squared"],
                        "correct": "B",
                        "explanation": "F1-Score is better for imbalanced datasets as it considers both precision and recall, unlike accuracy which can be misleading."
                    }
                ]
            },
            "Python": {
                "beginner": [
                    {
                        "type": "multiple-choice",
                        "question": "What is the correct way to create a list in Python?",
                        "options": ["A) list = {1, 2, 3}", "B) list = [1, 2, 3]", "C) list = (1, 2, 3)", "D) list = <1, 2, 3>"],
                        "correct": "B",
                        "explanation": "Lists in Python are created using square brackets []. Curly braces {} create sets or dictionaries, parentheses () create tuples."
                    },
                    {
                        "type": "true-false",
                        "question": "Python is case-sensitive.",
                        "options": ["True", "False"],
                        "correct": "True",
                        "explanation": "Python is case-sensitive, meaning 'Variable' and 'variable' are treated as different identifiers."
                    },
                    {
                        "type": "multiple-choice",
                        "question": "Which of the following is used to define a function in Python?",
                        "options": ["A) function", "B) def", "C) define", "D) func"],
                        "correct": "B",
                        "explanation": "The 'def' keyword is used to define functions in Python."
                    }
                ]
            },
            "Mathematics": {
                "beginner": [
                    {
                        "type": "multiple-choice",
                        "question": "What is the derivative of x²?",
                        "options": ["A) x", "B) 2x", "C) x²", "D) 2"],
                        "correct": "B",
                        "explanation": "Using the power rule: d/dx(x²) = 2x¹ = 2x"
                    },
                    {
                        "type": "true-false",
                        "question": "The integral of a derivative gives back the original function (plus a constant).",
                        "options": ["True", "False"],
                        "correct": "True",
                        "explanation": "This is the Fundamental Theorem of Calculus - integration and differentiation are inverse operations."
                    }
                ]
            }
        }
        
        # Get questions for the topic and level
        topic_questions = question_bank.get(topic, {})
        level_questions = topic_questions.get(mastery_level, [])
        
        # If not enough questions for the level, mix with other levels
        all_topic_questions = []
        for level, questions in topic_questions.items():
            all_topic_questions.extend(questions)
        
        if len(level_questions) < num_questions and all_topic_questions:
            level_questions = all_topic_questions
        
        # If still no questions, create generic ones
        if not level_questions:
            level_questions = [
                {
                    "type": "multiple-choice",
                    "question": f"Which of the following is most important when studying {topic}?",
                    "options": ["A) Memorization", "B) Understanding concepts", "C) Speed", "D) Copying examples"],
                    "correct": "B",
                    "explanation": f"Understanding core concepts is crucial for mastering {topic}. This builds a strong foundation for advanced topics."
                },
                {
                    "type": "true-false",
                    "question": f"Regular practice is important for learning {topic}.",
                    "options": ["True", "False"],
                    "correct": "True",
                    "explanation": f"Consistent practice helps reinforce concepts and build proficiency in {topic}."
                }
            ]
        
        # Select random questions
        selected_questions = random.sample(level_questions, min(num_questions, len(level_questions)))
        return selected_questions
    
    def run_interactive_quiz(self, topic: str, num_questions: int = 5):
        """Run an interactive quiz session"""
        print(f"\n🧠 INTERACTIVE QUIZ: {topic}")
        print("=" * 50)
        
        # Generate questions
        questions = self.generate_quiz_questions(topic, num_questions)
        if not questions:
            print("❌ Sorry, no questions available for this topic yet.")
            return
        
        self.total_questions = len(questions)
        self.correct_answers = 0
        
        print(f"📚 Topic: {topic}")
        print(f"📋 Questions: {self.total_questions}")
        print(f"📊 Difficulty: {self.user_profile.progress.get('mastery_levels', {}).get(topic, 'beginner').title()}")
        print("\n🎯 Instructions:")
        print("• Answer each question by typing the letter (A, B, C, D) or True/False")
        print("• You'll get immediate feedback after each answer")
        print("• Your progress will be tracked automatically")
        
        input("\n📖 Press Enter to start the quiz...")
        
        # Run through questions
        for i, question in enumerate(questions, 1):
            self.ask_question(i, question)
            print()  # Add spacing between questions
        
        # Calculate final score
        score_percentage = (self.correct_answers / self.total_questions) * 100
        
        # Show results
        self.show_quiz_results(topic, score_percentage)
        
        # Record the result
        time_spent = self.total_questions * 2  # Estimate 2 minutes per question
        self.user_profile.record_activity(topic, score_percentage, time_spent)
        
        return score_percentage
    
    def ask_question(self, question_num: int, question_data: Dict):
        """Ask a single question and get user response"""
        print(f"\n📝 Question {question_num}/{self.total_questions}")
        print("-" * 30)
        print(f"❓ {question_data['question']}")
        print()
        
        # Display options
        for option in question_data['options']:
            print(f"   {option}")
        
        # Get user answer
        while True:
            try:
                user_answer = input("\n💭 Your answer: ").strip().upper()
                
                # Validate input
                if question_data['type'] == 'true-false':
                    if user_answer in ['TRUE', 'T', 'FALSE', 'F']:
                        user_answer = 'True' if user_answer in ['TRUE', 'T'] else 'False'
                        break
                    else:
                        print("❌ Please enter True/False or T/F")
                        continue
                else:
                    if user_answer in ['A', 'B', 'C', 'D']:
                        break
                    else:
                        print("❌ Please enter A, B, C, or D")
                        continue
                        
            except (EOFError, KeyboardInterrupt):
                print("\n⏸️  Quiz paused. Your progress has been saved.")
                return
        
        # Check answer
        correct_answer = question_data['correct']
        
        if user_answer == correct_answer:
            print("✅ Correct! Well done!")
            self.correct_answers += 1
        else:
            print(f"❌ Incorrect. The correct answer is: {correct_answer}")
        
        # Show explanation
        print(f"💡 Explanation: {question_data['explanation']}")
        
        # Show progress
        current_score = (self.correct_answers / question_num) * 100
        print(f"📊 Current Score: {self.correct_answers}/{question_num} ({current_score:.1f}%)")
        
        # Wait a moment before next question
        if question_num < self.total_questions:
            input("🔄 Press Enter for the next question...")
    
    def show_quiz_results(self, topic: str, score_percentage: float):
        """Show final quiz results"""
        print("\n" + "=" * 50)
        print("🎉 QUIZ COMPLETED!")
        print("=" * 50)
        
        print(f"📚 Topic: {topic}")
        print(f"📊 Final Score: {self.correct_answers}/{self.total_questions} ({score_percentage:.1f}%)")
        
        # Performance feedback
        if score_percentage >= 90:
            feedback = "🏆 Outstanding! You've mastered this topic!"
            emoji = "🟢"
        elif score_percentage >= 80:
            feedback = "🎯 Excellent work! You have a strong understanding!"
            emoji = "🟢"
        elif score_percentage >= 70:
            feedback = "👍 Good job! You're getting there!"
            emoji = "🟡"
        elif score_percentage >= 60:
            feedback = "📈 Not bad! Keep practicing to improve!"
            emoji = "🟡"
        else:
            feedback = "💪 Keep studying! Practice makes perfect!"
            emoji = "🔴"
        
        print(f"{emoji} {feedback}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if score_percentage < 70:
            print(f"• Review the basic concepts of {topic}")
            print(f"• Practice more exercises")
            print(f"• Consider getting explanations for difficult concepts")
        elif score_percentage < 90:
            print(f"• You're doing well! Try more advanced topics")
            print(f"• Focus on areas where you made mistakes")
        else:
            print(f"• Excellent mastery! Consider advanced topics")
            print(f"• Help others or teach the concepts you've learned")
        
        print(f"• Take regular quizzes to maintain your knowledge")
        print(f"• Your progress has been automatically saved")

def create_custom_quiz():
    """Allow users to create custom quiz topics"""
    print("\n🎨 CUSTOM QUIZ CREATOR")
    print("=" * 30)
    print("You can create quizzes for any topic!")
    
    topic = input("Enter your topic: ").strip()
    if not topic:
        print("❌ Topic cannot be empty")
        return None
    
    try:
        num_questions = int(input("Number of questions (1-10): ").strip())
        if not 1 <= num_questions <= 10:
            num_questions = 5
    except:
        num_questions = 5
    
    return topic, num_questions

# Quick demo function
def demo_interactive_quiz():
    """Demo the interactive quiz system"""
    print("🎮 INTERACTIVE QUIZ DEMO")
    print("=" * 30)
    
    # Create a demo user
    user_profile = UserProfile("demo_user")
    quiz_system = InteractiveQuiz(user_profile)
    
    # Demo with Machine Learning quiz
    print("Starting a Machine Learning quiz...")
    quiz_system.run_interactive_quiz("Machine Learning", 3)

if __name__ == "__main__":
    demo_interactive_quiz()

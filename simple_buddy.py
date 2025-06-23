#!/usr/bin/env python3
"""
Learning Buddy System - Fallback Mode
Works without external LLM when GROQ is unavailable
"""

from user_profile import UserProfile
import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class SimpleLearningBuddy:
    """Simplified Learning Buddy that works without external LLM"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_profile = UserProfile(user_id)
    
    def get_dashboard(self):
        """Get user learning dashboard"""
        insights = self.user_profile.get_learning_insights()
        
        print("\n" + "="*50)
        print("🎓 LEARNING BUDDY DASHBOARD")
        print("="*50)
        print(f"📚 Total Topics: {insights['total_topics']}")
        print(f"🏆 Mastered Topics: {insights['mastered_topics']}")
        print(f"⏰ Total Study Time: {insights['study_time_hours']} hours")
        print(f"📈 Learning Consistency: {insights['learning_consistency']}")
        
        if insights['struggling_topics']:
            print(f"🔴 Need Attention: {', '.join(insights['struggling_topics'])}")
        
        print("\n📊 Current Topics & Mastery Levels:")
        for topic, level in self.user_profile.progress.get('mastery_levels', {}).items():
            emoji = {"advanced": "🟢", "intermediate": "🟡", "beginner": "🔵", "struggling": "🔴"}
            print(f"  {emoji.get(level, '⚪')} {topic}: {level.title()}")
        
        print("="*50)
    
    def analyze_progress(self, topic: str = None):
        """Simple progress analysis without LLM"""
        insights = self.user_profile.get_learning_insights()
        progress = self.user_profile.progress
        
        analysis = []
        analysis.append("📊 LEARNING PROGRESS ANALYSIS")
        analysis.append("=" * 40)
        
        if topic:
            analysis.append(f"🔍 Focus Topic: {topic}")
            if topic in progress.get('mastery_levels', {}):
                level = progress['mastery_levels'][topic]
                analysis.append(f"📈 Current Level: {level.title()}")
                
                if topic in progress.get('quiz_scores', {}):
                    scores = progress['quiz_scores'][topic]
                    avg_score = sum(s['score'] for s in scores) / len(scores)
                    latest_score = scores[-1]['score']
                    analysis.append(f"📋 Average Score: {avg_score:.1f}%")
                    analysis.append(f"🎯 Latest Score: {latest_score}%")
                    
                    if len(scores) > 1:
                        trend = "improving" if latest_score > scores[0]['score'] else "needs attention"
                        analysis.append(f"📈 Trend: {trend}")
        
        analysis.append(f"\n📚 Overall Statistics:")
        analysis.append(f"  • Total Topics: {insights['total_topics']}")
        analysis.append(f"  • Mastered Topics: {insights['mastered_topics']}")
        analysis.append(f"  • Study Time: {insights['study_time_hours']} hours")
        analysis.append(f"  • Consistency: {insights['learning_consistency']}")
        
        if insights['struggling_topics']:
            analysis.append(f"\n🔴 Topics Needing Attention:")
            for topic in insights['struggling_topics']:
                analysis.append(f"  • {topic}")
        
        # Recommendations
        analysis.append(f"\n💡 Quick Recommendations:")
        if insights['total_topics'] == 0:
            analysis.append("  • Start with a topic you're interested in")
            analysis.append("  • Set aside 15-30 minutes daily for learning")
        elif insights['learning_consistency'] == 'Inactive':
            analysis.append("  • Resume regular study sessions")
            analysis.append("  • Start with shorter sessions to build momentum")
        elif insights['struggling_topics']:
            analysis.append("  • Focus extra time on challenging topics")
            analysis.append("  • Break difficult concepts into smaller parts")
        else:
            analysis.append("  • Keep up the great work!")
            analysis.append("  • Consider adding new topics to expand knowledge")
        
        return "\n".join(analysis)
    
    def generate_explanation(self, topic: str, concept: str):
        """Simple explanation without LLM"""
        user_style = self.user_profile.profile.get("preferred_explanation_style", "simple")
        learning_style = self.user_profile.profile.get("learning_style", "visual")
        
        explanation = []
        explanation.append(f"💡 EXPLAINING: {concept} in {topic}")
        explanation.append("=" * 50)
        
        # Basic explanation framework
        explanation.append(f"📚 Topic: {topic}")
        explanation.append(f"🎯 Concept: {concept}")
        explanation.append(f"👤 Your Learning Style: {learning_style}")
        explanation.append(f"📝 Preferred Style: {user_style}")
        
        explanation.append(f"\n🔍 Basic Explanation:")
        explanation.append(f"The concept '{concept}' is a key part of {topic}.")
        
        # Style-specific suggestions
        style_tips = {
            "visual": [
                "• Try creating diagrams or mind maps",
                "• Use colors to highlight important parts", 
                "• Look for visual examples online",
                "• Draw connections between concepts"
            ],
            "auditory": [
                "• Read the explanation out loud",
                "• Find podcasts or videos about this topic",
                "• Discuss with others or teach someone else",
                "• Create rhymes or songs to remember key points"
            ],
            "kinesthetic": [
                "• Practice with hands-on examples",
                "• Use physical models if possible",
                "• Take notes while learning",
                "• Apply the concept in real scenarios"
            ],
            "reading": [
                "• Read multiple sources about this concept",
                "• Take detailed written notes",
                "• Create summaries and outlines",
                "• Write your own explanations"
            ]
        }
        
        explanation.append(f"\n🎨 Learning Tips for {learning_style.title()} Learners:")
        tips = style_tips.get(learning_style, style_tips["visual"])
        explanation.extend(tips)
        
        # General study suggestions
        explanation.append(f"\n📖 Next Steps:")
        explanation.append("• Break down complex parts into smaller pieces")
        explanation.append("• Practice with examples or exercises")
        explanation.append("• Connect to what you already know")
        explanation.append("• Test your understanding with questions")
        
        explanation.append(f"\n💪 Remember: Understanding takes time - be patient with yourself!")
        
        return "\n".join(explanation)
    
    def generate_quiz(self, topic: str, num_questions: int = 5):
        """Generate simple quiz without LLM"""
        mastery_level = self.user_profile.progress.get("mastery_levels", {}).get(topic, "beginner")
        
        quiz = []
        quiz.append(f"🧠 ADAPTIVE QUIZ: {topic}")
        quiz.append("=" * 50)
        quiz.append(f"📈 Difficulty Level: {mastery_level.title()}")
        quiz.append(f"📋 Questions: {num_questions}")
        
        # Sample quiz structure
        quiz.append(f"\n📝 Quiz Questions for {topic}:")
        
        for i in range(1, num_questions + 1):
            quiz.append(f"\n{i}. [Sample Question {i} about {topic}]")
            quiz.append(f"   A) Option A")
            quiz.append(f"   B) Option B") 
            quiz.append(f"   C) Option C")
            quiz.append(f"   D) Option D")
        
        quiz.append(f"\n💡 Quiz Generation Tips:")
        quiz.append(f"• Questions are tailored to your {mastery_level} level")
        quiz.append(f"• Focus on core concepts in {topic}")
        quiz.append(f"• Review incorrect answers for better understanding")
        quiz.append(f"• Regular practice improves retention")
        
        quiz.append(f"\n📊 After completing the quiz:")
        quiz.append(f"• Record your score using option 9 in the main menu")
        quiz.append(f"• This helps track your progress and adjust difficulty")
        
        return "\n".join(quiz)
    
    def create_weekly_plan(self, focus_topics: List[str] = None):
        """Create simple weekly learning plan"""
        if focus_topics is None:
            focus_topics = self.user_profile.progress.get("current_topics", [])[:3]
        
        if not focus_topics:
            focus_topics = ["Choose a topic to get started"]
        
        time_available = self.user_profile.profile.get('time_availability', 30)
        
        plan = []
        plan.append("📅 WEEKLY LEARNING PLAN")
        plan.append("=" * 50)
        plan.append(f"⏰ Daily Time Available: {time_available} minutes")
        plan.append(f"📚 Focus Topics: {', '.join(focus_topics)}")
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(days):
            plan.append(f"\n📆 {day}:")
            
            if i < len(focus_topics):
                topic = focus_topics[i % len(focus_topics)]
                plan.append(f"  🎯 Focus: {topic}")
                plan.append(f"  📖 Activity: Study core concepts ({time_available//2} min)")
                plan.append(f"  🧠 Practice: Quiz or exercises ({time_available//2} min)")
            else:
                plan.append(f"  🔄 Review: Previous topics ({time_available//2} min)")
                plan.append(f"  📝 Reflection: Note what you've learned ({time_available//2} min)")
        
        plan.append(f"\n💡 Weekly Goals:")
        plan.append(f"• Complete at least 4 study sessions")
        plan.append(f"• Take 1-2 practice quizzes")
        plan.append(f"• Review challenging concepts")
        plan.append(f"• Track your progress")
        
        return "\n".join(plan)
    
    def get_motivation_boost(self):
        """Get motivational message"""
        insights = self.user_profile.get_learning_insights()
        
        messages = []
        
        # Base encouragement
        if insights['total_topics'] == 0:
            messages.append("🌟 Welcome to your learning journey! Every expert was once a beginner.")
            messages.append("💪 The first step is always the hardest - you've already taken it by being here!")
            messages.append("🎯 Set your first learning goal and start with just 15 minutes of study today.")
        else:
            messages.append(f"🎓 Great job studying {insights['total_topics']} topics!")
            
        # Progress-based encouragement
        if insights['mastered_topics'] > 0:
            messages.append(f"🏆 Congratulations! You've mastered {insights['mastered_topics']} topic(s)!")
        
        if insights['study_time_hours'] > 0:
            messages.append(f"⏰ You've invested {insights['study_time_hours']} hours in learning - time well spent!")
        
        # Consistency encouragement
        consistency_messages = {
            "Very Active": "🔥 You're on fire! Your consistency is excellent!",
            "Consistent": "✅ Your regular study habits are paying off!",
            "Moderate": "📈 Try to study a bit more regularly for better results!",
            "Inactive": "🚀 Let's get back on track! Start with just 10 minutes today.",
            "No activity": "🌱 Every journey begins with a single step. Start today!"
        }
        
        messages.append(consistency_messages.get(insights['learning_consistency'], "Keep going!"))
        
        # Struggling topics support
        if insights['struggling_topics']:
            messages.append(f"💡 Don't worry about {', '.join(insights['struggling_topics'])} - difficulty is temporary, giving up lasts forever!")
        
        # Motivational tips
        tips = [
            "🧠 Remember: Your brain grows stronger with every challenge!",
            "📚 Break complex topics into smaller, manageable chunks.",
            "🎯 Set specific, achievable goals for each study session.",
            "🔄 Regular review is more effective than cramming.",
            "💭 Teach others what you learn - it reinforces your knowledge!"
        ]
        
        messages.append(random.choice(tips))
        
        return "\n".join(messages)
    
    def optimize_study_techniques(self, topic: str = None):
        """Get study technique recommendations"""
        learning_style = self.user_profile.profile.get('learning_style', 'visual')
        time_available = self.user_profile.profile.get('time_availability', 30)
        
        techniques = []
        techniques.append("🎯 STUDY TECHNIQUE OPTIMIZATION")
        techniques.append("=" * 50)
        techniques.append(f"👤 Your Learning Style: {learning_style}")
        techniques.append(f"⏰ Available Time: {time_available} minutes/day")
        if topic:
            techniques.append(f"🎯 Focus Topic: {topic}")
        
        # Style-specific techniques
        style_techniques = {
            "visual": {
                "primary": ["Mind Mapping", "Flashcards", "Diagrams", "Color Coding"],
                "description": "Visual learners benefit from seeing information organized and color-coded."
            },
            "auditory": {
                "primary": ["Read Aloud", "Audio Recordings", "Discussion", "Verbal Repetition"],
                "description": "Auditory learners excel when they hear and speak information."
            },
            "kinesthetic": {
                "primary": ["Hands-on Practice", "Note-taking", "Movement", "Real Examples"],
                "description": "Kinesthetic learners need to actively engage with material."
            },
            "reading": {
                "primary": ["Cornell Notes", "Summarization", "Outlining", "Text Analysis"],
                "description": "Reading/writing learners prefer text-based methods."
            }
        }
        
        style_info = style_techniques.get(learning_style, style_techniques["visual"])
        
        techniques.append(f"\n🎨 Recommended Techniques for {learning_style.title()} Learners:")
        techniques.append(f"📝 {style_info['description']}")
        
        for i, technique in enumerate(style_info["primary"], 1):
            techniques.append(f"  {i}. {technique}")
        
        # Universal techniques
        techniques.append(f"\n🌟 Universal Study Techniques:")
        techniques.append(f"• Spaced Repetition: Review at increasing intervals")
        techniques.append(f"• Active Recall: Test yourself without looking at notes")
        techniques.append(f"• Pomodoro Technique: Study in focused 25-minute blocks")
        techniques.append(f"• Elaborative Interrogation: Ask 'why' and 'how' questions")
        
        # Time-based recommendations
        if time_available < 30:
            techniques.append(f"\n⏰ Short Session Tips (under 30 min):")
            techniques.append(f"• Focus on one concept at a time")
            techniques.append(f"• Use quick review flashcards")
            techniques.append(f"• Practice active recall")
        else:
            techniques.append(f"\n⏰ Extended Session Tips (30+ min):")
            techniques.append(f"• Combine multiple techniques")
            techniques.append(f"• Include breaks every 25-30 minutes")
            techniques.append(f"• Mix review and new material")
        
        return "\n".join(techniques)
    
    def record_quiz_result(self, topic: str, score: float, time_spent: int = 15):
        """Record quiz results and update user progress"""
        self.user_profile.record_activity(topic, score, time_spent)
        print(f"✅ Recorded quiz result: {score}% for {topic}")
        print(f"📊 Updated mastery level: {self.user_profile.progress['mastery_levels'].get(topic, 'beginner')}")
    
    def update_profile(self, **kwargs):
        """Update user profile"""
        self.user_profile.update_profile(**kwargs)
        print("✅ Profile updated successfully!")

def main():
    """Main function for the simple learning buddy"""
    buddy = SimpleLearningBuddy()
    
    print("🤖 Learning Buddy System (Offline Mode)")
    print("📡 AI features are temporarily unavailable, using built-in learning tools.")
    print("This system will help you learn effectively with personalized content.")
    
    while True:
        print("\n" + "="*40)
        print("LEARNING BUDDY MENU")
        print("="*40)
        print("1. 📊 View Dashboard")
        print("2. 📝 Analyze Learning Progress")
        print("3. 💡 Get Topic Explanation")
        print("4. 🧠 Generate Quiz")
        print("5. 📅 Create Weekly Plan")
        print("6. 💪 Get Motivation Boost")
        print("7. 🎯 Optimize Study Techniques")
        print("8. ✏️ Update Profile")
        print("9. 📈 Record Quiz Result")
        print("0. Exit")
        
        try:
            choice = input("\nSelect an option (0-9): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye! Happy learning!")
            break
        
        if choice == "0":
            print("👋 Happy learning! See you next time!")
            break
        elif choice == "1":
            buddy.get_dashboard()
        elif choice == "2":
            topic = input("Enter topic to analyze (or press Enter for general): ").strip()
            result = buddy.analyze_progress(topic if topic else None)
            print(f"\n📊 PROGRESS ANALYSIS:\n{result}")
        elif choice == "3":
            topic = input("Enter topic: ").strip()
            concept = input("Enter concept to explain: ").strip()
            if topic and concept:
                result = buddy.generate_explanation(topic, concept)
                print(f"\n💡 EXPLANATION:\n{result}")
            else:
                print("❌ Please provide both topic and concept.")
        elif choice == "4":
            topic = input("Enter topic for quiz: ").strip()
            if topic:
                num_q = input("Number of questions (default 5): ").strip()
                num_questions = int(num_q) if num_q.isdigit() else 5
                result = buddy.generate_quiz(topic, num_questions)
                print(f"\n🧠 QUIZ:\n{result}")
            else:
                print("❌ Please provide a topic.")
        elif choice == "5":
            topics_input = input("Enter focus topics (comma-separated, or press Enter for auto): ").strip()
            topics = [t.strip() for t in topics_input.split(",")] if topics_input else None
            result = buddy.create_weekly_plan(topics)
            print(f"\n📅 WEEKLY PLAN:\n{result}")
        elif choice == "6":
            result = buddy.get_motivation_boost()
            print(f"\n💪 MOTIVATION BOOST:\n{result}")
        elif choice == "7":
            topic = input("Enter topic for optimization (or press Enter for general): ").strip()
            result = buddy.optimize_study_techniques(topic if topic else None)
            print(f"\n🎯 STUDY OPTIMIZATION:\n{result}")
        elif choice == "8":
            print("\n✏️ UPDATE PROFILE")
            style = input("Learning style (visual/auditory/kinesthetic/reading): ").strip().lower()
            if style in ["visual", "auditory", "kinesthetic", "reading"]:
                buddy.user_profile.update_profile(learning_style=style)
            
            exp_style = input("Explanation style (simple/detailed/analogies/examples): ").strip().lower()
            if exp_style in ["simple", "detailed", "analogies", "examples"]:
                buddy.user_profile.update_profile(preferred_explanation_style=exp_style)
            
            time_str = input("Daily study time in minutes: ").strip()
            if time_str.isdigit():
                buddy.user_profile.update_profile(time_availability=int(time_str))
            
            print("✅ Profile updated!")
        elif choice == "9":
            topic = input("Enter topic: ").strip()
            score_str = input("Enter quiz score (0-100): ").strip()
            time_str = input("Time spent in minutes (default 15): ").strip()
            
            if topic and score_str.replace('.', '').isdigit():
                score = float(score_str)
                time_spent = int(time_str) if time_str.isdigit() else 15
                buddy.record_quiz_result(topic, score, time_spent)
            else:
                print("❌ Please provide valid topic and score.")
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()

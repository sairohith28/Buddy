from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, LLM
from user_profile import UserProfile
from interactive_quiz import InteractiveQuiz
import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Initialize LLM with GROQ
llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)

class LearningBuddySystem:
    def __init__(self, user_id: str = "default_user"):
        self.user_profile = UserProfile(user_id)
        self.quiz_system = InteractiveQuiz(self.user_profile)
        self.setup_agents()
    
    def setup_agents(self):
        """Setup all the specialized agents"""
        
        # 1. Learning Analyzer Agent
        self.learning_analyzer = Agent(
            role="Learning Progress Analyzer",
            goal="Analyze user's learning progress, identify strengths, weaknesses, and patterns to optimize learning path",
            backstory="""You are an expert educational data analyst who specializes in understanding 
            individual learning patterns. You analyze quiz scores, study time, topic mastery levels, 
            and learning consistency to provide insights that help optimize the learning experience. 
            You identify which topics need more attention and which learning strategies work best for each user.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 2. Content Personalizer Agent
        self.content_personalizer = Agent(
            role="Content Personalization Specialist",
            goal="Adapt learning content to match user's learning style, preferences, and current skill level",
            backstory="""You are a master educator who excels at personalizing content delivery. 
            You understand different learning styles (visual, auditory, kinesthetic, reading/writing) 
            and can adapt explanations accordingly. You know when to use simple explanations, detailed 
            analysis, analogies, or real-world examples based on user preferences and comprehension levels.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 3. Quiz Generator Agent
        self.quiz_generator = Agent(
            role="Adaptive Quiz Creator",
            goal="Generate personalized quizzes that adapt to user's knowledge level and learning progress",
            backstory="""You are an expert assessment designer who creates engaging and effective quizzes. 
            You understand how to craft questions at appropriate difficulty levels, provide meaningful 
            feedback, and design assessments that reinforce learning. You adapt question types and 
            complexity based on user performance and mastery levels.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 4. Learning Path Planner Agent
        self.learning_planner = Agent(
            role="Adaptive Learning Path Designer",
            goal="Create and adjust weekly learning plans based on user goals, progress, and available time",
            backstory="""You are an educational strategist who designs optimal learning journeys. 
            You understand how to sequence topics, balance difficulty progression, and respect time 
            constraints. You create realistic, achievable learning plans that adapt based on user 
            progress and changing circumstances.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 5. Motivational Coach Agent
        self.motivational_coach = Agent(
            role="Learning Motivation Coach",
            goal="Provide encouragement, track achievements, and maintain user engagement in learning",
            backstory="""You are an enthusiastic learning coach who excels at keeping learners motivated. 
            You celebrate achievements, provide constructive feedback for struggles, set realistic goals, 
            and help users build sustainable learning habits. You understand the psychology of learning 
            and know how to maintain long-term engagement.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 6. Study Technique Advisor Agent
        self.study_advisor = Agent(
            role="Study Technique Optimization Specialist",
            goal="Recommend and optimize study techniques based on user performance and learning patterns",
            backstory="""You are a learning science expert who knows the most effective study techniques 
            for different types of content and learners. You understand spaced repetition, active recall, 
            elaborative interrogation, and other evidence-based learning strategies. You recommend the 
            best techniques for each user's situation and learning goals.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
    
    def analyze_progress(self, topic: str = None):
        """Analyze user's learning progress"""
        user_data = {
            "profile": self.user_profile.profile,
            "progress": self.user_profile.progress,
            "insights": self.user_profile.get_learning_insights(),
            "focus_topic": topic
        }
        
        analysis_task = Task(
            description=f"""Analyze the user's learning progress and patterns:
            
            User Profile: {json.dumps(user_data['profile'], indent=2)}
            Progress Data: {json.dumps(user_data['progress'], indent=2)}
            Learning Insights: {json.dumps(user_data['insights'], indent=2)}
            Focus Topic: {topic or 'General Analysis'}
            
            Provide detailed analysis including:
            1. Current learning status and trends
            2. Strengths and areas needing improvement
            3. Learning pattern insights
            4. Recommendations for optimization
            5. Specific concerns or red flags
            """,
            agent=self.learning_analyzer,
            expected_output="Comprehensive learning progress analysis with actionable insights"
        )
        
        crew = Crew(
            agents=[self.learning_analyzer],
            tasks=[analysis_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def get_simple_explanation(self, topic: str, concept: str):
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
    
    def generate_personalized_explanation(self, topic: str, concept: str):
        """Generate personalized explanation for a concept with fallback"""
        try:
            user_style = self.user_profile.profile.get("preferred_explanation_style", "simple")
            learning_style = self.user_profile.profile.get("learning_style", "visual")
            mastery_level = self.user_profile.progress.get("mastery_levels", {}).get(topic, "beginner")
            
            explanation_task = Task(
                description=f"""Create a personalized explanation for the concept '{concept}' in the topic '{topic}':
                
                User Preferences:
                - Learning Style: {learning_style}
                - Explanation Style: {user_style}
                - Current Mastery Level: {mastery_level}
                - Time Availability: {self.user_profile.profile.get('time_availability', 30)} minutes
                
                Requirements:
                1. Adapt explanation to {learning_style} learning style
                2. Use {user_style} explanation approach
                3. Match complexity to {mastery_level} level
                4. Include practical examples and applications
                5. Suggest follow-up activities or practice
                
                Make it engaging and easy to understand while being comprehensive.
                """,
                agent=self.content_personalizer,
                expected_output="Personalized, engaging explanation tailored to user's learning style and level"
            )
            
            crew = Crew(
                agents=[self.content_personalizer],
                tasks=[explanation_task],
                verbose=False
            )
            
            result = crew.kickoff()
            return result
            
        except Exception as e:
            print(f"⚠️  AI explanation temporarily unavailable. Using simple explanation mode...")
            return self.get_simple_explanation(topic, concept)
    
    def generate_adaptive_quiz(self, topic: str, num_questions: int = 5):
        """Generate adaptive quiz based on user's level"""
        mastery_level = self.user_profile.progress.get("mastery_levels", {}).get(topic, "beginner")
        recent_scores = self.user_profile.progress.get("quiz_scores", {}).get(topic, [])
        
        quiz_task = Task(
            description=f"""Generate an adaptive quiz for topic '{topic}':
            
            User Context:
            - Current Mastery Level: {mastery_level}
            - Recent Quiz Performance: {recent_scores[-3:] if recent_scores else 'No previous attempts'}
            - Learning Style: {self.user_profile.profile.get('learning_style', 'visual')}
            
            Quiz Requirements:
            1. Create {num_questions} questions appropriate for {mastery_level} level
            2. Include mix of question types (multiple choice, true/false, short answer)
            3. Gradually increase difficulty if user is performing well
            4. Focus on weak areas identified from recent performance
            5. Provide detailed explanations for each answer
            6. Include hints for struggling learners
            
            Format as JSON with questions, options, correct answers, and explanations.
            """,
            agent=self.quiz_generator,
            expected_output="Adaptive quiz in JSON format with questions, answers, and detailed explanations"
        )
        
        crew = Crew(
            agents=[self.quiz_generator],
            tasks=[quiz_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Save quiz for later reference
        quiz_file = f"quizzes/{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            # Try to parse and save the quiz
            quiz_data = json.loads(str(result))
            with open(quiz_file, 'w') as f:
                json.dump(quiz_data, f, indent=2)
        except:
            # If parsing fails, save as text
            with open(quiz_file.replace('.json', '.txt'), 'w') as f:
                f.write(str(result))
        
        return result
    
    def create_weekly_plan(self, focus_topics: List[str] = None):
        """Create personalized weekly learning plan"""
        if focus_topics is None:
            focus_topics = self.user_profile.progress.get("current_topics", [])[:3]
        
        planning_task = Task(
            description=f"""Create a personalized weekly learning plan:
            
            User Profile:
            - Daily Time Available: {self.user_profile.profile.get('time_availability', 30)} minutes
            - Learning Style: {self.user_profile.profile.get('learning_style', 'visual')}
            - Current Topics: {focus_topics}
            - Learning Consistency: {self.user_profile.get_learning_insights()['learning_consistency']}
            - Struggling Topics: {self.user_profile.get_learning_insights()['struggling_topics']}
            
            Plan Requirements:
            1. Distribute study time across 7 days
            2. Balance between review and new content
            3. Include specific activities (reading, practice, quizzes)
            4. Account for varying energy levels throughout week
            5. Include rest days and flexibility
            6. Set specific, measurable goals for each day
            7. Suggest optimal study techniques for each session
            
            Make it realistic and achievable while challenging.
            """,
            agent=self.learning_planner,
            expected_output="Detailed 7-day learning plan with daily activities, goals, and study techniques"
        )
        
        crew = Crew(
            agents=[self.learning_planner],
            tasks=[planning_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Save plan
        plan_file = f"learning_data/weekly_plan_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(plan_file, 'w') as f:
            f.write(str(result))
        
        return result
    
    def get_simple_motivation_boost(self):
        """Get simple motivational message without LLM (fallback)"""
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
    
    def get_motivation_boost(self):
        """Get motivational message and encouragement with fallback"""
        try:
            # Try AI-powered motivation first
            insights = self.user_profile.get_learning_insights()
            
            motivation_task = Task(
                description=f"""Provide personalized motivation and encouragement:
                
                User's Learning Journey:
                - Total Topics Studying: {insights['total_topics']}
                - Mastered Topics: {insights['mastered_topics']}
                - Study Time: {insights['study_time_hours']} hours
                - Learning Consistency: {insights['learning_consistency']}
                - Current Challenges: {insights['struggling_topics']}
                
                Motivation Requirements:
                1. Acknowledge their progress and achievements
                2. Address any struggles with empathy and solutions
                3. Set encouraging but realistic next steps
                4. Provide specific praise for improvements
                5. Share relevant learning tips or techniques
                6. Boost confidence while maintaining growth mindset
                
                Be genuine, encouraging, and personalized to their journey.
                """,
                agent=self.motivational_coach,
                expected_output="Personalized motivational message with specific encouragement and next steps"
            )
            
            crew = Crew(
                agents=[self.motivational_coach],
                tasks=[motivation_task],
                verbose=False  # Reduce verbosity to avoid hanging
            )
            
            # Set a timeout for the crew execution
            result = crew.kickoff()
            return result
            
        except Exception as e:
            print(f"⚠️  AI motivation temporarily unavailable. Using simple motivation mode...")
            return self.get_simple_motivation_boost()
    
    def optimize_study_techniques(self, topic: str = None):
        """Get personalized study technique recommendations"""
        user_performance = self.user_profile.progress.get("mastery_levels", {})
        struggling_topics = [t for t, level in user_performance.items() if level == "struggling"]
        
        optimization_task = Task(
            description=f"""Recommend optimized study techniques:
            
            User Context:
            - Learning Style: {self.user_profile.profile.get('learning_style', 'visual')}
            - Time Availability: {self.user_profile.profile.get('time_availability', 30)} minutes/day
            - Focus Topic: {topic or 'General Study Optimization'}
            - Struggling Areas: {struggling_topics}
            - Current Performance: {user_performance}
            
            Recommendations Needed:
            1. Specific study techniques for their learning style
            2. Time management strategies for available time
            3. Methods to improve retention and recall
            4. Techniques specifically for struggling topics
            5. Active learning strategies
            6. Memory enhancement techniques
            7. Progress tracking methods
            
            Provide practical, actionable techniques with implementation steps.
            """,
            agent=self.study_advisor,
            expected_output="Comprehensive study technique recommendations with implementation guidance"
        )
        
        crew = Crew(
            agents=[self.study_advisor],
            tasks=[optimization_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def record_quiz_result(self, topic: str, score: float, time_spent: int = 15):
        """Record quiz results and update user progress"""
        self.user_profile.record_activity(topic, score, time_spent)
        print(f"✅ Recorded quiz result: {score}% for {topic}")
        print(f"📊 Updated mastery level: {self.user_profile.progress['mastery_levels'].get(topic, 'beginner')}")
    
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
    
    def get_simple_progress_analysis(self, topic: str = None):
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
    
    def analyze_progress(self, topic: str = None):
        """Analyze user's learning progress with fallback"""
        try:
            user_data = {
                "profile": self.user_profile.profile,
                "progress": self.user_profile.progress,
                "insights": self.user_profile.get_learning_insights(),
                "focus_topic": topic
            }
            
            analysis_task = Task(
                description=f"""Analyze the user's learning progress and patterns:
                
                User Profile: {json.dumps(user_data['profile'], indent=2)}
                Progress Data: {json.dumps(user_data['progress'], indent=2)}
                Learning Insights: {json.dumps(user_data['insights'], indent=2)}
                Focus Topic: {topic or 'General Analysis'}
                
                Provide detailed analysis including:
                1. Current learning status and trends
                2. Strengths and areas needing improvement
                3. Learning pattern insights
                4. Recommendations for optimization
                5. Specific concerns or red flags
                """,
                agent=self.learning_analyzer,
                expected_output="Comprehensive learning progress analysis with actionable insights"
            )
            
            crew = Crew(
                agents=[self.learning_analyzer],
                tasks=[analysis_task],
                verbose=False
            )
            
            result = crew.kickoff()
            return result
            
        except Exception as e:
            print(f"⚠️  AI analysis temporarily unavailable. Using simple analysis mode...")
            return self.get_simple_progress_analysis(topic)
    
    # ...existing code...

# Example usage and testing functions
def main():
    """Main function to demonstrate the Learning Buddy System"""
    buddy = LearningBuddySystem()
    
    print("🤖 Welcome to your Hyper-Personalized Learning Buddy!")
    print("This AI system will help you learn more effectively with personalized content.")
    
    while True:
        print("\n" + "="*40)
        print("LEARNING BUDDY MENU")
        print("="*40)
        print("1. 📊 View Dashboard")
        print("2. 📝 Analyze Learning Progress")
        print("3. 💡 Get Topic Explanation")
        print("4. 🧠 Take Adaptive Quiz")
        print("5. 📅 Create Weekly Plan")
        print("6. 💪 Get Motivation Boost")
        print("7. 🎯 Optimize Study Techniques")
        print("8. ✏️ Update Profile")
        print("9. 📈 Record Quiz Result")
        print("0. Exit")
        
        choice = input("\nSelect an option (0-9): ").strip()
        
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
                result = buddy.generate_personalized_explanation(topic, concept)
                print(f"\n💡 PERSONALIZED EXPLANATION:\n{result}")
        elif choice == "4":
            topic = input("Enter topic for quiz: ").strip()
            if topic:
                num_q = input("Number of questions (default 5): ").strip()
                num_questions = int(num_q) if num_q.isdigit() else 5
                result = buddy.generate_adaptive_quiz(topic, num_questions)
                print(f"\n🧠 ADAPTIVE QUIZ:\n{result}")
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
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()

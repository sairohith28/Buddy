#!/usr/bin/env python3
"""
Demo and Testing Script for Learning Buddy System
Demonstrates all features with sample data
"""

from learning_buddy import LearningBuddySystem
from learning_analytics import LearningAnalytics
import random

def demo_learning_buddy():
    """Demonstrate the Learning Buddy System capabilities"""
    print("🎓 LEARNING BUDDY SYSTEM DEMO")
    print("=" * 50)
    
    # Initialize system
    buddy = LearningBuddySystem("demo_user")
    analytics = LearningAnalytics(buddy.user_profile)
    
    # Setup demo profile
    print("\n1. 👤 Setting up demo user profile...")
    buddy.user_profile.update_profile(
        learning_style="visual",
        preferred_explanation_style="analogies",
        time_availability=45,
        interests=["mathematics", "physics", "computer science"],
        goals=["Master calculus", "Understand quantum mechanics", "Learn machine learning"]
    )
    print("✅ Demo profile created!")
    
    # Record some demo progress
    print("\n2. 📊 Recording demo learning activities...")
    demo_activities = [
        ("Calculus", 85, 30),
        ("Physics", 72, 25),
        ("Machine Learning", 65, 40),
        ("Calculus", 88, 35),  # Improvement
        ("Physics", 78, 30),   # Improvement
        ("Machine Learning", 70, 45),  # Improvement
        ("Quantum Mechanics", 60, 20),  # New topic
        ("Linear Algebra", 75, 35),    # New topic
    ]
    
    for topic, score, time_spent in demo_activities:
        buddy.record_quiz_result(topic, score, time_spent)
    
    print("✅ Demo activities recorded!")
    
    # Show dashboard
    print("\n3. 📈 Current Learning Dashboard:")
    buddy.get_dashboard()
    
    # Demo feature: Progress Analysis
    print("\n4. 🔍 DEMO: Learning Progress Analysis")
    print("-" * 40)
    result = buddy.analyze_progress("Calculus")
    print(f"Analysis Result:\n{result}")
    
    # Demo feature: Personalized Explanation
    print("\n5. 💡 DEMO: Personalized Explanation")
    print("-" * 40)
    result = buddy.generate_personalized_explanation("Calculus", "derivatives")
    print(f"Explanation:\n{result}")
    
    # Demo feature: Adaptive Quiz
    print("\n6. 🧠 DEMO: Adaptive Quiz Generation")
    print("-" * 40)
    result = buddy.generate_adaptive_quiz("Physics", 3)
    print(f"Generated Quiz:\n{result}")
    
    # Demo feature: Weekly Plan
    print("\n7. 📅 DEMO: Weekly Learning Plan")
    print("-" * 40)
    result = buddy.create_weekly_plan(["Calculus", "Physics", "Machine Learning"])
    print(f"Weekly Plan:\n{result}")
    
    # Demo feature: Motivation
    print("\n8. 💪 DEMO: Motivation Boost")
    print("-" * 40)
    result = buddy.get_motivation_boost()
    print(f"Motivation:\n{result}")
    
    # Demo feature: Study Optimization
    print("\n9. 🎯 DEMO: Study Technique Optimization")
    print("-" * 40)
    result = buddy.optimize_study_techniques("Machine Learning")
    print(f"Study Techniques:\n{result}")
    
    # Demo feature: Advanced Analytics
    print("\n10. 📊 DEMO: Advanced Learning Analytics")
    print("-" * 40)
    report = analytics.generate_learning_report()
    
    print("LEARNING ANALYTICS REPORT:")
    print(f"📚 Total Topics: {report['learning_summary']['total_topics']}")
    print(f"🎯 Average Score: {report['learning_summary']['average_score']}%")
    print(f"⏱️ Study Time: {report['learning_summary']['study_time_hours']} hours")
    print(f"🏆 Achievements: {len(report['achievements'])}")
    
    if report['achievements']:
        print("\n🎉 Your Achievements:")
        for achievement in report['achievements']:
            print(f"  ✨ {achievement}")
    
    if report['recommendations']:
        print("\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"  📌 {rec}")
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETE!")
    print("Run 'python learning_buddy.py' to start interactive mode")
    print("=" * 50)

def performance_test():
    """Test system performance with multiple users"""
    print("\n🔬 PERFORMANCE TEST")
    print("-" * 30)
    
    # Test multiple user profiles
    users = ["alice", "bob", "charlie"]
    learning_styles = ["visual", "auditory", "kinesthetic"]
    
    for i, user in enumerate(users):
        print(f"\nTesting user: {user}")
        buddy = LearningBuddySystem(user)
        
        # Setup unique profile
        buddy.user_profile.update_profile(
            learning_style=learning_styles[i],
            time_availability=random.randint(20, 60)
        )
        
        # Record some activities
        for _ in range(3):
            topic = random.choice(["Math", "Science", "History"])
            score = random.randint(60, 95)
            buddy.record_quiz_result(topic, score)
        
        # Test analysis
        try:
            result = buddy.analyze_progress()
            print(f"  ✅ Analysis successful for {user}")
        except Exception as e:
            print(f"  ❌ Analysis failed for {user}: {e}")
    
    print("\n✅ Performance test complete!")

def interactive_demo():
    """Interactive demo mode"""
    print("\n🎮 INTERACTIVE DEMO MODE")
    print("Try out different features step by step!")
    
    buddy = LearningBuddySystem("interactive_user")
    
    while True:
        print("\n" + "="*30)
        print("QUICK DEMO OPTIONS")
        print("="*30)
        print("1. 🎯 Quick Progress Analysis")
        print("2. 💡 Get Explanation (Python)")
        print("3. 🧠 Generate Quiz (Mathematics)")
        print("4. 📅 Create Study Plan")
        print("5. 💪 Motivation Message")
        print("6. 📊 View Dashboard")
        print("0. Exit Demo")
        
        choice = input("\nSelect demo option (0-6): ").strip()
        
        if choice == "0":
            print("👋 Demo complete!")
            break
        elif choice == "1":
            print("\n🎯 Running progress analysis...")
            result = buddy.analyze_progress()
            print(f"Result: {str(result)[:500]}...")
        elif choice == "2":
            print("\n💡 Generating explanation for Python loops...")
            result = buddy.generate_personalized_explanation("Python", "for loops")
            print(f"Explanation: {str(result)[:500]}...")
        elif choice == "3":
            print("\n🧠 Creating mathematics quiz...")
            result = buddy.generate_adaptive_quiz("Mathematics", 3)
            print(f"Quiz: {str(result)[:500]}...")
        elif choice == "4":
            print("\n📅 Creating study plan...")
            result = buddy.create_weekly_plan(["Python", "Mathematics"])
            print(f"Plan: {str(result)[:500]}...")
        elif choice == "5":
            print("\n💪 Getting motivation boost...")
            result = buddy.get_motivation_boost()
            print(f"Motivation: {str(result)[:500]}...")
        elif choice == "6":
            buddy.get_dashboard()
        else:
            print("❌ Invalid option!")

def main():
    """Main demo function"""
    print("🚀 LEARNING BUDDY SYSTEM - DEMO & TEST SUITE")
    print("=" * 60)
    print("Choose demo mode:")
    print("1. 🎬 Full Feature Demo")
    print("2. 🔬 Performance Test")
    print("3. 🎮 Interactive Demo")
    print("4. 🚀 Start Main Application")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        demo_learning_buddy()
    elif choice == "2":
        performance_test()
    elif choice == "3":
        interactive_demo()
    elif choice == "4":
        from learning_buddy import main as main_app
        main_app()
    else:
        print("❌ Invalid choice. Running full demo...")
        demo_learning_buddy()

if __name__ == "__main__":
    main()

import json
import os
from datetime import datetime
from typing import Dict, List

class LearningAnalytics:
    """Advanced analytics for learning patterns and insights"""
    
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.analytics_file = f"reports/analytics_{user_profile.user_id}.json"
        
    def generate_learning_report(self) -> Dict:
        """Generate comprehensive learning analytics report"""
        progress = self.user_profile.progress
        profile = self.user_profile.profile
        
        report = {
            "user_id": self.user_profile.user_id,
            "generated_at": datetime.now().isoformat(),
            "learning_summary": self._get_learning_summary(),
            "performance_analysis": self._analyze_performance(),
            "time_analysis": self._analyze_time_patterns(),
            "difficulty_progression": self._track_difficulty_progression(),
            "recommendations": self._generate_recommendations(),
            "achievements": self._identify_achievements()
        }
        
        # Save report
        os.makedirs("reports", exist_ok=True)
        with open(self.analytics_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _get_learning_summary(self) -> Dict:
        """Get high-level learning summary"""
        progress = self.user_profile.progress
        
        total_quizzes = sum(len(scores) for scores in progress.get("quiz_scores", {}).values())
        avg_score = 0
        if total_quizzes > 0:
            all_scores = []
            for topic_scores in progress.get("quiz_scores", {}).values():
                all_scores.extend([s["score"] for s in topic_scores])
            avg_score = sum(all_scores) / len(all_scores)
        
        return {
            "total_topics": len(progress.get("current_topics", [])),
            "total_quizzes_taken": total_quizzes,
            "average_score": round(avg_score, 2),
            "study_time_hours": round(progress.get("total_study_time", 0) / 60, 2),
            "learning_streak": progress.get("learning_streaks", 0),
            "mastery_distribution": self._get_mastery_distribution()
        }
    
    def _get_mastery_distribution(self) -> Dict:
        """Get distribution of mastery levels"""
        mastery_levels = self.user_profile.progress.get("mastery_levels", {})
        distribution = {"advanced": 0, "intermediate": 0, "beginner": 0, "struggling": 0}
        
        for level in mastery_levels.values():
            if level in distribution:
                distribution[level] += 1
        
        return distribution
    
    def _analyze_performance(self) -> Dict:
        """Analyze performance trends"""
        quiz_scores = self.user_profile.progress.get("quiz_scores", {})
        
        performance_analysis = {
            "improving_topics": [],
            "declining_topics": [],
            "consistent_topics": [],
            "top_performing_topics": [],
            "struggling_topics": []
        }
        
        for topic, scores in quiz_scores.items():
            if len(scores) >= 3:
                recent_scores = [s["score"] for s in scores[-3:]]
                earlier_scores = [s["score"] for s in scores[:-3]] if len(scores) > 3 else []
                
                if earlier_scores:
                    recent_avg = sum(recent_scores) / len(recent_scores)
                    earlier_avg = sum(earlier_scores) / len(earlier_scores)
                    
                    if recent_avg > earlier_avg + 10:
                        performance_analysis["improving_topics"].append(topic)
                    elif recent_avg < earlier_avg - 10:
                        performance_analysis["declining_topics"].append(topic)
                    else:
                        performance_analysis["consistent_topics"].append(topic)
                
                # Overall performance classification
                overall_avg = sum(s["score"] for s in scores) / len(scores)
                if overall_avg >= 85:
                    performance_analysis["top_performing_topics"].append(topic)
                elif overall_avg < 60:
                    performance_analysis["struggling_topics"].append(topic)
        
        return performance_analysis
    
    def _analyze_time_patterns(self) -> Dict:
        """Analyze study time patterns"""
        return {
            "preferred_study_duration": self.user_profile.profile.get("time_availability", 30),
            "total_study_time": self.user_profile.progress.get("total_study_time", 0),
            "average_session_length": 15,  # Default assumption
            "consistency_rating": self.user_profile.calculate_consistency()
        }
    
    def _track_difficulty_progression(self) -> Dict:
        """Track how user progresses through difficulty levels"""
        mastery_levels = self.user_profile.progress.get("mastery_levels", {})
        
        progression = {
            "topics_mastered": len([t for t, l in mastery_levels.items() if l == "advanced"]),
            "topics_in_progress": len([t for t, l in mastery_levels.items() if l in ["intermediate", "beginner"]]),
            "topics_struggling": len([t for t, l in mastery_levels.items() if l == "struggling"])
        }
        
        return progression
    
    def _generate_recommendations(self) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        insights = self.user_profile.get_learning_insights()
        
        # Consistency recommendations
        if insights["learning_consistency"] == "Inactive":
            recommendations.append("Consider setting up daily study reminders to maintain consistency")
        elif insights["learning_consistency"] == "Moderate":
            recommendations.append("Try to increase study frequency to improve retention")
        
        # Performance recommendations
        if insights["struggling_topics"]:
            recommendations.append(f"Focus extra attention on: {', '.join(insights['struggling_topics'])}")
        
        # Time management
        if insights["study_time_hours"] < 5:
            recommendations.append("Consider increasing weekly study time for better progress")
        
        # Mastery recommendations
        if insights["mastered_topics"] == 0:
            recommendations.append("Set a goal to master at least one topic this week")
        
        return recommendations
    
    def _identify_achievements(self) -> List[str]:
        """Identify user achievements"""
        achievements = []
        insights = self.user_profile.get_learning_insights()
        
        if insights["mastered_topics"] > 0:
            achievements.append(f"Mastered {insights['mastered_topics']} topics!")
        
        if insights["study_time_hours"] >= 10:
            achievements.append(f"Logged {insights['study_time_hours']} hours of study time!")
        
        if insights["learning_consistency"] in ["Very Active", "Consistent"]:
            achievements.append("Maintaining excellent learning consistency!")
        
        if insights["total_topics"] >= 5:
            achievements.append(f"Actively learning {insights['total_topics']} topics!")
        
        return achievements

class StudyTechniques:
    """Collection of study techniques and recommendations"""
    
    @staticmethod
    def get_techniques_for_style(learning_style: str) -> List[Dict]:
        """Get study techniques based on learning style"""
        techniques = {
            "visual": [
                {"name": "Mind Mapping", "description": "Create visual diagrams connecting concepts"},
                {"name": "Flashcards", "description": "Use visual flashcards with images and colors"},
                {"name": "Concept Diagrams", "description": "Draw diagrams to represent relationships"},
                {"name": "Color Coding", "description": "Use different colors for different topics or concepts"}
            ],
            "auditory": [
                {"name": "Read Aloud", "description": "Read study materials out loud"},
                {"name": "Audio Recordings", "description": "Record yourself explaining concepts"},
                {"name": "Discussion Groups", "description": "Discuss topics with others"},
                {"name": "Music Mnemonics", "description": "Set information to music or rhythm"}
            ],
            "kinesthetic": [
                {"name": "Hands-on Practice", "description": "Practice with real-world examples"},
                {"name": "Walking Study", "description": "Study while walking or moving"},
                {"name": "Building Models", "description": "Create physical models of concepts"},
                {"name": "Active Note-taking", "description": "Use interactive note-taking methods"}
            ],
            "reading": [
                {"name": "Cornell Notes", "description": "Use structured note-taking system"},
                {"name": "Summarization", "description": "Write summaries after reading"},
                {"name": "Outline Creation", "description": "Create detailed outlines of topics"},
                {"name": "Text Annotation", "description": "Actively annotate reading materials"}
            ]
        }
        
        return techniques.get(learning_style, techniques["visual"])
    
    @staticmethod
    def get_retention_techniques() -> List[Dict]:
        """Get techniques specifically for retention"""
        return [
            {"name": "Spaced Repetition", "description": "Review material at increasing intervals"},
            {"name": "Active Recall", "description": "Test yourself without looking at notes"},
            {"name": "Elaborative Interrogation", "description": "Ask yourself 'why' and 'how' questions"},
            {"name": "Interleaving", "description": "Mix different topics in study sessions"},
            {"name": "Dual Coding", "description": "Combine verbal and visual information"}
        ]

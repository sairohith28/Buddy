import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class UserProfile:
    """Manages user learning profile and preferences"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.profile_file = f"user_profiles/{user_id}_profile.json"
        self.progress_file = f"user_profiles/{user_id}_progress.json"
        self.ensure_directories()
        self.profile = self.load_profile()
        self.progress = self.load_progress()
    
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        os.makedirs("user_profiles", exist_ok=True)
        os.makedirs("learning_data", exist_ok=True)
        os.makedirs("quizzes", exist_ok=True)
    
    def load_profile(self) -> Dict:
        """Load user profile from file"""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                return json.load(f)
        return {
            "user_id": self.user_id,
            "learning_style": "visual",  # visual, auditory, kinesthetic, reading
            "difficulty_preference": "intermediate",
            "interests": [],
            "goals": [],
            "time_availability": 30,  # minutes per day
            "preferred_explanation_style": "simple",  # simple, detailed, analogies, examples
            "strengths": [],
            "weaknesses": [],
            "created_at": datetime.now().isoformat()
        }
    
    def load_progress(self) -> Dict:
        """Load user progress from file"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            "topics_completed": [],
            "quiz_scores": {},
            "learning_streaks": 0,
            "total_study_time": 0,
            "last_activity": None,
            "current_topics": [],
            "mastery_levels": {}
        }
    
    def save_profile(self):
        """Save user profile to file"""
        with open(self.profile_file, 'w') as f:
            json.dump(self.profile, f, indent=2)
    
    def save_progress(self):
        """Save user progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def update_profile(self, **kwargs):
        """Update user profile"""
        self.profile.update(kwargs)
        self.save_profile()
    
    def record_activity(self, topic: str, score: float = None, study_time: int = 0):
        """Record learning activity"""
        self.progress["last_activity"] = datetime.now().isoformat()
        self.progress["total_study_time"] += study_time
        
        if topic not in self.progress["current_topics"]:
            self.progress["current_topics"].append(topic)
        
        if score is not None:
            if topic not in self.progress["quiz_scores"]:
                self.progress["quiz_scores"][topic] = []
            self.progress["quiz_scores"][topic].append({
                "score": score,
                "date": datetime.now().isoformat()
            })
            
            # Update mastery level based on recent scores
            recent_scores = self.progress["quiz_scores"][topic][-3:]  # Last 3 attempts
            avg_score = sum(s["score"] for s in recent_scores) / len(recent_scores)
            
            if avg_score >= 85:
                self.progress["mastery_levels"][topic] = "advanced"
            elif avg_score >= 70:
                self.progress["mastery_levels"][topic] = "intermediate"
            elif avg_score >= 50:
                self.progress["mastery_levels"][topic] = "beginner"
            else:
                self.progress["mastery_levels"][topic] = "struggling"
        
        self.save_progress()
    
    def get_learning_insights(self) -> Dict:
        """Get insights about user's learning patterns"""
        insights = {
            "total_topics": len(self.progress["current_topics"]),
            "mastered_topics": len([t for t, level in self.progress["mastery_levels"].items() if level == "advanced"]),
            "struggling_topics": [t for t, level in self.progress["mastery_levels"].items() if level == "struggling"],
            "study_time_hours": round(self.progress["total_study_time"] / 60, 2),
            "learning_consistency": self.calculate_consistency()
        }
        return insights
    
    def calculate_consistency(self) -> str:
        """Calculate learning consistency based on activity"""
        if not self.progress["last_activity"]:
            return "No activity"
        
        last_activity = datetime.fromisoformat(self.progress["last_activity"])
        days_since = (datetime.now() - last_activity).days
        
        if days_since == 0:
            return "Very Active"
        elif days_since <= 2:
            return "Consistent"
        elif days_since <= 7:
            return "Moderate"
        else:
            return "Inactive"

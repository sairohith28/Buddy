#!/usr/bin/env python3
"""
Setup script for Learning Buddy System
Installs required packages and sets up the environment
"""

import subprocess
import sys
import os

def install_packages():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please install manually:")
        print("pip install crewai python-dotenv groq")
        return False
    return True

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    directories = ["user_profiles", "learning_data", "quizzes", "reports"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ Created {directory}/")
    
    print("✅ Directories created successfully!")

def main():
    print("🎓 Learning Buddy System Setup")
    print("=" * 40)
    
    # Install packages
    if not install_packages():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check environment file
    if not os.path.exists(".env"):
        print("⚠️  .env file not found. Please ensure GROQ_API_KEY is set.")
    else:
        print("✅ Environment file found!")
    
    print("\n🚀 Setup complete! Run: python learning_buddy.py")

if __name__ == "__main__":
    main()

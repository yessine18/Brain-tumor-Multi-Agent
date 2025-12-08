"""
Quick Setup Script for Brain Tumor Analysis System
Run this after installing requirements
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required = [
        'flask',
        'tensorflow',
        'crewai',
        'langchain',
        'neo4j',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease run: pip install -r requirements.txt")
        return False
    
    print("✓ All required packages are installed")
    return True


def check_directories():
    """Ensure all required directories exist"""
    dirs = [
        'models',
        'uploads',
        'reports',
        'static/results',
        'templates'
    ]
    
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✓ All directories created")


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found")
        print("   Creating from .env.example...")
        
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ .env file created")
            print("⚠️  Please edit .env and add your API keys!")
            return False
        else:
            print("❌ .env.example not found")
            return False
    
    print("✓ .env file exists")
    return True


def check_model():
    """Check if trained model exists"""
    from config import Config
    config = Config()
    
    if not os.path.exists(config.MODEL_PATH):
        print(f"❌ Model not found at: {config.MODEL_PATH}")
        print("   Please copy your trained model file:")
        print(f"   Copy-Item best_modelVGG19_brain_tumor.keras {config.MODEL_PATH}")
        return False
    
    print("✓ Trained model found")
    return True


def test_neo4j_connection():
    """Test Neo4j connection"""
    try:
        from neo4j import GraphDatabase
        from config import Config
        
        config = Config()
        
        if not config.NEO4J_PASSWORD:
            print("⚠️  Neo4j password not set in .env")
            return False
        
        driver = GraphDatabase.driver(
            config.NEO4J_URI,
            auth=(config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
        )
        
        with driver.session() as session:
            session.run("RETURN 1")
        
        driver.close()
        print("✓ Neo4j connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Neo4j connection failed: {str(e)}")
        print("   Please ensure Neo4j is running and credentials are correct")
        return False


def initialize_knowledge_base():
    """Initialize the Neo4j knowledge base"""
    try:
        print("\nInitializing Neo4j knowledge base...")
        from agents.knowledge_base import get_knowledge_base
        from config import Config
        
        config = Config()
        kb = get_knowledge_base(
            config.NEO4J_URI,
            config.NEO4J_USERNAME,
            config.NEO4J_PASSWORD
        )
        
        kb.initialize_knowledge_base()
        print("✓ Knowledge base initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize knowledge base: {str(e)}")
        return False


def main():
    """Run all setup checks"""
    print("=" * 60)
    print("Brain Tumor Analysis System - Setup Check")
    print("=" * 60)
    print()
    
    steps = [
        ("Checking Python packages", check_requirements),
        ("Creating directories", check_directories),
        ("Checking environment file", check_env_file),
        ("Checking trained model", check_model),
    ]
    
    all_passed = True
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            all_passed = False
    
    # Optional: Test Neo4j
    print("\n" + "=" * 60)
    print("Optional: Neo4j Setup")
    print("=" * 60)
    
    neo4j_ok = test_neo4j_connection()
    
    if neo4j_ok:
        response = input("\nInitialize Neo4j knowledge base? (y/n): ")
        if response.lower() == 'y':
            initialize_knowledge_base()
    
    print("\n" + "=" * 60)
    print("Setup Summary")
    print("=" * 60)
    
    if all_passed and neo4j_ok:
        print("✓ All checks passed! You're ready to go!")
        print("\nTo start the application, run:")
        print("  python app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nRefer to README.md for detailed setup instructions.")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

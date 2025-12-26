"""
Configuration management for StoryWriterAgent
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

    # Server Configuration
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8036))

    # Story Configuration
    GENRES = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Children's"]
    TONES = ["Serious", "Funny", "Inspirational", "Dramatic"]
    LENGTHS = {
        "short": {"min": 100, "max": 300, "label": "Short (100-300 words)"},
        "medium": {"min": 300, "max": 600, "label": "Medium (300-600 words)"},
        "long": {"min": 600, "max": 1000, "label": "Long (600+ words)"}
    }
    LANGUAGES = ["English", "Urdu", "Arabic", "Spanish", "French", "German"]

    # Storage Configuration
    STORIES_DIR = os.getenv("STORIES_DIR", "stories")
    STORIES_FILE = os.path.join(STORIES_DIR, "stories.json")

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in .env file.")
        return True


# Example prompts for inspiration
EXAMPLE_PROMPTS = [
    "A dragon who wanted to become a chef",
    "A robot learning to love in a world without emotions",
    "A detective solving crimes in a haunted mansion",
    "Two strangers meeting on a train to nowhere",
    "A child discovering a magical door in their closet",
    "An astronaut finding signs of ancient civilization on Mars"
]

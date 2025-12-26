"""
Core story generation logic for StoryWriterAgent
"""
import json
import os
import uuid
from datetime import datetime
from typing import Optional, Generator
from openai import OpenAI
from config import Config


class StoryAgent:
    def __init__(self):
        Config.validate()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.stories = self._load_stories()

    def _load_stories(self) -> list:
        """Load stories from storage"""
        if os.path.exists(Config.STORIES_FILE):
            try:
                with open(Config.STORIES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_stories(self):
        """Save stories to storage"""
        os.makedirs(Config.STORIES_DIR, exist_ok=True)
        with open(Config.STORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.stories, f, ensure_ascii=False, indent=2)

    def _build_prompt(self, user_prompt: str, genre: str, tone: str,
                      length: str, language: str) -> str:
        """Build the story generation prompt"""
        length_info = Config.LENGTHS.get(length, Config.LENGTHS["medium"])

        system_prompt = f"""You are a creative story writer. Write an engaging {genre.lower()} story with a {tone.lower()} tone.

Guidelines:
- Write the story in {language}
- Target length: {length_info['min']}-{length_info['max']} words
- Create vivid characters and settings
- Include a clear beginning, middle, and end
- Make the story engaging and memorable
- Match the tone consistently throughout

User's story idea: {user_prompt}

Write the story now:"""

        return system_prompt

    def generate_story(self, prompt: str, genre: str = "Fantasy",
                       tone: str = "Serious", length: str = "medium",
                       language: str = "English") -> dict:
        """Generate a complete story"""
        full_prompt = self._build_prompt(prompt, genre, tone, length, language)

        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a creative story writer."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )

        story_content = response.choices[0].message.content

        story = {
            "id": str(uuid.uuid4()),
            "prompt": prompt,
            "content": story_content,
            "genre": genre,
            "tone": tone,
            "length": length,
            "language": language,
            "created_at": datetime.now().isoformat(),
            "favorite": False,
            "word_count": len(story_content.split())
        }

        self.stories.append(story)
        self._save_stories()

        return story

    def generate_story_stream(self, prompt: str, genre: str = "Fantasy",
                              tone: str = "Serious", length: str = "medium",
                              language: str = "English") -> Generator[str, None, dict]:
        """Generate a story with streaming for typewriter effect"""
        full_prompt = self._build_prompt(prompt, genre, tone, length, language)

        stream = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a creative story writer."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.8,
            max_tokens=2000,
            stream=True
        )

        story_content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                story_content += content
                yield content

        story = {
            "id": str(uuid.uuid4()),
            "prompt": prompt,
            "content": story_content,
            "genre": genre,
            "tone": tone,
            "length": length,
            "language": language,
            "created_at": datetime.now().isoformat(),
            "favorite": False,
            "word_count": len(story_content.split())
        }

        self.stories.append(story)
        self._save_stories()

        return story

    def get_all_stories(self) -> list:
        """Get all stories"""
        return sorted(self.stories, key=lambda x: x['created_at'], reverse=True)

    def get_story(self, story_id: str) -> Optional[dict]:
        """Get a specific story by ID"""
        for story in self.stories:
            if story['id'] == story_id:
                return story
        return None

    def delete_story(self, story_id: str) -> bool:
        """Delete a story by ID"""
        for i, story in enumerate(self.stories):
            if story['id'] == story_id:
                del self.stories[i]
                self._save_stories()
                return True
        return False

    def toggle_favorite(self, story_id: str) -> Optional[dict]:
        """Toggle favorite status of a story"""
        for story in self.stories:
            if story['id'] == story_id:
                story['favorite'] = not story['favorite']
                self._save_stories()
                return story
        return None

    def get_favorites(self) -> list:
        """Get all favorite stories"""
        return [s for s in self.stories if s.get('favorite', False)]

    def search_stories(self, query: str) -> list:
        """Search stories by content, prompt, or genre"""
        query = query.lower()
        results = []
        for story in self.stories:
            if (query in story['content'].lower() or
                query in story['prompt'].lower() or
                query in story['genre'].lower()):
                results.append(story)
        return sorted(results, key=lambda x: x['created_at'], reverse=True)

    def get_stats(self) -> dict:
        """Get writing statistics"""
        total_stories = len(self.stories)
        total_words = sum(s.get('word_count', 0) for s in self.stories)
        favorites_count = len(self.get_favorites())

        genre_counts = {}
        tone_counts = {}
        language_counts = {}

        for story in self.stories:
            genre = story.get('genre', 'Unknown')
            tone = story.get('tone', 'Unknown')
            language = story.get('language', 'Unknown')

            genre_counts[genre] = genre_counts.get(genre, 0) + 1
            tone_counts[tone] = tone_counts.get(tone, 0) + 1
            language_counts[language] = language_counts.get(language, 0) + 1

        return {
            "total_stories": total_stories,
            "total_words": total_words,
            "favorites": favorites_count,
            "average_words": total_words // total_stories if total_stories > 0 else 0,
            "genres": genre_counts,
            "tones": tone_counts,
            "languages": language_counts
        }

    def export_story(self, story_id: str, format: str = "txt") -> Optional[str]:
        """Export a story to a specific format"""
        story = self.get_story(story_id)
        if not story:
            return None

        if format == "txt":
            return f"""Title: Story by StoryWriterAgent
Genre: {story['genre']}
Tone: {story['tone']}
Language: {story['language']}
Created: {story['created_at']}
Prompt: {story['prompt']}

---

{story['content']}
"""
        elif format == "md":
            return f"""# Story by StoryWriterAgent

**Genre:** {story['genre']}
**Tone:** {story['tone']}
**Language:** {story['language']}
**Created:** {story['created_at']}

> *Prompt: {story['prompt']}*

---

{story['content']}
"""
        return None

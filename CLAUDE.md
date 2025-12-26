# StoryWriterAgent - Day 36 of #100DaysOfAI-Agents

## Project Overview

An AI-powered creative writing assistant that generates engaging short stories across multiple genres, tones, and languages. Built with OpenAI GPT-4 and FastAPI.

**Author:** Muhammad Sami
**GitHub:** https://github.com/muhammadsami987123/100DaysOfAI-Agents/tree/main/36_StoryWriterAgent

## Tech Stack

- Python 3.8+
- OpenAI GPT-4 API
- FastAPI web framework
- HTML/CSS/JavaScript frontend
- JSON for data persistence

## Key Files

- `story_agent.py` - Core story generation logic
- `web_app.py` - FastAPI web application
- `main.py` - Entry point (supports `--web`, `--terminal`, `--quick` modes)
- `config.py` - Configuration management
- `static/` - Frontend assets
- `templates/` - HTML templates

## Features

- **6 Genres:** Fantasy, Sci-Fi, Mystery, Romance, Horror, Children's
- **4 Tones:** Serious, Funny, Inspirational, Dramatic
- **3 Lengths:** Short (100-300 words), Medium (300-600), Long (600+)
- **6 Languages:** English, Urdu, Arabic, Spanish, French, German
- Story library with favorites, search, and export (TXT, Markdown)
- Typewriter animation effects
- Auto-save functionality

## Quick Start

```bash
# Web interface (recommended)
python main.py --web
# Open: http://localhost:8036

# Terminal interface
python main.py --terminal

# Quick generation
python main.py --quick "A dragon who wanted to become a chef" --genre fantasy --tone funny
```

## API Endpoints

- `POST /generate` - Create new stories
- `GET /stories` - Retrieve story collection
- `GET /stories/{id}` - Get specific story
- `POST /stories/{id}/favorite` - Mark as favorite
- `DELETE /stories/{id}` - Remove story
- `GET /search` - Query stories

## Environment Setup

Requires `OPENAI_API_KEY` in `.env` file.

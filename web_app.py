"""
FastAPI web application for StoryWriterAgent
"""
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json

from config import Config, EXAMPLE_PROMPTS
from story_agent import StoryAgent

app = FastAPI(title="StoryWriterAgent", version="1.0.0")

# CORS middleware for Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Initialize story agent
story_agent = None


def get_agent():
    global story_agent
    if story_agent is None:
        story_agent = StoryAgent()
    return story_agent


class StoryRequest(BaseModel):
    prompt: str
    genre: str = "Fantasy"
    tone: str = "Serious"
    length: str = "medium"
    language: str = "English"
    stream: bool = False


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "genres": Config.GENRES,
        "tones": Config.TONES,
        "lengths": Config.LENGTHS,
        "languages": Config.LANGUAGES,
        "examples": EXAMPLE_PROMPTS
    })


@app.post("/generate")
async def generate_story(request: StoryRequest):
    """Generate a new story"""
    agent = get_agent()

    if request.stream:
        async def stream_generator():
            for chunk in agent.generate_story_stream(
                prompt=request.prompt,
                genre=request.genre,
                tone=request.tone,
                length=request.length,
                language=request.language
            ):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream"
        )

    story = agent.generate_story(
        prompt=request.prompt,
        genre=request.genre,
        tone=request.tone,
        length=request.length,
        language=request.language
    )
    return JSONResponse(story)


@app.get("/stories")
async def get_stories():
    """Get all stories"""
    agent = get_agent()
    return JSONResponse(agent.get_all_stories())


@app.get("/stories/{story_id}")
async def get_story(story_id: str):
    """Get a specific story"""
    agent = get_agent()
    story = agent.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return JSONResponse(story)


@app.delete("/stories/{story_id}")
async def delete_story(story_id: str):
    """Delete a story"""
    agent = get_agent()
    if agent.delete_story(story_id):
        return JSONResponse({"status": "deleted"})
    raise HTTPException(status_code=404, detail="Story not found")


@app.post("/stories/{story_id}/favorite")
async def toggle_favorite(story_id: str):
    """Toggle favorite status"""
    agent = get_agent()
    story = agent.toggle_favorite(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return JSONResponse(story)


@app.get("/favorites")
async def get_favorites():
    """Get favorite stories"""
    agent = get_agent()
    return JSONResponse(agent.get_favorites())


@app.get("/search")
async def search_stories(q: str):
    """Search stories"""
    agent = get_agent()
    return JSONResponse(agent.search_stories(q))


@app.get("/stats")
async def get_stats():
    """Get writing statistics"""
    agent = get_agent()
    return JSONResponse(agent.get_stats())


@app.get("/export/{story_id}")
async def export_story(story_id: str, format: str = "txt"):
    """Export a story"""
    agent = get_agent()
    content = agent.export_story(story_id, format)
    if not content:
        raise HTTPException(status_code=404, detail="Story not found")

    media_type = "text/plain" if format == "txt" else "text/markdown"
    filename = f"story_{story_id[:8]}.{format}"

    return StreamingResponse(
        iter([content]),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/config")
async def get_config():
    """Get configuration options"""
    return JSONResponse({
        "genres": Config.GENRES,
        "tones": Config.TONES,
        "lengths": Config.LENGTHS,
        "languages": Config.LANGUAGES,
        "examples": EXAMPLE_PROMPTS
    })


def run_server():
    """Run the web server"""
    import uvicorn
    print(f"\n{'='*50}")
    print("  StoryWriterAgent - Web Interface")
    print(f"{'='*50}")
    print(f"\n  Open: http://{Config.HOST}:{Config.PORT}")
    print(f"\n  Press Ctrl+C to stop the server\n")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)


if __name__ == "__main__":
    run_server()

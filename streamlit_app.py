"""
StoryWriterAgent - Streamlit App
Day 36 of #100DaysOfAI-Agents
Author: Muhammad Sami
"""
import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="StoryWriterAgent - AI Story Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400&display=swap');

    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border-radius: 1rem;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
    }

    .story-content {
        font-family: 'Merriweather', serif;
        font-size: 1.1rem;
        line-height: 2;
        padding: 2rem;
        background: #1a1a2e;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
    }

    .story-content p:first-of-type::first-letter {
        font-size: 3rem;
        float: left;
        line-height: 1;
        padding-right: 0.5rem;
        color: #6366f1;
        font-weight: 700;
    }

    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid #6366f1;
        border-radius: 2rem;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .stats-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4a 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid #3a3a5a;
    }

    .stats-card h3 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .story-card {
        background: #1a1a2e;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }

    .story-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
    }

    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #2a2a4a;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
GENRES = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Children's", "Success", "Struggle", "Adventure", "Thriller", "Comedy", "Drama"]
TONES = ["Serious", "Funny", "Inspirational", "Dramatic"]
LENGTHS = {
    "Short (100-300 words)": (100, 300),
    "Medium (300-600 words)": (300, 600),
    "Long (600+ words)": (600, 1000)
}
LANGUAGES = ["English", "Urdu", "Arabic", "Spanish", "French", "German"]

EXAMPLE_PROMPTS = [
    "A dragon who wanted to become a chef",
    "A robot learning to love in a world without emotions",
    "A detective solving crimes in a haunted mansion",
    "Two strangers meeting on a train to nowhere",
    "A child discovering a magical door in their closet",
    "An astronaut finding signs of ancient civilization on Mars",
    "A struggling artist who finds success through failure",
    "An entrepreneur's journey from nothing to everything"
]

# Initialize session state
if 'stories' not in st.session_state:
    st.session_state.stories = []
if 'current_story' not in st.session_state:
    st.session_state.current_story = None

def get_openai_client():
    """Get OpenAI client with API key"""
    api_key = st.session_state.get('api_key') or os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def generate_story(prompt, genre, tone, length, language):
    """Generate a story using OpenAI"""
    client = get_openai_client()
    if not client:
        st.error("Please enter your OpenAI API key in the sidebar")
        return None

    min_words, max_words = LENGTHS[length]

    system_prompt = f"""You are a creative story writer. Write an engaging {genre.lower()} story with a {tone.lower()} tone.

Guidelines:
- Write the story in {language}
- Target length: {min_words}-{max_words} words
- Create vivid characters and settings
- Include a clear beginning, middle, and end
- Make the story engaging and memorable
- Match the tone consistently throughout
- Use markdown formatting for better readability

User's story idea: {prompt}

Write the story now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative story writer."},
                {"role": "user", "content": system_prompt}
            ],
            temperature=0.8,
            max_tokens=2000,
            stream=True
        )
        return response
    except Exception as e:
        st.error(f"Error generating story: {str(e)}")
        return None

def save_story(story_data):
    """Save story to session state"""
    st.session_state.stories.insert(0, story_data)

# Header
st.markdown("""
<div class="main-header">
    <h1>✨ StoryWriterAgent</h1>
    <p style="font-size: 1.2rem; color: #888;">AI-Powered Creative Writing Assistant</p>
    <p style="font-size: 0.9rem; color: #666;">Day 36 of #100DaysOfAI-Agents by Muhammad Sami</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Enter your OpenAI API key to generate stories"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("API Key saved!")

    st.markdown("---")

    # Stats
    st.markdown("### 📊 Statistics")
    total_stories = len(st.session_state.stories)
    total_words = sum(s.get('word_count', 0) for s in st.session_state.stories)
    favorites = sum(1 for s in st.session_state.stories if s.get('favorite', False))

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Stories", total_stories)
        st.metric("Favorites", favorites)
    with col2:
        st.metric("Words", total_words)
        st.metric("Avg Words", total_words // total_stories if total_stories > 0 else 0)

    st.markdown("---")

    # Example prompts
    st.markdown("### 💡 Example Prompts")
    for example in EXAMPLE_PROMPTS[:4]:
        if st.button(f"📝 {example[:30]}...", key=f"ex_{example[:10]}", use_container_width=True):
            st.session_state.selected_prompt = example

# Main content
tab1, tab2 = st.tabs(["✨ Generate Story", "📚 Story Library"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🪄 Create Your Story")

        # Get prompt from example or user input
        default_prompt = st.session_state.get('selected_prompt', '')
        prompt = st.text_area(
            "Your Story Idea",
            value=default_prompt,
            placeholder="Enter your story idea... (e.g., A dragon who wanted to become a chef)",
            height=100
        )

        # Clear selected prompt after use
        if 'selected_prompt' in st.session_state:
            del st.session_state.selected_prompt

    with col2:
        st.markdown("### ⚙️ Options")
        genre = st.selectbox("Genre", GENRES)
        tone = st.selectbox("Tone", TONES)
        length = st.selectbox("Length", list(LENGTHS.keys()))
        language = st.selectbox("Language", LANGUAGES)

    # Generate button
    if st.button("✨ Generate Story", type="primary", use_container_width=True):
        if not prompt:
            st.warning("Please enter a story idea")
        elif not st.session_state.get('api_key') and not os.getenv('OPENAI_API_KEY'):
            st.warning("Please enter your OpenAI API key in the sidebar")
        else:
            with st.spinner("🪄 Generating your story..."):
                story_placeholder = st.empty()
                full_content = ""

                response = generate_story(prompt, genre, tone, length, language)

                if response:
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            full_content += chunk.choices[0].delta.content
                            story_placeholder.markdown(f"""
                            <div class="story-content">
                                {full_content}
                            </div>
                            """, unsafe_allow_html=True)

                    # Save story
                    story_data = {
                        "id": datetime.now().isoformat(),
                        "prompt": prompt,
                        "content": full_content,
                        "genre": genre,
                        "tone": tone,
                        "length": length,
                        "language": language,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "word_count": len(full_content.split()),
                        "favorite": False
                    }
                    save_story(story_data)
                    st.session_state.current_story = story_data

                    st.success("✅ Story generated and saved!")

                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            "📥 Download (.md)",
                            full_content,
                            file_name=f"story_{genre.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    with col2:
                        if st.button("📋 Copy to Clipboard"):
                            st.code(full_content)
                            st.info("Select and copy the text above")
                    with col3:
                        if st.button("⭐ Add to Favorites"):
                            st.session_state.stories[0]['favorite'] = True
                            st.success("Added to favorites!")

with tab2:
    st.markdown("### 📚 Your Story Library")

    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search stories", placeholder="Search by prompt or content...")
    with col2:
        filter_genre = st.selectbox("Filter by Genre", ["All"] + GENRES)
    with col3:
        show_favorites = st.checkbox("⭐ Show Favorites Only")

    # Filter stories
    filtered_stories = st.session_state.stories

    if search:
        filtered_stories = [s for s in filtered_stories if search.lower() in s['prompt'].lower() or search.lower() in s['content'].lower()]

    if filter_genre != "All":
        filtered_stories = [s for s in filtered_stories if s['genre'] == filter_genre]

    if show_favorites:
        filtered_stories = [s for s in filtered_stories if s.get('favorite', False)]

    # Display stories
    if not filtered_stories:
        st.info("📝 No stories found. Generate your first story!")
    else:
        for i, story in enumerate(filtered_stories):
            with st.expander(f"{'⭐' if story.get('favorite') else '📖'} {story['genre']} - {story['prompt'][:50]}..."):
                # Tags
                st.markdown(f"""
                <span class="tag">{story['genre']}</span>
                <span class="tag">{story['tone']}</span>
                <span class="tag">{story['language']}</span>
                <span class="tag">{story['word_count']} words</span>
                <span class="tag">{story['created_at']}</span>
                """, unsafe_allow_html=True)

                st.markdown("---")

                # Story content
                st.markdown(story['content'])

                # Actions
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.download_button(
                        "📥 Download",
                        story['content'],
                        file_name=f"story_{story['genre'].lower()}.md",
                        mime="text/markdown",
                        key=f"dl_{i}"
                    )
                with col2:
                    if st.button("⭐ Toggle Favorite", key=f"fav_{i}"):
                        idx = st.session_state.stories.index(story)
                        st.session_state.stories[idx]['favorite'] = not story.get('favorite', False)
                        st.rerun()
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{i}"):
                        st.session_state.stories.remove(story)
                        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>Made with ❤️ by Muhammad Sami | Day 36 of #100DaysOfAI-Agents</p>
    <p>Powered by OpenAI GPT-4 & Streamlit</p>
</div>
""", unsafe_allow_html=True)

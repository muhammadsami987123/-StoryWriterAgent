// StoryWriterAgent - Enhanced Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const promptInput = document.getElementById('prompt');
    const genreSelect = document.getElementById('genre');
    const toneSelect = document.getElementById('tone');
    const lengthSelect = document.getElementById('length');
    const languageSelect = document.getElementById('language');
    const generateBtn = document.getElementById('generateBtn');
    const outputSection = document.getElementById('outputSection');
    const storyContent = document.getElementById('storyContent');
    const storyMeta = document.getElementById('storyMeta');
    const storiesList = document.getElementById('storiesList');
    const searchInput = document.getElementById('searchInput');
    const showFavoritesBtn = document.getElementById('showFavoritesBtn');
    const showStatsBtn = document.getElementById('showStatsBtn');
    const statsModal = document.getElementById('statsModal');
    const closeStatsBtn = document.getElementById('closeStatsBtn');
    const statsContent = document.getElementById('statsContent');
    const favoriteBtn = document.getElementById('favoriteBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const expandBtn = document.getElementById('expandBtn');
    const newStoryBtn = document.getElementById('newStoryBtn');
    const exampleBtns = document.querySelectorAll('.example-btn');

    // Story Modal Elements
    const storyModal = document.getElementById('storyModal');
    const closeStoryBtn = document.getElementById('closeStoryBtn');
    const storyModalTitle = document.getElementById('storyModalTitle');
    const storyModalMeta = document.getElementById('storyModalMeta');
    const storyModalContent = document.getElementById('storyModalContent');
    const modalFavBtn = document.getElementById('modalFavBtn');
    const modalCopyBtn = document.getElementById('modalCopyBtn');
    const modalDownloadBtn = document.getElementById('modalDownloadBtn');

    const toastContainer = document.getElementById('toastContainer');

    let currentStory = null;
    let currentModalStory = null;
    let showingFavorites = false;

    // Configure marked for markdown rendering
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,
            gfm: true
        });
    }

    // Load form data from localStorage
    loadFormData();

    // Load stories on page load
    loadStories();

    // Event Listeners
    generateBtn.addEventListener('click', generateStory);
    searchInput.addEventListener('input', debounce(searchStories, 300));
    showFavoritesBtn.addEventListener('click', toggleFavorites);
    showStatsBtn.addEventListener('click', showStats);
    closeStatsBtn.addEventListener('click', () => closeModal(statsModal));
    closeStoryBtn.addEventListener('click', () => closeModal(storyModal));
    favoriteBtn.addEventListener('click', toggleCurrentFavorite);
    copyBtn.addEventListener('click', () => copyStoryToClipboard(currentStory));
    downloadBtn.addEventListener('click', () => downloadStoryFile(currentStory));
    expandBtn.addEventListener('click', () => openStoryModal(currentStory));
    newStoryBtn.addEventListener('click', resetForm);

    // Modal buttons
    modalFavBtn.addEventListener('click', () => toggleModalFavorite());
    modalCopyBtn.addEventListener('click', () => copyStoryToClipboard(currentModalStory));
    modalDownloadBtn.addEventListener('click', () => downloadStoryFile(currentModalStory));

    // Example prompts
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            promptInput.value = btn.dataset.prompt;
            saveFormData();
            showToast('Prompt loaded!', 'success');
        });
    });

    // Auto-save form data
    [promptInput, genreSelect, toneSelect, lengthSelect, languageSelect].forEach(el => {
        el.addEventListener('change', saveFormData);
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            generateStory();
        }
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            if (currentStory) copyStoryToClipboard(currentStory);
        }
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            resetForm();
        }
        if (e.key === 'Escape') {
            closeModal(statsModal);
            closeModal(storyModal);
        }
    });

    // Close modal on outside click
    [statsModal, storyModal].forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal);
            }
        });
    });

    // Toast notification function
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${type === 'success' ? '✓' : '✕'}</span>
            <span class="toast-message">${message}</span>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideInRight 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Modal functions
    function closeModal(modal) {
        modal.style.display = 'none';
    }

    function openStoryModal(story) {
        if (!story) return;
        currentModalStory = story;

        storyModalTitle.innerHTML = `<span class="icon">📖</span> ${story.genre} Story`;
        storyModalMeta.innerHTML = renderStoryTags(story);
        storyModalContent.innerHTML = renderMarkdown(story.content);
        modalFavBtn.innerHTML = story.favorite ? '★ Favorited' : '☆ Favorite';

        storyModal.style.display = 'flex';
    }

    // Render story tags
    function renderStoryTags(story) {
        return `
            <span class="tag genre">${story.genre}</span>
            <span class="tag">${story.tone}</span>
            <span class="tag">${story.language}</span>
            <span class="tag words">${story.word_count} words</span>
        `;
    }

    // Render markdown content
    function renderMarkdown(content) {
        if (typeof marked !== 'undefined') {
            return marked.parse(content);
        }
        // Fallback: basic formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/^/, '<p>')
            .replace(/$/, '</p>');
    }

    // Functions
    async function generateStory() {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            showToast('Please enter a story idea', 'error');
            return;
        }

        const btnText = generateBtn.querySelector('.btn-text');
        const btnLoading = generateBtn.querySelector('.btn-loading');

        generateBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';

        outputSection.style.display = 'block';
        storyContent.innerHTML = '<span class="typewriter-cursor"></span>';
        storyMeta.innerHTML = '';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: prompt,
                    genre: genreSelect.value,
                    tone: toneSelect.value,
                    length: lengthSelect.value,
                    language: languageSelect.value,
                    stream: true
                })
            });

            if (!response.ok) throw new Error('Generation failed');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullContent = '';

            // Remove cursor for streaming
            storyContent.innerHTML = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            // Story complete - render as markdown
                            storyContent.innerHTML = renderMarkdown(fullContent);
                            loadStories();
                            showToast('Story generated successfully!', 'success');
                        } else {
                            try {
                                const parsed = JSON.parse(data);
                                if (parsed.content) {
                                    fullContent += parsed.content;
                                    // Show plain text during streaming
                                    storyContent.textContent = fullContent;
                                    storyContent.scrollTop = storyContent.scrollHeight;
                                }
                            } catch (e) {}
                        }
                    }
                }
            }

            // Update meta info
            storyMeta.innerHTML = renderStoryTags({
                genre: genreSelect.value,
                tone: toneSelect.value,
                language: languageSelect.value,
                word_count: countWords(fullContent)
            });

            currentStory = {
                content: fullContent,
                genre: genreSelect.value,
                tone: toneSelect.value,
                language: languageSelect.value,
                word_count: countWords(fullContent)
            };

            favoriteBtn.textContent = '☆';

            // Get the actual story ID from the server
            const stories = await fetch('/stories').then(r => r.json());
            if (stories.length > 0) {
                currentStory.id = stories[0].id;
                currentStory.favorite = stories[0].favorite;
            }

        } catch (error) {
            storyContent.innerHTML = `<p style="color: var(--error);">Error generating story: ${error.message}</p>`;
            showToast('Failed to generate story', 'error');
        } finally {
            generateBtn.disabled = false;
            btnText.style.display = 'flex';
            btnLoading.style.display = 'none';
        }
    }

    async function loadStories() {
        try {
            const endpoint = showingFavorites ? '/favorites' : '/stories';
            const response = await fetch(endpoint);
            const stories = await response.json();
            renderStories(stories);
        } catch (error) {
            console.error('Error loading stories:', error);
        }
    }

    async function searchStories() {
        const query = searchInput.value.trim();
        if (!query) {
            loadStories();
            return;
        }

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const stories = await response.json();
            renderStories(stories);
        } catch (error) {
            console.error('Error searching stories:', error);
        }
    }

    function renderStories(stories) {
        if (!stories.length) {
            storiesList.innerHTML = `
                <div class="empty-message">
                    <div class="empty-icon">📝</div>
                    <p>${showingFavorites ? 'No favorite stories yet.' : 'No stories found. Generate your first story!'}</p>
                </div>
            `;
            return;
        }

        storiesList.innerHTML = stories.map(story => {
            const date = new Date(story.created_at).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });

            return `
                <div class="story-card" data-id="${story.id}">
                    <div class="story-card-header">
                        <span class="story-card-title">
                            ${story.favorite ? '<span class="fav-star">★</span>' : ''}
                            ${story.genre}
                        </span>
                        <span class="story-card-date">${date}</span>
                    </div>
                    <div class="story-card-tags">
                        <span class="mini-tag">${story.tone}</span>
                        <span class="mini-tag">${story.language}</span>
                        <span class="mini-tag">${story.word_count} words</span>
                    </div>
                    <div class="story-card-preview">${story.prompt}</div>
                    <div class="story-card-footer">
                        <button class="btn btn-secondary view-btn">📖 View</button>
                        <button class="btn btn-secondary fav-btn">${story.favorite ? '★' : '☆'}</button>
                        <button class="btn btn-danger delete-btn">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');

        // Add event listeners
        storiesList.querySelectorAll('.story-card').forEach(card => {
            const id = card.dataset.id;

            card.querySelector('.view-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                viewStory(id);
            });

            card.querySelector('.fav-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                toggleFavorite(id);
            });

            card.querySelector('.delete-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                deleteStory(id);
            });

            // Click on card to view
            card.addEventListener('click', () => viewStory(id));
        });
    }

    async function viewStory(id) {
        try {
            const response = await fetch(`/stories/${id}`);
            const story = await response.json();
            openStoryModal(story);
        } catch (error) {
            showToast('Error loading story', 'error');
        }
    }

    async function toggleFavorite(id) {
        try {
            await fetch(`/stories/${id}/favorite`, { method: 'POST' });
            loadStories();
            showToast('Favorite updated!', 'success');
        } catch (error) {
            showToast('Error updating favorite', 'error');
        }
    }

    async function toggleCurrentFavorite() {
        if (!currentStory || !currentStory.id) return;
        await toggleFavorite(currentStory.id);
        currentStory.favorite = !currentStory.favorite;
        favoriteBtn.textContent = currentStory.favorite ? '★' : '☆';
    }

    async function toggleModalFavorite() {
        if (!currentModalStory || !currentModalStory.id) return;
        await toggleFavorite(currentModalStory.id);
        currentModalStory.favorite = !currentModalStory.favorite;
        modalFavBtn.innerHTML = currentModalStory.favorite ? '★ Favorited' : '☆ Favorite';
    }

    async function deleteStory(id) {
        if (!confirm('Are you sure you want to delete this story?')) return;

        try {
            await fetch(`/stories/${id}`, { method: 'DELETE' });
            loadStories();
            showToast('Story deleted', 'success');
        } catch (error) {
            showToast('Error deleting story', 'error');
        }
    }

    function toggleFavorites() {
        showingFavorites = !showingFavorites;
        showFavoritesBtn.innerHTML = showingFavorites ? '📚 All Stories' : '⭐ Favorites';
        loadStories();
    }

    async function showStats() {
        try {
            const response = await fetch('/stats');
            const stats = await response.json();

            const maxGenre = Math.max(...Object.values(stats.genres || {1: 1}));
            const maxTone = Math.max(...Object.values(stats.tones || {1: 1}));

            let genreBars = '';
            if (stats.genres && Object.keys(stats.genres).length) {
                genreBars = Object.entries(stats.genres).map(([genre, count]) => `
                    <div class="stat-bar">
                        <span class="stat-bar-label">${genre}</span>
                        <div class="stat-bar-track">
                            <div class="stat-bar-fill" style="width: ${(count / maxGenre) * 100}%"></div>
                        </div>
                        <span class="stat-bar-value">${count}</span>
                    </div>
                `).join('');
            }

            let toneBars = '';
            if (stats.tones && Object.keys(stats.tones).length) {
                toneBars = Object.entries(stats.tones).map(([tone, count]) => `
                    <div class="stat-bar">
                        <span class="stat-bar-label">${tone}</span>
                        <div class="stat-bar-track">
                            <div class="stat-bar-fill" style="width: ${(count / maxTone) * 100}%"></div>
                        </div>
                        <span class="stat-bar-value">${count}</span>
                    </div>
                `).join('');
            }

            statsContent.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_stories}</div>
                        <div class="stat-label">Total Stories</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_words.toLocaleString()}</div>
                        <div class="stat-label">Total Words</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.average_words}</div>
                        <div class="stat-label">Avg Words/Story</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.favorites}</div>
                        <div class="stat-label">Favorites</div>
                    </div>
                </div>

                ${genreBars ? `
                <div class="stat-section">
                    <h4>Stories by Genre</h4>
                    <div class="stat-bars">${genreBars}</div>
                </div>
                ` : ''}

                ${toneBars ? `
                <div class="stat-section">
                    <h4>Stories by Tone</h4>
                    <div class="stat-bars">${toneBars}</div>
                </div>
                ` : ''}
            `;

            statsModal.style.display = 'flex';
        } catch (error) {
            showToast('Error loading statistics', 'error');
        }
    }

    function copyStoryToClipboard(story) {
        if (!story) return;
        const content = story.content || storyContent.textContent;
        navigator.clipboard.writeText(content);
        showToast('Copied to clipboard!', 'success');
    }

    function downloadStoryFile(story) {
        if (!story) return;

        const content = `# ${story.genre} Story

**Genre:** ${story.genre}
**Tone:** ${story.tone}
**Language:** ${story.language}
**Words:** ${story.word_count}

---

${story.content}

---
*Generated by StoryWriterAgent - Day 36 of #100DaysOfAI-Agents*
`;

        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `story_${story.genre.toLowerCase()}_${Date.now()}.md`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('Story downloaded!', 'success');
    }

    function resetForm() {
        promptInput.value = '';
        genreSelect.selectedIndex = 0;
        toneSelect.selectedIndex = 0;
        lengthSelect.selectedIndex = 1;
        languageSelect.selectedIndex = 0;
        outputSection.style.display = 'none';
        currentStory = null;
        localStorage.removeItem('storyFormData');
        promptInput.focus();
        showToast('Ready for a new story!', 'success');
    }

    function saveFormData() {
        const data = {
            prompt: promptInput.value,
            genre: genreSelect.value,
            tone: toneSelect.value,
            length: lengthSelect.value,
            language: languageSelect.value
        };
        localStorage.setItem('storyFormData', JSON.stringify(data));
    }

    function loadFormData() {
        const saved = localStorage.getItem('storyFormData');
        if (saved) {
            const data = JSON.parse(saved);
            promptInput.value = data.prompt || '';
            if (data.genre) genreSelect.value = data.genre;
            if (data.tone) toneSelect.value = data.tone;
            if (data.length) lengthSelect.value = data.length;
            if (data.language) languageSelect.value = data.language;
        }
    }

    function countWords(text) {
        return text.trim().split(/\s+/).filter(w => w.length > 0).length;
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});

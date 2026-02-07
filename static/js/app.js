// ContentMultiplier - Enhanced JavaScript with all improvements
// Last updated: February 7, 2026 - Continuous development

// State management
let selectedPlatforms = ['twitter', 'linkedin'];
let isConverting = false;
let currentResults = null;
let conversionHistory = [];

// All available platforms
const ALL_PLATFORMS = ['twitter', 'linkedin', 'instagram', 'facebook', 'youtube', 'newsletter', 'tiktok', 'pinterest', 'threads', 'reddit'];

// Platform display names
const PLATFORM_NAMES = {
    'twitter': 'Twitter/X Thread',
    'linkedin': 'LinkedIn Post',
    'instagram': 'Instagram Caption',
    'facebook': 'Facebook Post',
    'youtube': 'YouTube Description',
    'newsletter': 'Newsletter Excerpt',
    'tiktok': 'TikTok Script',
    'pinterest': 'Pinterest Pin',
    'threads': 'Threads Post',
    'reddit': 'Reddit Post'
};

// Platform colors for UI
const PLATFORM_COLORS = {
    'twitter': '#1DA1F2',
    'linkedin': '#0A66C2',
    'instagram': '#E4405F',
    'facebook': '#1877F2',
    'youtube': '#FF0000',
    'newsletter': '#4f46e5',
    'tiktok': '#000000',
    'pinterest': '#BD081C',
    'threads': '#000000',
    'reddit': '#FF4500'
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadDemoData();
    updateCounters();
    loadHistory();
    console.log('🚀 ContentMultiplier initialized');
});

// Event Listeners
function setupEventListeners() {
    const contentInput = document.getElementById('contentInput');
    if (contentInput) {
        contentInput.addEventListener('input', () => {
            updateCharCount();
            updateWordCount();
        });
    }
}

// Character and word count
function updateCharCount() {
    const content = document.getElementById('contentInput').value;
    const count = content.length;
    const counter = document.getElementById('charCount');
    
    if (counter) {
        counter.textContent = `${count} znakov`;
        
        if (count > 2000) {
            counter.classList.add('char-count-danger');
            counter.classList.remove('char-count-warning');
        } else if (count > 1500) {
            counter.classList.add('char-count-warning');
            counter.classList.remove('char-count-danger');
        } else {
            counter.classList.remove('char-count-warning', 'char-count-danger');
        }
    }
}

function updateWordCount() {
    const content = document.getElementById('contentInput').value;
    const words = content.trim().split(/\s+/).filter(w => w.length > 0).length;
    const counter = document.getElementById('wordCount');
    
    if (counter) {
        counter.textContent = `${words} slov`;
    }
    
    // Update reading time
    updateReadingTime(words);
}

function updateReadingTime(words) {
    const readingTimeEl = document.getElementById('readingTime');
    if (readingTimeEl) {
        const minutes = Math.max(1, Math.ceil(words / 200));
        readingTimeEl.innerHTML = `\u003ci class="far fa-clock mr-1"\u003e\u003c/i\u003e${minutes} min čítania`;
    }
}

function updateCounters() {
    updateCharCount();
    updateWordCount();
}

// Toggle platform selection
function togglePlatform(platform) {
    const btn = document.getElementById(`btn-${platform}`);
    
    if (selectedPlatforms.includes(platform)) {
        if (selectedPlatforms.length > 1) {
            selectedPlatforms = selectedPlatforms.filter(p => p !== platform);
            btn.classList.remove('active');
            btn.classList.remove('bg-indigo-600', 'border-indigo-600', 'text-white');
            btn.classList.add('border-gray-300', 'text-gray-600');
        }
    } else {
        selectedPlatforms.push(platform);
        btn.classList.add('active');
        btn.classList.remove('border-gray-300', 'text-gray-600');
        btn.classList.add('bg-indigo-600', 'border-indigo-600', 'text-white');
    }
}

// Select all platforms
function selectAllPlatforms() {
    ALL_PLATFORMS.forEach(platform => {
        if (!selectedPlatforms.includes(platform)) {
            selectedPlatforms.push(platform);
        }
        const btn = document.getElementById(`btn-${platform}`);
        if (btn) {
            btn.classList.add('active');
            btn.classList.remove('border-gray-300', 'text-gray-600');
            btn.classList.add('bg-indigo-600', 'border-indigo-600', 'text-white');
        }
    });
}

// Deselect all platforms
function deselectAllPlatforms() {
    selectedPlatforms = ['twitter'];
    ALL_PLATFORMS.forEach(platform => {
        const btn = document.getElementById(`btn-${platform}`);
        if (btn) {
            if (platform === 'twitter') {
                btn.classList.add('active');
                btn.classList.remove('border-gray-300', 'text-gray-600');
                btn.classList.add('bg-indigo-600', 'border-indigo-600', 'text-white');
            } else {
                btn.classList.remove('active');
                btn.classList.remove('bg-indigo-600', 'border-indigo-600', 'text-white');
                btn.classList.add('border-gray-300', 'text-gray-600');
            }
        }
    });
}

// Main conversion function
async function convertContent() {
    if (isConverting) return;
    
    const content = document.getElementById('contentInput').value.trim();
    
    if (!content) {
        showToast('Prosím vložte obsah na konverziu', 'warning');
        return;
    }
    
    if (content.length < 50) {
        showToast('Obsah je príliš krátky. Minimálne 50 znakov.', 'warning');
        return;
    }
    
    isConverting = true;
    showLoading(true);
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                platforms: selectedPlatforms,
                tone: document.getElementById('toneSelect').value
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentResults = data.results;
            displayResults(data.results);
            showDownloadButton(true);
            saveToHistory(content, data.results, selectedPlatforms, data.tone);
            showToast('Obsah úspešne vygenerovaný!', 'success');
            trackEvent('content_converted', {
                platforms: selectedPlatforms.length,
                tone: data.tone,
                content_length: data.original_length
            });
        } else {
            showToast(data.error || 'Nastala chyba', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        handleApiError(error);
    } finally {
        isConverting = false;
        showLoading(false);
    }
}

// Show/hide loading
function showLoading(show) {
    const indicator = document.getElementById('loadingIndicator');
    const skeleton = document.getElementById('loadingSkeleton');
    const emptyState = document.getElementById('emptyState');
    const btn = document.getElementById('convertBtn');
    const progressBar = document.getElementById('progressBarFill');

    if (show) {
        indicator.classList.remove('hidden');
        if (skeleton) skeleton.classList.remove('hidden');
        if (emptyState) emptyState.classList.add('hidden');
        btn.disabled = true;
        btn.innerHTML = '\u003ci class="fas fa-spinner fa-spin mr-2"\u003e\u003c/i\u003e\u003cspan\u003eGenerujem...\u003c/span\u003e';
        btn.classList.add('opacity-75');
        
        if (progressBar) {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                progressBar.style.width = progress + '%';
            }, 200);
            window.progressInterval = interval;
        }
    } else {
        indicator.classList.add('hidden');
        if (skeleton) skeleton.classList.add('hidden');
        btn.disabled = false;
        btn.innerHTML = '\u003ci class="fas fa-magic mr-2"\u003e\u003c/i\u003e\u003cspan\u003eGenerovať obsah\u003c/span\u003e';
        btn.classList.remove('opacity-75');
        
        if (window.progressInterval) {
            clearInterval(window.progressInterval);
        }
        if (progressBar) {
            progressBar.style.width = '0%';
        }
    }
}

// Show/hide download buttons
function showDownloadButton(show) {
    const buttons = ['downloadBtn', 'clearBtn', 'exportBtn', 'copyAllBtn'];
    buttons.forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
            if (show) btn.classList.remove('hidden');
            else btn.classList.add('hidden');
        }
    });
}

// Display results
function displayResults(results) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = '';
    
    Object.entries(results).forEach(([platform, data]) => {
        const card = createResultCard(platform, PLATFORM_NAMES[platform], data);
        container.appendChild(card);
    });
    
    animateCards();
}

// Animate cards
function animateCards() {
    const cards = document.querySelectorAll('.result-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Create result card
function createResultCard(platform, name, data) {
    const div = document.createElement('div');
    div.className = 'result-card';
    
    const color = PLATFORM_COLORS[platform] || '#4f46e5';
    
    let content = '';
    if (platform === 'twitter' && data.tweets) {
        content = data.tweets.map((tweet, i) => 
            `\u003cdiv class="mb-2 p-2 bg-white rounded border text-sm hover:border-indigo-300 transition"\u003e${escapeHtml(tweet)}\u003c/div\u003e`
        ).join('');
    } else if (platform === 'threads' && data.posts) {
        content = data.posts.map((post, i) => 
            `\u003cdiv class="mb-2 p-2 bg-white rounded border text-sm hover:border-indigo-300 transition"\u003e${escapeHtml(post)}\u003c/div\u003e`
        ).join('');
    } else if (data.content) {
        content = `\u003cdiv class="p-3 bg-white rounded border text-sm whitespace-pre-wrap hover:border-indigo-300 transition"\u003e${escapeHtml(data.content)}\u003c/div\u003e`;
    }
    
    const metrics = [];
    if (data.estimated_engagement) metrics.push(`📊 ${data.estimated_engagement}`);
    if (data.character_count) metrics.push(`📝 ${data.character_count} znakov`);
    if (data.hashtag_count) metrics.push(`🏷️ ${data.hashtag_count} hashtagov`);
    if (data.count) metrics.push(`📱 ${data.count} posts`);
    
    div.innerHTML = `
        \u003cdiv class="flex items-center justify-between mb-3"\u003e
            \u003cdiv class="flex items-center"\u003e
                \u003ci class="fab fa-${platform} text-xl mr-2" style="color: ${color}"\u003e\u003c/i\u003e
                \u003cspan class="font-semibold"\u003e${name}\u003c/span\u003e
            \u003c/div\u003e
            \u003cbutton onclick="copyToClipboard(this, '${platform}')" class="copy-btn px-3 py-1 rounded border text-sm flex items-center hover:bg-indigo-50 transition"\u003e
                \u003ci class="fas fa-copy mr-1"\u003e\u003c/i\u003e\u003cspan\u003eKopírovať\u003c/span\u003e
            \u003c/button\u003e
        \u003c/div\u003e
        \u003cdiv class="result-content mb-3" data-platform="${platform}"\u003e${content}\u003c/div\u003e
        ${metrics.length \u003e 0 ? `\u003cdiv class="text-xs text-gray-500 flex flex-wrap gap-2"\u003e${metrics.map(m => `\u003cspan class="bg-gray-100 px-2 py-1 rounded"\u003e${m}\u003c/span\u003e`).join('')}\u003c/div\u003e` : ''}
    `;
    
    return div;
}

// Copy to clipboard
function copyToClipboard(btn, platform) {
    const card = btn.closest('.result-card');
    const contentDiv = card.querySelector('.result-content');
    
    let textToCopy = '';
    const textElements = contentDiv.querySelectorAll('div');
    textElements.forEach(el => {
        textToCopy += el.textContent + '\n\n';
    });
    
    navigator.clipboard.writeText(textToCopy.trim()).then(() => {
        btn.classList.add('copied');
        const icon = btn.querySelector('i');
        const span = btn.querySelector('span');
        icon.classList.remove('fa-copy');
        icon.classList.add('fa-check');
        span.textContent = 'Skopírované!';
        setTimeout(() => {
            btn.classList.remove('copied');
            icon.classList.remove('fa-check');
            icon.classList.add('fa-copy');
            span.textContent = 'Kopírovať';
        }, 2000);
        showToast('Skopírované do schránky!', 'success');
    });
}

// Show toast
function showToast(message, type = 'success') {
    const existing = document.querySelectorAll('.toast');
    existing.forEach(t => t.remove());
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    const colors = { success: '#10b981', error: '#ef4444', warning: '#f59e0b', info: '#3b82f6' };
    const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
    
    toast.style.background = colors[type] || colors.success;
    toast.innerHTML = `\u003cspan style="margin-right: 8px;"\u003e${icons[type] || icons.success}\u003c/span\u003e${message}`;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Scroll to converter
function scrollToConverter() {
    document.getElementById('converter').scrollIntoView({ behavior: 'smooth' });
}

// Show demo
async function showDemo() {
    try {
        const response = await fetch('/api/demo');
        const data = await response.json();
        
        document.getElementById('contentInput').value = data.demo_input;
        updateCounters();
        currentResults = data.demo_results;
        displayResults(data.demo_results);
        showDownloadButton(true);
        scrollToConverter();
        showToast('Demo načítané!', 'success');
    } catch (error) {
        showToast('Nepodarilo sa načítať demo', 'error');
    }
}

// Load demo data
async function loadDemoData() {
    // Optional
}

// Track event
function trackEvent(eventName, data = {}) {
    console.log('[Analytics]', eventName, data);
}

// History functions
function saveToHistory(content, results, platforms, tone) {
    const historyItem = {
        id: Date.now(),
        content: content.substring(0, 200) + (content.length > 200 ? '...' : ''),
        results: results,
        platforms: platforms,
        tone: tone,
        timestamp: new Date().toISOString(),
        platformCount: Object.keys(results).length
    };
    
    conversionHistory.unshift(historyItem);
    if (conversionHistory.length > 20) {
        conversionHistory = conversionHistory.slice(0, 20);
    }
    
    localStorage.setItem('contentMultiplier_history', JSON.stringify(conversionHistory));
}

function loadHistory() {
    const saved = localStorage.getItem('contentMultiplier_history');
    if (saved) {
        try {
            conversionHistory = JSON.parse(saved);
        } catch (e) {
            console.error('Error loading history:', e);
            conversionHistory = [];
        }
    }
}

function clearResults() {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = `
        \u003cdiv id="emptyState" class="text-center py-12 text-gray-400"\u003e
            \u003ci class="fas fa-rocket text-6xl mb-4 opacity-30"\u003e\u003c/i\u003e
            \u003cp\u003eVýsledky sa zobrazia tu\u003c/p\u003e
            \u003cp class="text-sm mt-2"\u003eVložte obsah a kliknite "Generovať"\u003c/p\u003e
        \u003c/div\u003e
    `;
    currentResults = null;
    showDownloadButton(false);
    showToast('Výsledky vymazané', 'info');
}

// Export and download
function downloadAllResults() {
    if (!currentResults) return;
    
    let text = '# ContentMultiplier - Vygenerovaný obsah\n';
    text += `Dátum: ${new Date().toLocaleString()}\n`;
    text += '='.repeat(50) + '\n\n';
    
    Object.entries(currentResults).forEach(([platform, data]) => {
        text += `## ${PLATFORM_NAMES[platform] || platform}\n`;
        text += '-'.repeat(40) + '\n';
        if (data.tweets) text += data.tweets.join('\n\n') + '\n';
        else if (data.posts) text += data.posts.join('\n\n') + '\n';
        else if (data.content) text += data.content + '\n';
        text += '\n\n';
    });
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `content-multiplier-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Výsledky stiahnuté!', 'success');
}

function exportAsJSON() {
    if (!currentResults) {
        showToast('Nie sú žiadne výsledky na export', 'warning');
        return;
    }
    
    const exportData = {
        exportDate: new Date().toISOString(),
        originalContent: document.getElementById('contentInput').value,
        results: currentResults,
        platforms: selectedPlatforms,
        tone: document.getElementById('toneSelect').value
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `content-multiplier-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Exportované ako JSON!', 'success');
}

function copyAllResults() {
    if (!currentResults) return;
    
    let text = '🚀 ContentMultiplier - Vygenerovaný obsah\n';
    text += '='.repeat(50) + '\n\n';
    
    Object.entries(currentResults).forEach(([platform, data]) => {
        text += `📱 ${PLATFORM_NAMES[platform] || platform}\n`;
        text += '-'.repeat(40) + '\n';
        if (data.tweets) text += data.tweets.join('\n\n') + '\n';
        else if (data.posts) text += data.posts.join('\n\n') + '\n';
        else if (data.content) text += data.content + '\n';
        text += '\n' + '='.repeat(40) + '\n\n';
    });
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('Všetky výsledky skopírované!', 'success');
    });
}

// Keyboard shortcuts
function showShortcuts() {
    const modal = document.getElementById('shortcutsModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function hideShortcuts() {
    const modal = document.getElementById('shortcutsModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === '?' || (e.shiftKey && e.key === '/')) {
        e.preventDefault();
        showShortcuts();
    }
    if (e.key === 'Escape') hideShortcuts();
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        convertContent();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'a' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        selectAllPlatforms();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'd' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        deselectAllPlatforms();
    }
});

document.addEventListener('click', (e) => {
    const modal = document.getElementById('shortcutsModal');
    if (e.target === modal) hideShortcuts();
});

// Share results
function shareResults(platform) {
    if (!currentResults) {
        showToast('Nie sú žiadne výsledky na zdieľanie', 'warning');
        return;
    }
    
    const text = 'Práve som vytvoril obsah pre 10 sociálnych sietí pomocou ContentMultiplier! 🚀';
    const url = window.location.href;
    
    const shareUrls = {
        twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`,
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`
    };
    
    if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
        trackEvent('share', { platform });
    }
}

// Error handling
function handleApiError(error) {
    console.error('API Error:', error);
    let message = 'Nastala chyba pri komunikácii so serverom';
    if (error.message && error.message.includes('Failed to fetch')) {
        message = 'Server nie je dostupný. Skúste to neskôr.';
    }
    showToast(message, 'error');
}

// Analytics
trackEvent('page_load', { url: window.location.href, timestamp: new Date().toISOString() });

console.log('✅ ContentMultiplier fully loaded');

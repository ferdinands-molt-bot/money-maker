// ContentMultiplier - Frontend JavaScript

// State management
let selectedPlatforms = ['twitter', 'linkedin'];
let isConverting = false;
let currentResults = null;
let conversionHistory = [];

// All available platforms
const ALL_PLATFORMS = ['twitter', 'linkedin', 'instagram', 'facebook', 'youtube', 'newsletter', 'tiktok', 'pinterest', 'threads', 'reddit'];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadDemoData();
    updateCounters();
    loadHistory();
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

function updateWordCount() {
    const content = document.getElementById('contentInput').value;
    const words = content.trim().split(/\s+/).filter(w => w.length > 0).length;
    const counter = document.getElementById('wordCount');
    
    counter.textContent = `${words} slov`;
}

function updateCounters() {
    updateCharCount();
    updateWordCount();
}

// Toggle platform selection
function togglePlatform(platform) {
    const btn = document.getElementById(`btn-${platform}`);
    
    if (selectedPlatforms.includes(platform)) {
        // Don't allow deselecting if it's the last one
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

// Deselect all platforms (keep only first one)
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
            
            // Save to history
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
        showToast('Nastala chyba pri generovaní', 'error');
    } finally {
        isConverting = false;
        showLoading(false);
    }
}

// Show/hide loading
function showLoading(show) {
    const indicator = document.getElementById('loadingIndicator');
    const btn = document.getElementById('convertBtn');
    
    if (show) {
        indicator.classList.remove('hidden');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i><span>Generujem...</span>';
        btn.classList.add('opacity-75');
    } else {
        indicator.classList.add('hidden');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic mr-2"></i><span>Generovať obsah</span>';
        btn.classList.remove('opacity-75');
    }
}

// Show/hide download button
function showDownloadButton(show) {
    const downloadBtn = document.getElementById('downloadBtn');
    const clearBtn = document.getElementById('clearBtn');
    const exportBtn = document.getElementById('exportBtn');
    
    if (show) {
        downloadBtn.classList.remove('hidden');
        clearBtn.classList.remove('hidden');
        exportBtn.classList.remove('hidden');
    } else {
        downloadBtn.classList.add('hidden');
        clearBtn.classList.add('hidden');
        exportBtn.classList.add('hidden');
    }
}

// Display results
function displayResults(results) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = '';
    
    const platformNames = {
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
    
    const platformIcons = {
        'twitter': 'fab fa-twitter',
        'linkedin': 'fab fa-linkedin',
        'instagram': 'fab fa-instagram',
        'facebook': 'fab fa-facebook',
        'youtube': 'fab fa-youtube',
        'newsletter': 'fas fa-envelope',
        'tiktok': 'fab fa-tiktok',
        'pinterest': 'fab fa-pinterest',
        'threads': 'fab fa-threads',
        'reddit': 'fab fa-reddit'
    };
    
    Object.entries(results).forEach(([platform, data]) => {
        const card = createResultCard(platform, platformNames[platform], platformIcons[platform], data);
        container.appendChild(card);
    });
    
    // Animate cards in
    animateCards();
}

// Animate result cards
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
function createResultCard(platform, name, iconClass, data) {
    const div = document.createElement('div');
    div.className = 'result-card';
    
    let content = '';
    
    if (platform === 'twitter' && data.tweets) {
        content = data.tweets.map((tweet, i) => 
            `<div class="mb-2 p-2 bg-white rounded border text-sm hover:border-indigo-300 transition">${escapeHtml(tweet)}</div>`
        ).join('');
    } else if (platform === 'threads' && data.posts) {
        content = data.posts.map((post, i) => 
            `<div class="mb-2 p-2 bg-white rounded border text-sm hover:border-indigo-300 transition">${escapeHtml(post)}</div>`
        ).join('');
    } else if (data.content) {
        content = `<div class="p-3 bg-white rounded border text-sm whitespace-pre-wrap hover:border-indigo-300 transition">${escapeHtml(data.content)}</div>`;
    }
    
    // Build metrics
    const metrics = [];
    if (data.estimated_engagement) metrics.push(`📊 ${data.estimated_engagement} engagement`);
    if (data.estimated_reach) metrics.push(`🎯 ${data.estimated_reach}`);
    if (data.character_count) metrics.push(`📝 ${data.character_count} znakov`);
    if (data.hashtag_count) metrics.push(`🏷️ ${data.hashtag_count} hashtagov`);
    if (data.viral_potential) metrics.push(`🔥 ${data.viral_potential} viral`);
    if (data.count) metrics.push(`📱 ${data.count} posts`);
    
    // Get platform color
    const platformColors = {
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
    const color = platformColors[platform] || '#4f46e5';
    
    div.innerHTML = `
        <div class="flex items-center justify-between mb-3">
            <div class="flex items-center">
                <i class="${iconClass} text-xl mr-2" style="color: ${color}"></i>
                <span class="font-semibold">${name}</span>
            </div>
            <div class="flex gap-2">
                <button onclick="copyToClipboard(this, '${platform}')" class="copy-btn px-3 py-1 rounded border text-sm flex items-center hover:bg-indigo-50 transition">
                    <i class="fas fa-copy mr-1"></i>
                    <span>Kopírovať</span>
                </button>
            </div>
        </div>
        <div class="result-content mb-3" data-platform="${platform}">
            ${content}
        </div>
        ${metrics.length > 0 ? `<div class="text-xs text-gray-500 flex flex-wrap gap-2">${metrics.map(m => `<span class="bg-gray-100 px-2 py-1 rounded">${m}</span>`).join('')}</div>` : ''}
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
    }).catch(err => {
        showToast('Nepodarilo sa skopírovať', 'error');
    });
}

// Download all results
function downloadAllResults() {
    if (!currentResults) return;
    
    let text = '# ContentMultiplier - Vygenerovaný obsah\n';
    text += `Dátum: ${new Date().toLocaleString()}\n`;
    text += '='.repeat(50) + '\n\n';
    
    const platformNames = {
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
    
    Object.entries(currentResults).forEach(([platform, data]) => {
        text += `## ${platformNames[platform] || platform}\n`;
        text += '-'.repeat(40) + '\n';
        
        if (data.tweets) {
            text += data.tweets.join('\n\n') + '\n';
        } else if (data.posts) {
            text += data.posts.join('\n\n') + '\n';
        } else if (data.content) {
            text += data.content + '\n';
        }
        
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
    trackEvent('results_downloaded', { platforms: Object.keys(currentResults).length });
}

// Show toast notification
function showToast(message, type = 'success') {
    // Remove existing toasts
    const existing = document.querySelectorAll('.toast');
    existing.forEach(t => t.remove());
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    
    toast.style.background = colors[type] || colors.success;
    toast.innerHTML = `<span style="margin-right: 8px;">${icons[type] || icons.success}</span>${message}`;
    
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
        showToast('Demo načítané! Pozrite si výsledky.', 'success');
    } catch (error) {
        showToast('Nepodarilo sa načítať demo', 'error');
    }
}

// Load demo data
async function loadDemoData() {
    // Optionally load initial demo
}

// Pricing interaction
document.querySelectorAll('#pricing button').forEach(btn => {
    if (!btn.onclick) {
        btn.addEventListener('click', () => {
            showToast('Funkcia dostupná čoskoro!', 'warning');
        });
    }
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to convert
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        convertContent();
    }
    
    // Escape to close modals (if any)
    if (e.key === 'Escape') {
        // Close any open modals
    }
});

// Analytics (simple)
function trackEvent(eventName, data = {}) {
    console.log('[Analytics]', eventName, data);
    // In production, send to analytics service
}

// Track page load
trackEvent('page_load', {
    url: window.location.href,
    timestamp: new Date().toISOString()
});

// Intersection Observer for animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.hover-card, .result-card').forEach(el => {
        observer.observe(el);
    });
});

// ============ HISTORY FEATURE ============

// Save conversion to history
function saveToHistory(content, results, platforms, tone) {
    const historyItem = {
        id: Date.now(),
        content: content.substring(0, 200) + (content.length > 200 ? '...' : ''),
        fullContent: content,
        results: results,
        platforms: platforms,
        tone: tone,
        timestamp: new Date().toISOString(),
        platformCount: Object.keys(results).length
    };
    
    // Add to beginning of array
    conversionHistory.unshift(historyItem);
    
    // Keep only last 20 items
    if (conversionHistory.length > 20) {
        conversionHistory = conversionHistory.slice(0, 20);
    }
    
    // Save to localStorage
    localStorage.setItem('contentMultiplier_history', JSON.stringify(conversionHistory));
}

// Load history from localStorage
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

// Clear all results
function clearResults() {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = `
        <div id="emptyState" class="text-center py-12 text-gray-400">
            <i class="fas fa-rocket text-6xl mb-4 opacity-30"></i>
            <p>Výsledky sa zobrazia tu</p>
            <p class="text-sm mt-2">Vložte obsah a kliknite "Generovať"</p>
        </div>
    `;
    currentResults = null;
    showDownloadButton(false);
    showToast('Výsledky vymazané', 'info');
}

// Export results as JSON
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

// Calculate reading time
function calculateReadingTime(text) {
    const words = text.trim().split(/\s+/).length;
    const minutes = Math.ceil(words / 200); // Average reading speed
    return minutes;
}

// Check Twitter character limit
function checkTwitterLimit(text) {
    // Twitter has 280 char limit per tweet
    const limit = 280;
    const length = text.length;
    
    if (length > limit) {
        return {
            valid: false,
            overBy: length - limit,
            message: `Prekročený limit o ${length - limit} znakov`
        };
    }
    
    return {
        valid: true,
        remaining: limit - length,
        message: `Zostáva ${limit - length} znakov`
    };
}

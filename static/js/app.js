// ContentMultiplier - Frontend JavaScript

// State management
let selectedPlatforms = ['twitter', 'linkedin'];
let isConverting = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadDemoData();
});

// Event Listeners
function setupEventListeners() {
    const contentInput = document.getElementById('contentInput');
    if (contentInput) {
        contentInput.addEventListener('input', updateCharCount);
    }
}

// Character count
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
            displayResults(data.results);
            showToast('Obsah úspešne vygenerovaný!', 'success');
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
    } else {
        indicator.classList.add('hidden');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic mr-2"></i><span>Generovať obsah</span>';
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
        'newsletter': 'Newsletter Excerpt'
    };
    
    const platformIcons = {
        'twitter': 'fab fa-twitter',
        'linkedin': 'fab fa-linkedin',
        'instagram': 'fab fa-instagram',
        'facebook': 'fab fa-facebook',
        'youtube': 'fab fa-youtube',
        'newsletter': 'fas fa-envelope'
    };
    
    Object.entries(results).forEach(([platform, data]) => {
        const card = createResultCard(platform, platformNames[platform], platformIcons[platform], data);
        container.appendChild(card);
    });
}

// Create result card
function createResultCard(platform, name, iconClass, data) {
    const div = document.createElement('div');
    div.className = 'result-card';
    
    let content = '';
    
    if (platform === 'twitter' && data.tweets) {
        content = data.tweets.map((tweet, i) => 
            `<div class="mb-2 p-2 bg-white rounded border text-sm">${escapeHtml(tweet)}</div>`
        ).join('');
    } else if (data.content) {
        content = `<div class="p-3 bg-white rounded border text-sm whitespace-pre-wrap">${escapeHtml(data.content)}</div>`;
    }
    
    const metrics = [];
    if (data.estimated_engagement) metrics.push(`📊 ${data.estimated_engagement}`);
    if (data.estimated_reach) metrics.push(`🎯 ${data.estimated_reach}`);
    if (data.character_count) metrics.push(`📝 ${data.character_count} znakov`);
    if (data.hashtag_count) metrics.push(`🏷️ ${data.hashtag_count} hashtagov`);
    
    div.innerHTML = `
        <div class="flex items-center justify-between mb-3">
            <div class="flex items-center">
                <i class="${iconClass} text-xl mr-2"></i>
                <span class="font-semibold">${name}</span>
            </div>
            <button onclick="copyToClipboard(this, '${platform}')" class="copy-btn px-3 py-1 rounded border text-sm flex items-center">
                <i class="fas fa-copy mr-1"></i>
                <span>Kopírovať</span>
            </button>
        </div>
        <div class="result-content mb-3" data-platform="${platform}">
            ${content}
        </div>
        ${metrics.length > 0 ? `<div class="text-xs text-gray-500">${metrics.join(' • ')}</div>` : ''}
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
        const span = btn.querySelector('span');
        const originalText = span.textContent;
        span.textContent = 'Skopírované!';
        
        setTimeout(() => {
            btn.classList.remove('copied');
            span.textContent = originalText;
        }, 2000);
        
        showToast('Skopírované do schránky!', 'success');
    });
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b'
    };
    
    toast.style.background = colors[type] || colors.success;
    toast.textContent = message;
    
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
        updateCharCount();
        displayResults(data.demo_results);
        
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

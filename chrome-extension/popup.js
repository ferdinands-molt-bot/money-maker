// ContentMultiplier Chrome Extension - Popup Script

document.addEventListener('DOMContentLoaded', () => {
    const contentInput = document.getElementById('contentInput');
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const platformBtns = document.querySelectorAll('.platform-btn');
    
    let selectedPlatforms = ['twitter', 'linkedin'];
    
    // Platform selection
    platformBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const platform = btn.dataset.platform;
            
            if (selectedPlatforms.includes(platform)) {
                if (selectedPlatforms.length > 1) {
                    selectedPlatforms = selectedPlatforms.filter(p => p !== platform);
                    btn.classList.remove('active');
                }
            } else {
                selectedPlatforms.push(platform);
                btn.classList.add('active');
            }
        });
    });
    
    // Generate content
    generateBtn.addEventListener('click', async () => {
        const content = contentInput.value.trim();
        
        if (!content || content.length < 50) {
            alert('Please enter at least 50 characters');
            return;
        }
        
        // Show loading
        generateBtn.disabled = true;
        loading.style.display = 'block';
        results.style.display = 'none';
        results.innerHTML = '';
        
        try {
            const response = await fetch('http://localhost:8080/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: content,
                    platforms: selectedPlatforms,
                    tone: 'professional'
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data.results);
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error connecting to server. Make sure the app is running.');
        } finally {
            generateBtn.disabled = false;
            loading.style.display = 'none';
        }
    });
    
    function displayResults(resultsData) {
        results.style.display = 'block';
        
        const platformNames = {
            'twitter': 'Twitter/X',
            'linkedin': 'LinkedIn',
            'instagram': 'Instagram',
            'facebook': 'Facebook',
            'youtube': 'YouTube',
            'newsletter': 'Newsletter'
        };
        
        Object.entries(resultsData).forEach(([platform, data]) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            let content = '';
            if (data.tweets) {
                content = data.tweets.join('\n\n');
            } else if (data.content) {
                content = data.content;
            }
            
            card.innerHTML = `
                <div class="result-header">
                    <span class="result-platform">${platformNames[platform]}</span>
                    <button class="copy-btn" data-content="${escapeHtml(content)}">Copy</button>
                </div>
                <div class="result-content">${escapeHtml(content).replace(/\n/g, '<br>')}</div>
            `;
            
            results.appendChild(card);
        });
        
        // Add copy functionality
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const content = btn.dataset.content;
                navigator.clipboard.writeText(content);
                btn.textContent = 'Copied!';
                setTimeout(() => btn.textContent = 'Copy', 2000);
            });
        });
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Get content from current page
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, {action: 'getContent'}, (response) => {
            if (response && response.content) {
                contentInput.value = response.content.substring(0, 2000);
            }
        });
    });
});

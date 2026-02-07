"""
Utility functions for ContentMultiplier
"""

import re
import json
from datetime import datetime

def count_words(text):
    """Count words in text"""
    return len(text.split())

def count_sentences(text):
    """Count sentences in text"""
    return len(re.findall(r'[.!?]+', text))

def estimate_reading_time(text):
    """Estimate reading time in minutes (200 wpm average)"""
    words = count_words(text)
    return max(1, round(words / 200))

def truncate_text(text, max_length=100, suffix='...'):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def format_number(num):
    """Format large numbers (1000 -> 1K)"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    if num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def sanitize_input(text):
    """Sanitize user input"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text.strip()

def extract_hashtags(text):
    """Extract hashtags from text"""
    return re.findall(r'#\w+', text)

def extract_mentions(text):
    """Extract @mentions from text"""
    return re.findall(r'@\w+', text)

def calculate_engagement_score(content, platform):
    """
    Calculate estimated engagement score based on content characteristics
    Returns score 0-100
    """
    score = 50  # Base score
    
    # Length checks
    if platform == 'twitter':
        if len(content) < 100:
            score += 10  # Concise is better
        if '?' in content:
            score += 5  # Questions engage
        if any(h in content for h in ['🧵', '🧶']):
            score += 5  # Thread indicator
            
    elif platform == 'linkedin':
        if len(content) > 500:
            score += 10  # Longer performs better
        if any(n in content for n in ['1️⃣', '2️⃣', '3️⃣']):
            score += 10  # Numbered lists
        if '?' in content:
            score += 5
            
    elif platform == 'instagram':
        hashtags = len(extract_hashtags(content))
        if 10 <= hashtags <= 20:
            score += 10
        if '📸' in content or '✨' in content:
            score += 5
    
    # Universal factors
    if content.count('!') > 3:
        score -= 10  # Too many exclamation marks
    if content.isupper():
        score -= 20  # All caps is bad
    
    return min(100, max(0, score))

def generate_share_text(platform, content_type):
    """Generate share text for social media"""
    templates = {
        'twitter': [
            "Just used ContentMultiplier to turn my blog post into a Twitter thread in 30 seconds! 🚀",
            "This tool saved me 5 hours this week. One blog post → 6 platforms instantly!",
            "Content repurposing used to take me hours. Now it's 30 seconds. Game changer! 💪"
        ],
        'linkedin': [
            "I've been testing ContentMultiplier for content repurposing. The results are impressive - what used to take 3+ hours now takes 30 seconds.",
            "As a content creator, finding ways to work smarter is crucial. ContentMultiplier helps me reach audiences across 6 platforms with one click."
        ]
    }
    
    import random
    return random.choice(templates.get(platform, ["Check out ContentMultiplier!"]))

def log_conversion(user_id, platforms, content_length):
    """Log conversion for analytics"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'platforms': platforms,
        'content_length': content_length,
        'platform_count': len(platforms)
    }
    
    # In production, this would write to database
    # For now, just print
    print(f"[CONVERSION] {json.dumps(log_entry)}")
    return log_entry

# Platform-specific utilities
PLATFORM_LIMITS = {
    'twitter': {'chars': 280, 'threads': True},
    'linkedin': {'chars': 3000, 'threads': False},
    'instagram': {'chars': 2200, 'threads': False},
    'facebook': {'chars': 63206, 'threads': False},
    'youtube': {'chars': 5000, 'threads': False},
    'newsletter': {'chars': float('inf'), 'threads': False}
}

def get_platform_limit(platform):
    """Get character limit for platform"""
    return PLATFORM_LIMITS.get(platform, {}).get('chars', 1000)

def split_into_thread(text, platform='twitter'):
    """Split long text into thread format"""
    limit = get_platform_limit(platform)
    tweets = []
    
    while len(text) > limit:
        # Find last space before limit
        split_point = text[:limit].rfind(' ')
        if split_point == -1:
            split_point = limit
        
        tweets.append(text[:split_point].strip())
        text = text[split_point:].strip()
    
    if text:
        tweets.append(text)
    
    return tweets

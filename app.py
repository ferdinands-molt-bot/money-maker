from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Konfigurácia
app.config['SECRET_KEY'] = os.urandom(24)

# Simulovaná "databáza" používateľov (v produkcii by to bola reálna DB)
users_db = {}
content_history = []

# Ceny pre monetizáciu
PRICING = {
    'free': {
        'name': 'Free',
        'price': 0,
        'limits': {
            'monthly_conversions': 3,
            'platforms': ['twitter', 'linkedin']
        }
    },
    'pro': {
        'name': 'Pro',
        'price': 9,
        'limits': {
            'monthly_conversions': float('inf'),
            'platforms': ['twitter', 'linkedin', 'instagram', 'facebook', 'youtube', 'newsletter']
        }
    },
    'business': {
        'name': 'Business',
        'price': 29,
        'limits': {
            'monthly_conversions': float('inf'),
            'platforms': ['twitter', 'linkedin', 'instagram', 'facebook', 'youtube', 'newsletter'],
            'team_members': 5,
            'api_access': True
        }
    }
}

@app.route('/')
def index():
    """Hlavná stránka"""
    return render_template('index.html')

@app.route('/api/pricing')
def get_pricing():
    """Vráti cenník"""
    return jsonify(PRICING)

@app.route('/api/convert', methods=['POST'])
def convert_content():
    """Hlavná API funkcia - konverzia obsahu"""
    data = request.json
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content'}), 400
    
    original_content = data.get('content', '')
    platforms = data.get('platforms', ['twitter', 'linkedin'])
    tone = data.get('tone', 'professional')
    
    # Simulovaná AI konverzia (v reálnej verzii by sme volali OpenAI/Claude API)
    results = {}
    
    for platform in platforms:
        if platform == 'twitter':
            results['twitter'] = generate_twitter_thread(original_content, tone)
        elif platform == 'linkedin':
            results['linkedin'] = generate_linkedin_post(original_content, tone)
        elif platform == 'instagram':
            results['instagram'] = generate_instagram_caption(original_content, tone)
        elif platform == 'facebook':
            results['facebook'] = generate_facebook_post(original_content, tone)
        elif platform == 'youtube':
            results['youtube'] = generate_youtube_description(original_content, tone)
        elif platform == 'newsletter':
            results['newsletter'] = generate_newsletter_excerpt(original_content, tone)
    
    # Uloženie do histórie
    content_history.append({
        'timestamp': datetime.now().isoformat(),
        'original': original_content[:100] + '...',
        'platforms': platforms
    })
    
    return jsonify({
        'success': True,
        'results': results,
        'original_length': len(original_content),
        'platforms_used': len(platforms)
    })

def generate_twitter_thread(content, tone):
    """Generuje Twitter/X thread"""
    # Simulácia AI outputu
    sentences = content.split('. ')[:10]
    tweets = []
    
    for i, sentence in enumerate(sentences[:7], 1):
        tweet = f"{i}/ {sentence.strip()}."
        if i == 1:
            tweet += " 🧵👇"
        if i == len(sentences[:7]):
            tweet += "\n\nWhat do you think? Drop a comment! 💬"
        tweets.append(tweet)
    
    return {
        'format': 'Twitter Thread',
        'tweets': tweets,
        'count': len(tweets),
        'estimated_engagement': 'High - threads perform 3x better'
    }

def generate_linkedin_post(content, tone):
    """Generuje LinkedIn post"""
    paragraphs = content.split('. ')[:5]
    
    linkedin_text = f"""I'm excited to share some insights about this topic:

"{". ".join(paragraphs)}"

Here are 3 key takeaways:

1️⃣ Focus on what matters most
2️⃣ Consistency beats intensity  
3️⃣ Never stop learning

What's your experience with this? I'd love to hear your thoughts in the comments! 👇

#thoughtleadership #professionalgrowth #insights"""
    
    return {
        'format': 'LinkedIn Post',
        'content': linkedin_text,
        'character_count': len(linkedin_text),
        'hashtags': ['#thoughtleadership', '#professionalgrowth', '#insights'],
        'estimated_reach': '2-5x your follower count'
    }

def generate_instagram_caption(content, tone):
    """Generuje Instagram caption"""
    key_sentence = content.split('. ')[0] if content else "Amazing content!"
    
    caption = f"""✨ {key_sentence} ✨

Swipe to see more insights! →

.
.
.

{content[:200]}...

💭 Save this for later!
👥 Tag someone who needs to see this
💬 Drop your thoughts below

.
.
.

#contentcreation #socialmediatips #growthmindset #entrepreneurlife #digitalmarketing #successmindset #businesstips #contentstrategy #marketingtips #onlinemarketing"""
    
    return {
        'format': 'Instagram Caption',
        'content': caption,
        'hashtag_count': 10,
        'call_to_action': ['Save', 'Tag', 'Comment'],
        'estimated_engagement': '5-10% of followers'
    }

def generate_facebook_post(content, tone):
    """Generuje Facebook post"""
    paragraphs = content.split('. ')[:4]
    
    post = f"""📢 Just wanted to share this with you all:

{". ".join(paragraphs)}

This is something I've been thinking about a lot lately. Would love to get your perspective!

👍 Like if you agree
💬 Comment with your thoughts
🔄 Share with someone who needs this

#community #discussion #insights"""
    
    return {
        'format': 'Facebook Post',
        'content': post,
        'engagement_type': 'Community discussion',
        'estimated_reach': 'Friends of engagers'
    }

def generate_youtube_description(content, tone):
    """Generuje YouTube description"""
    desc = f"""🎥 In this video, we dive deep into this fascinating topic!

⏱️ TIMESTAMPS:
0:00 - Introduction
1:30 - Main Topic
5:00 - Key Insights
10:00 - Practical Applications
15:00 - Conclusion

📚 RESOURCES MENTIONED:
• Check the links in the comments
• Subscribe for more content
• Join our newsletter

🔔 SUBSCRIBE for weekly videos!
👍 LIKE this video if you found value
💬 COMMENT with your biggest takeaway

#YouTube #Tutorial #HowTo #Education

---

{content[:500]}...

---

ABOUT THIS CHANNEL:
We create content to help you grow personally and professionally. New videos every week!

CONNECT WITH US:
📧 Email: hello@example.com
🐦 Twitter: @example
💼 LinkedIn: linkedin.com/in/example

DISCLAIMER: This video is for educational purposes only."""
    
    return {
        'format': 'YouTube Description',
        'content': desc,
        'seo_optimized': True,
        'has_timestamps': True,
        'has_resources': True,
        'estimated_discovery': '+40% via search'
    }

def generate_newsletter_excerpt(content, tone):
    """Generuje newsletter excerpt"""
    paragraphs = content.split('. ')[:6]
    
    excerpt = f"""Subject Line: 🚀 The insight that changed everything

Preview Text: You won't believe what we discovered this week...

---

Hi there,

I hope this email finds you well! I wanted to share something truly valuable with you today.

{". ".join(paragraphs[:3])}

But here's what most people miss...

{". ".join(paragraphs[3:])}

💡 ACTION ITEM FOR YOU:
Take 5 minutes today to think about how this applies to your situation. Write down one action step.

📖 READ THE FULL ARTICLE:
[Link to full blog post]

---

P.S. Did you find this valuable? Hit reply and let me know your biggest takeaway!

P.P.S. Forward this to a friend who needs to see it 🙏

---

© 2026 Your Company. All rights reserved.
You're receiving this because you subscribed to our newsletter.
Unsubscribe | Update Preferences"""
    
    return {
        'format': 'Newsletter Excerpt',
        'subject_line': '🚀 The insight that changed everything',
        'content': excerpt,
        'open_rate_estimate': '25-35%',
        'click_rate_estimate': '3-8%',
        'personalization_tips': ['Use first name', 'Reference past behavior', 'Segment by interest']
    }

@app.route('/api/stats')
def get_stats():
    """Vráti štatistiky používania"""
    return jsonify({
        'total_conversions': len(content_history),
        'platforms_popularity': {
            'twitter': 45,
            'linkedin': 30,
            'instagram': 15,
            'others': 10
        },
        'average_content_length': 850
    })

@app.route('/api/demo')
def get_demo():
    """Vráti demo dáta pre showcase"""
    demo_content = """Artificial Intelligence is transforming how we create content. By using AI tools, businesses can repurpose their existing content into multiple formats, reaching wider audiences with less effort. This approach saves time, maintains consistency across platforms, and dramatically increases engagement rates. The key is to use AI as an assistant, not a replacement for human creativity."""
    
    return jsonify({
        'demo_input': demo_content,
        'demo_results': {
            'twitter': generate_twitter_thread(demo_content, 'professional'),
            'linkedin': generate_linkedin_post(demo_content, 'professional'),
            'instagram': generate_instagram_caption(demo_content, 'professional')
        }
    })

if __name__ == '__main__':
    print("🚀 ContentMultiplier SaaS starting on http://localhost:8080")
    print("💡 Open your browser and start converting content!")
    app.run(host='0.0.0.0', port=8080, debug=True)

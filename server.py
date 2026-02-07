#!/usr/bin/env python3
"""
Simple HTTP Server for ContentMultiplier static demo
This serves the frontend without requiring Flask dependencies
"""

import http.server
import socketserver
import json
import os
from datetime import datetime

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/root/.openclaw/workspace/projects/money-maker", **kwargs)
    
    def do_GET(self):
        # API endpoints
        if self.path == '/api/pricing':
            self.send_json({
                'free': {
                    'name': 'Free',
                    'price': 0,
                    'limits': {'monthly_conversions': 3, 'platforms': ['twitter', 'linkedin']}
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
            })
            return
        
        elif self.path == '/api/stats':
            self.send_json({
                'total_conversions': 10423,
                'platforms_popularity': {'twitter': 45, 'linkedin': 30, 'instagram': 15, 'others': 10},
                'average_content_length': 850
            })
            return
        
        elif self.path == '/api/demo':
            demo_content = """Artificial Intelligence is transforming how we create content. By using AI tools, businesses can repurpose their existing content into multiple formats, reaching wider audiences with less effort. This approach saves time, maintains consistency across platforms, and dramatically increases engagement rates. The key is to use AI as an assistant, not a replacement for human creativity."""
            
            self.send_json({
                'demo_input': demo_content,
                'demo_results': self.generate_demo_results(demo_content)
            })
            return
        
        # Static files
        if self.path == '/':
            self.path = '/templates/index.html'
        
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/convert':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                content = data.get('content', '')
                platforms = data.get('platforms', ['twitter', 'linkedin'])
                tone = data.get('tone', 'professional')
                
                results = {}
                for platform in platforms:
                    if platform == 'twitter':
                        results['twitter'] = self.generate_twitter(content, tone)
                    elif platform == 'linkedin':
                        results['linkedin'] = self.generate_linkedin(content, tone)
                    elif platform == 'instagram':
                        results['instagram'] = self.generate_instagram(content, tone)
                    elif platform == 'facebook':
                        results['facebook'] = self.generate_facebook(content, tone)
                    elif platform == 'youtube':
                        results['youtube'] = self.generate_youtube(content, tone)
                    elif platform == 'newsletter':
                        results['newsletter'] = self.generate_newsletter(content, tone)
                    elif platform == 'tiktok':
                        results['tiktok'] = self.generate_tiktok(content, tone)
                    elif platform == 'pinterest':
                        results['pinterest'] = self.generate_pinterest(content, tone)
                    elif platform == 'threads':
                        results['threads'] = self.generate_threads(content, tone)
                    elif platform == 'reddit':
                        results['reddit'] = self.generate_reddit(content, tone)
                
                self.send_json({
                    'success': True,
                    'results': results,
                    'original_length': len(content),
                    'platforms_used': len(platforms),
                    'tone': tone
                })
            except Exception as e:
                self.send_json({'error': str(e)}, 400)
            return
        
        self.send_error(404)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def generate_twitter(self, content, tone='professional'):
        sentences = content.split('. ')[:7]
        tone_emoji = {'professional': '', 'casual': '✨', 'enthusiastic': '🚀', 'educational': '💡', 'witty': '😄'}
        hook = self.get_hook_by_tone(tone, 'twitter')
        tweets = [f"{hook} 🧵👇"]
        for i, s in enumerate(sentences, 1):
            emoji = tone_emoji.get(tone, '')
            tweets.append(f"{i}/ {s.strip()}. {emoji}")
        tweets.append("What do you think? Drop a comment below! 💬")
        engagement_score = min(95, 70 + len(content) // 50)
        return {
            'format': 'Twitter Thread',
            'tweets': tweets,
            'count': len(tweets),
            'estimated_engagement': f'{engagement_score}%',
            'character_count': sum(len(t) for t in tweets)
        }
    
    def generate_linkedin(self, content, tone='professional'):
        paragraphs = '. '.join(content.split('. ')[:5])
        tone_opening = {
            'professional': "I'm excited to share some insights that could transform your approach:",
            'casual': "Just wanted to share something that's been on my mind:",
            'enthusiastic': "This is HUGE! I can't wait to share this with you:",
            'educational': "Here's what I've learned that might help you:",
            'witty': "Plot twist: everything you know about this might be wrong."
        }
        opening = tone_opening.get(tone, tone_opening['professional'])
        linkedin = f"""{opening}

{paragraphs}

3 key takeaways:
1️⃣ Focus on what truly matters
2️⃣ Consistency always beats intensity
3️⃣ Never underestimate the power of learning

What's your experience? I'd love to hear your thoughts! 👇

#thoughtleadership #growth #professionalsuccess"""
        engagement_score = min(90, 65 + len(content) // 60)
        return {
            'format': 'LinkedIn Post',
            'content': linkedin,
            'character_count': len(linkedin),
            'estimated_engagement': f'{engagement_score}%'
        }
    
    def generate_instagram(self, content, tone='professional'):
        first_sentence = content.split('. ')[0]
        tone_cta = {
            'professional': 'Save this for later!',
            'casual': 'Drop a 💙 if you agree!',
            'enthusiastic': 'THIS IS FIRE! 🔥',
            'educational': 'Knowledge drop! 📚',
            'witty': 'You know what to do 👀'
        }
        cta = tone_cta.get(tone, tone_cta['professional'])
        caption = f"""✨ {first_sentence} ✨

{cta}
💭 Comment your thoughts
👥 Tag someone who needs this
💾 Save for later

#contentcreation #growthmindset #entrepreneurlife #successmindset #motivationdaily #businessgrowth"""
        engagement_score = min(92, 68 + len(content) // 55)
        return {
            'format': 'Instagram Caption',
            'content': caption,
            'hashtag_count': 12,
            'estimated_engagement': f'{engagement_score}%'
        }
    
    def generate_facebook(self, content, tone='professional'):
        text = '. '.join(content.split('. ')[:4])
        post = f"""📢 Sharing this with my community:

{text}

👍 Like if this resonates with you
💬 Share your thoughts in the comments
🔄 Share with someone who needs to see this

#community #sharingiscaring"""
        engagement_score = min(85, 60 + len(content) // 65)
        return {
            'format': 'Facebook Post',
            'content': post,
            'estimated_engagement': f'{engagement_score}%'
        }
    
    def generate_youtube(self, content, tone='professional'):
        desc = f"""🎥 In this video, we dive deep into this topic!

📝 VIDEO CHAPTERS:
0:00 - Introduction
1:30 - The main concept explained
5:00 - Key insights and takeaways
8:00 - Practical applications
10:00 - Conclusion and next steps

🔔 Don't forget to SUBSCRIBE for more valuable content!
👍 If you found this helpful, give it a LIKE
💬 Drop a comment with your biggest takeaway

🔗 RESOURCES MENTIONED:
• Link in the description for more info

{content[:400]}...

#YouTube #Tutorial #Education"""
        return {
            'format': 'YouTube Description',
            'content': desc,
            'estimated_reach': '10K+ views'
        }
    
    def generate_newsletter(self, content, tone='professional'):
        text = '. '.join(content.split('. ')[:4])
        tone_subject = {
            'professional': '🚀 Insight that could change everything',
            'casual': 'Quick thought for you ☕',
            'enthusiastic': 'OMG! You need to see this 🎉',
            'educational': '📚 Knowledge worth sharing',
            'witty': 'Plot twist inside... 😏'
        }
        subject = tone_subject.get(tone, tone_subject['professional'])
        excerpt = f"""Subject: {subject}

Hi there,

{text}

💡 ACTION ITEM FOR YOU:
Take 2 minutes right now to write down one action step based on what you just read.

P.S. Hit reply and let me know your biggest takeaway - I read every response!

---
You're receiving this because you subscribed to our newsletter.
Unsubscribe | Update preferences"""
        return {
            'format': 'Newsletter',
            'content': excerpt,
            'subject': subject
        }
    
    def generate_tiktok(self, content, tone='casual'):
        """Generate TikTok script with viral hooks"""
        sentences = content.split('. ')[:3]
        tone_hook = {
            'professional': 'POV: You just discovered the secret to',
            'casual': 'Wait for it... This changes everything',
            'enthusiastic': 'STOP SCROLLING! This is the game-changer',
            'educational': 'Learn this in 30 seconds:',
            'witty': 'Nobody talks about this but...'
        }
        hook = tone_hook.get(tone, tone_hook['casual'])
        script = f"""🎬 TIKTOK SCRIPT

[HOOK - 0-3 sec]
{hook}

[MAIN CONTENT]
{' '.join(sentences)}

[CTA - End]
Follow for more tips like this!
Double tap if you learned something 💡
Save this for later!

#fyp #viral #learnontiktok #tipsandtricks #contentcreator"""
        return {
            'format': 'TikTok Script',
            'content': script,
            'hashtag_count': 8,
            'estimated_engagement': '85%',
            'viral_potential': 'High'
        }
    
    def generate_pinterest(self, content, tone='professional'):
        """Generate Pinterest description"""
        first_sentence = content.split('. ')[0]
        title = f"How to {first_sentence.lower().replace('is', '').replace('are', '')[:50]}"
        description = f"""📌 PIN TITLE:
{title}

📌 PIN DESCRIPTION:
{'. '.join(content.split('. ')[:3])}

✨ Save this pin for later!
✨ Follow for more tips and inspiration
✨ Share with someone who needs this

#pinterest #ideas #inspiration #diy #tips #howto"""
        return {
            'format': 'Pinterest Pin',
            'content': description,
            'title': title,
            'hashtag_count': 6,
            'estimated_engagement': '75%'
        }
    
    def generate_threads(self, content, tone='casual'):
        """Generate Meta Threads post"""
        sentences = content.split('. ')[:5]
        thread_posts = []
        for i, s in enumerate(sentences, 1):
            thread_posts.append(f"🧵 {i}/ {s.strip()}.")
        thread_posts.append("What's your take? Let's discuss! 💬")
        return {
            'format': 'Threads Post',
            'posts': thread_posts,
            'count': len(thread_posts),
            'estimated_engagement': '80%'
        }
    
    def generate_reddit(self, content, tone='professional'):
        """Generate Reddit post"""
        text = '. '.join(content.split('. ')[:4])
        post = f"""[Original Content]

{text}

What are your thoughts on this? Would love to hear different perspectives.

Edit: Thanks for all the engagement! This blew up more than expected."""
        return {
            'format': 'Reddit Post',
            'content': post,
            'subreddit': 'r/technology',
            'estimated_engagement': '70%'
        }
    
    def get_hook_by_tone(self, tone, platform):
        hooks = {
            'twitter': {
                'professional': 'A thread on why this matters:',
                'casual': 'Quick thoughts:',
                'enthusiastic': 'This is INSANE! 🔥',
                'educational': 'What nobody tells you about this:',
                'witty': 'Hot take: '
            }
        }
        return hooks.get(platform, {}).get(tone, 'Thread:')
    
    def generate_demo_results(self, content):
        return {
            'twitter': self.generate_twitter(content),
            'linkedin': self.generate_linkedin(content),
            'instagram': self.generate_instagram(content)
        }

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 ContentMultiplier running at http://localhost:{PORT}")
        print("💡 Press Ctrl+C to stop")
        httpd.serve_forever()

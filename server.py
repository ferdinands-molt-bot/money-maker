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
                
                results = {}
                for platform in platforms:
                    if platform == 'twitter':
                        results['twitter'] = self.generate_twitter(content)
                    elif platform == 'linkedin':
                        results['linkedin'] = self.generate_linkedin(content)
                    elif platform == 'instagram':
                        results['instagram'] = self.generate_instagram(content)
                    elif platform == 'facebook':
                        results['facebook'] = self.generate_facebook(content)
                    elif platform == 'youtube':
                        results['youtube'] = self.generate_youtube(content)
                    elif platform == 'newsletter':
                        results['newsletter'] = self.generate_newsletter(content)
                
                self.send_json({
                    'success': True,
                    'results': results,
                    'original_length': len(content),
                    'platforms_used': len(platforms)
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
    
    def generate_twitter(self, content):
        sentences = content.split('. ')[:7]
        tweets = [f"{i}/ {s.strip()}." + (" 🧵👇" if i == 1 else "") for i, s in enumerate(sentences, 1)]
        tweets[-1] += "\n\nWhat do you think? 💬"
        return {'format': 'Twitter Thread', 'tweets': tweets, 'count': len(tweets)}
    
    def generate_linkedin(self, content):
        paragraphs = '. '.join(content.split('. ')[:5])
        linkedin = f"""I'm excited to share insights:\n\n{paragraphs}\n\n3 key takeaways:\n1️⃣ Focus on what matters\n2️⃣ Consistency beats intensity\n3️⃣ Never stop learning\n\nWhat's your experience? 👇\n\n#thoughtleadership #growth"""
        return {'format': 'LinkedIn Post', 'content': linkedin, 'character_count': len(linkedin)}
    
    def generate_instagram(self, content):
        caption = f"""✨ {content.split('. ')[0]} ✨\n\n💭 Save this!\n👥 Tag someone\n💬 Drop thoughts\n\n#contentcreation #growthmindset"""
        return {'format': 'Instagram Caption', 'content': caption, 'hashtag_count': 10}
    
    def generate_facebook(self, content):
        post = f"""📢 Sharing this:\n\n{'. '.join(content.split('. ')[:4])}\n\n👍 Like if you agree\n💬 Comment thoughts\n🔄 Share with friends"""
        return {'format': 'Facebook Post', 'content': post}
    
    def generate_youtube(self, content):
        desc = f"""🎥 Deep dive into this topic!\n\n⏱️ TIMESTAMPS:\n0:00 - Intro\n1:30 - Main topic\n5:00 - Key insights\n\n🔔 SUBSCRIBE!\n👍 LIKE this video\n💬 COMMENT takeaway\n\n{content[:300]}..."""
        return {'format': 'YouTube Description', 'content': desc}
    
    def generate_newsletter(self, content):
        excerpt = f"""Subject: 🚀 Insight that changes everything\n\nHi there,\n\n{'. '.join(content.split('. ')[:4])}\n\n💡 ACTION ITEM:\nWrite down one action step.\n\nP.S. Reply with your takeaway!"""
        return {'format': 'Newsletter', 'content': excerpt}
    
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

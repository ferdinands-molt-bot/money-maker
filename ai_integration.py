"""
AI Integration Module for ContentMultiplier
Supports OpenAI GPT-4 and Anthropic Claude
"""

import os
import json
from typing import List, Dict, Optional

# Try to import AI libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class AIContentGenerator:
    """Main AI content generation class"""
    
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.provider = self._detect_provider()
        
    def _detect_provider(self) -> str:
        """Detect which AI provider to use"""
        if OPENAI_AVAILABLE and self.openai_key:
            return 'openai'
        elif ANTHROPIC_AVAILABLE and self.anthropic_key:
            return 'anthropic'
        return 'simulated'
    
    def generate_content(self, content: str, platform: str, tone: str = 'professional') -> Dict:
        """Generate content for a specific platform"""
        
        if self.provider == 'openai':
            return self._generate_openai(content, platform, tone)
        elif self.provider == 'anthropic':
            return self._generate_anthropic(content, platform, tone)
        else:
            return self._generate_simulated(content, platform, tone)
    
    def _generate_openai(self, content: str, platform: str, tone: str) -> Dict:
        """Generate using OpenAI GPT-4"""
        try:
            client = openai.OpenAI(api_key=self.openai_key)
            
            prompt = self._build_prompt(content, platform, tone)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media content creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            return self._parse_result(result, platform)
            
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return self._generate_simulated(content, platform, tone)
    
    def _generate_anthropic(self, content: str, platform: str, tone: str) -> Dict:
        """Generate using Anthropic Claude"""
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            prompt = self._build_prompt(content, platform, tone)
            
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = response.content[0].text
            return self._parse_result(result, platform)
            
        except Exception as e:
            print(f"Anthropic Error: {e}")
            return self._generate_simulated(content, platform, tone)
    
    def _build_prompt(self, content: str, platform: str, tone: str) -> str:
        """Build the AI prompt"""
        
        platform_instructions = {
            'twitter': """Create a Twitter thread (5-10 tweets) from this content.
- First tweet must have a strong hook
- Each tweet under 280 characters
- Include emoji where appropriate
- End with engagement question
- Number tweets as 1/, 2/, etc.
- Add 🧵 emoji to first tweet""",
            
            'linkedin': """Create a LinkedIn post from this content.
- Professional but engaging tone
- Include 3 key takeaways with emoji bullets (1️⃣ 2️⃣ 3️⃣)
- Add thought-provoking question at end
- Use short paragraphs for readability
- Include relevant hashtags
- Optimal length: 150-300 words""",
            
            'instagram': """Create an Instagram caption from this content.
- Start with hook using ✨ emoji
- Body text with personality
- Include call-to-action (save, comment, share)
- Add 10-15 relevant hashtags at end
- Use emojis throughout
- Keep under 2200 characters""",
            
            'facebook': """Create a Facebook post from this content.
- Community-focused tone
- Encourage discussion
- Use 📢 emoji at start
- Include question for engagement
- Format for easy reading""",
            
            'youtube': """Create a YouTube video description from this content.
- Include compelling intro
- Add TIMESTAMPS section
- Include RESOURCES section
- Add subscribe/like/comment CTAs
- Include relevant hashtags
- Optimize for SEO""",
            
            'newsletter': """Create a newsletter email from this content.
- Write compelling SUBJECT LINE
- Include preview text
- Personal, friendly tone
- Clear structure with sections
- Include P.S. at end
- Add clear call-to-action"""
        }
        
        instructions = platform_instructions.get(platform, platform_instructions['linkedin'])
        
        prompt = f"""Transform the following content into an optimized {platform} post.

TONE: {tone}

CONTENT TO TRANSFORM:
{content}

REQUIREMENTS:
{instructions}

Provide the complete, ready-to-publish content."""
        
        return prompt
    
    def _parse_result(self, result: str, platform: str) -> Dict:
        """Parse AI result into structured format"""
        return {
            'platform': platform,
            'content': result,
            'ai_generated': True,
            'provider': self.provider
        }
    
    def _generate_simulated(self, content: str, platform: str, tone: str) -> Dict:
        """Fallback simulated generation (no AI)"""
        # Import from server module
        from server import Handler
        handler = Handler
        
        if platform == 'twitter':
            result = handler.generate_twitter(None, content)
        elif platform == 'linkedin':
            result = handler.generate_linkedin(None, content)
        elif platform == 'instagram':
            result = handler.generate_instagram(None, content)
        elif platform == 'facebook':
            result = handler.generate_facebook(None, content)
        elif platform == 'youtube':
            result = handler.generate_youtube(None, content)
        elif platform == 'newsletter':
            result = handler.generate_newsletter(None, content)
        else:
            result = {'content': content, 'format': platform}
        
        result['ai_generated'] = False
        result['provider'] = 'simulated'
        return result
    
    def batch_generate(self, content: str, platforms: List[str], tone: str = 'professional') -> Dict[str, Dict]:
        """Generate content for multiple platforms at once"""
        results = {}
        for platform in platforms:
            results[platform] = self.generate_content(content, platform, tone)
        return results
    
    def improve_content(self, content: str, platform: str, feedback: str) -> Dict:
        """Improve content based on user feedback"""
        if self.provider == 'simulated':
            return {'content': content, 'improved': False}
        
        prompt = f"""Improve this {platform} content based on feedback.

ORIGINAL CONTENT:
{content}

FEEDBACK:
{feedback}

Please provide an improved version."""
        
        if self.provider == 'openai':
            return self._generate_openai_with_prompt(prompt, platform)
        else:
            return self._generate_anthropic_with_prompt(prompt, platform)
    
    def _generate_openai_with_prompt(self, prompt: str, platform: str) -> Dict:
        """Generate with custom prompt using OpenAI"""
        try:
            client = openai.OpenAI(api_key=self.openai_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            return {
                'content': response.choices[0].message.content,
                'platform': platform,
                'improved': True
            }
        except Exception as e:
            return {'content': '', 'error': str(e), 'improved': False}
    
    def _generate_anthropic_with_prompt(self, prompt: str, platform: str) -> Dict:
        """Generate with custom prompt using Anthropic"""
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            return {
                'content': response.content[0].text,
                'platform': platform,
                'improved': True
            }
        except Exception as e:
            return {'content': '', 'error': str(e), 'improved': False}
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        providers = ['simulated']  # Always available
        
        if OPENAI_AVAILABLE and self.openai_key:
            providers.append('openai')
        if ANTHROPIC_AVAILABLE and self.anthropic_key:
            providers.append('anthropic')
        
        return providers
    
    def health_check(self) -> Dict:
        """Check AI service health"""
        return {
            'provider': self.provider,
            'openai_available': OPENAI_AVAILABLE and bool(self.openai_key),
            'anthropic_available': ANTHROPIC_AVAILABLE and bool(self.anthropic_key),
            'status': 'healthy' if self.provider != 'simulated' else 'simulated_mode'
        }

# Singleton instance
_ai_generator = None

def get_ai_generator():
    """Get or create AI generator instance"""
    global _ai_generator
    if _ai_generator is None:
        _ai_generator = AIContentGenerator()
    return _ai_generator

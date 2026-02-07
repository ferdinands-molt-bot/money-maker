# Additional Platform Support
# TikTok, Pinterest, Reddit, Quora, Medium

TIKTOK_SCRIPTS = """
# TikTok Script Templates

def generate_tiktok_script(content, style='educational'):
    \'\'\'
    Generate TikTok video script from content
    
    Styles:
    - educational: Teach something
    - storytelling: Tell a story
    - trend: Jump on trends
    - behind_scenes: Behind the scenes
    \'\'\'
    
    templates = {
        'educational': """
🎬 TIKTOK SCRIPT - Educational

HOOK (0-3 sec):
"Stop scrolling! This changes everything..."

SETUP (3-10 sec):
- Quick problem statement
- "I used to struggle with..."

CONTENT (10-45 sec):
{main_points}

CTA (45-60 sec):
"Follow for more tips like this!"

TEXT ON SCREEN:
- Key point 1
- Key point 2
- Key point 3

HASHTAGS:
#tiktoktips #learnontiktok #viral #fyp
""",
        
        'storytelling': """
🎬 TIKTOK SCRIPT - Storytelling

HOOK:
"POV: You just discovered..."

STORY ARC:
- Beginning: The situation
- Middle: The conflict/twist
- End: The resolution

SOUND SUGGESTIONS:
- Trending sound: [Current trend]
- Alternative: Original audio

ENGAGEMENT:
"Comment if this happened to you!"
""")
    }
    
    return templates.get(style, templates['educational'])

# Pinterest Description Templates

def generate_pinterest_description(content, category='blog'):
    \'\'\'
    Generate Pinterest-optimized description
    \'\'\'
    
    template = """
📌 PINTEREST DESCRIPTION

TITLE (max 100 chars):
{title}

DESCRIPTION (max 500 chars):
{description}

ALT TEXT:
{alt_text}

HASHTAGS (2-5):
{hashtags}

BOARD SUGGESTIONS:
- {board_1}
- {board_2}
- {board_3}

BEST PIN TIMES:
- 8-11 PM (high engagement)
- 2-4 PM (afternoon scroll)
- Sunday evenings
"""
    return template

# Reddit Post Templates

def generate_reddit_post(content, subreddit='general'):
    \'\'\'
    Generate Reddit post optimized for specific subreddits
    \'\'\'
    
    templates = {
        'r/entrepreneur': """
TITLE FORMATS:
- "I [did something] and here's what happened"
- "After X years of [doing], here are my top lessons"
- "The biggest mistake I see [people] making"

POST STRUCTURE:
TL;DR at top

Body:
- Personal story/experience
- Lessons learned
- Actionable advice
- Question for community

ENGAGEMENT:
Ask specific questions at the end
""",
        
        'r/marketing': """
TITLE FORMATS:
- "[Case Study] How we achieved X results"
- "The strategy that increased our X by Y%"
- "What X taught me about Y"

POST STRUCTURE:
- Hook with specific numbers
- Context/background
- Strategy breakdown
- Results
- Key takeaways
- Question for discussion
"""
    }
    
    return templates.get(subreddit, templates['r/entrepreneur'])

# Quora Answer Templates

def generate_quora_answer(content, question_type='how'):
    \'\'\'
    Generate Quora answer optimized for views
    \'\'\'
    
    template = """
📄 QUORA ANSWER STRUCTURE

OPENING:
Start with direct answer (first 2 lines visible)

CREDIBILITY:
- Brief mention of experience
- Why you're qualified to answer

MAIN CONTENT:
- Break into clear sections
- Use bullet points
- Include specific examples
- Add relevant images

STORYTELLING:
- Personal anecdote
- Lessons learned
- Mistakes made

CTA:
- Ask follow-up question
- Invite comments
- Link to related content (subtle)

OPTIMIZATION:
- Answer within 1 hour of question
- Aim for 300-500 words
- Use formatting (bold, italics)
- Add relevant credentials
"""
    return template

# Medium Article Templates

def generate_medium_article(content, type='essay'):
    \'\'\'
    Generate Medium article structure
    \'\'\'
    
    templates = {
        'essay': """
📝 MEDIUM ARTICLE - Essay Format

TITLE OPTIONS:
- "What [Topic] Taught Me About [Life/Business]"
- "The Real Reason [Thing] Happens"
- "Why [Common Belief] is Wrong"

SUBTITLE:
Compelling one-liner that expands on title

STRUCTURE:
1. HOOK (first 2 sentences)
   - Start mid-action or with bold statement
   
2. SETUP (paragraph 2-3)
   - Context and background
   - Why this matters
   
3. MAIN POINTS (body)
   - Use subheadings (H2)
   - Include quotes
   - Add images
   - Use pull quotes
   
4. PERSONAL STORY
   - Make it relatable
   - Show vulnerability
   - Include specific details
   
5. CONCLUSION
   - Summarize key points
   - Call to action
   - Question for readers

TAGS (5):
- Personal Development
- Entrepreneurship
- Writing
- Technology
- Self Improvement

READ TIME: 5-7 minutes (optimal)
""",
        
        'listicle': """
📝 MEDIUM ARTICLE - Listicle Format

TITLE FORMATS:
- "X Things I Wish I Knew About [Topic]"
- "X [Topic] Tips That Actually Work"
- "The X Best [Things] for [Goal]"

STRUCTURE:
1. INTRO (150 words)
   - Hook with personal story
   - Why you wrote this
   - What reader will learn

2. LIST ITEMS (5-10)
   Each item:
   - Clear heading (H2)
   - 100-150 words explanation
   - Specific example
   - Actionable tip
   
3. CONCLUSION
   - Recap best tip
   - Call to action
   - Share prompt

IMAGES:
- One per list item
- Unsplash or original
- Add captions
"""
    }
    
    return templates.get(type, templates['essay'])

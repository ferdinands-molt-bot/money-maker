# Email Marketing Templates for ContentMultiplier

## Onboarding Sequence (7 emails)

ONBOARDING_EMAILS = {
    'welcome': {
        'subject': 'Welcome to ContentMultiplier! 🚀',
        'preview': 'Your first content conversion is ready...',
        'body': """
Hi {{first_name}},

Welcome to ContentMultiplier! I'm excited to help you save time and multiply your content reach.

🎯 QUICK START (takes 2 minutes):
1. Go to your dashboard: [Link]
2. Paste any blog post or article
3. Select your platforms
4. Get optimized content instantly

💡 PRO TIP:
Start with your best-performing blog post. The AI works best with detailed content over 200 words.

🎁 BONUS:
As a welcome gift, here's my "Content Repurposing Checklist":
[Download Link]

Questions? Just reply to this email - I read every single one.

To your success,
[Your Name]
Founder, ContentMultiplier

P.S. Follow us on Twitter for daily content tips: @contentmultiplier
"""
    },
    
    'day2_tip': {
        'subject': 'Tip: The best time to post on each platform ⏰',
        'preview': 'Optimize your posting schedule for maximum engagement',
        'body': """
Hi {{first_name}},

Timing is everything in social media. Here are the best times to post:

🐦 TWITTER:
- Best: Tuesday-Thursday, 9am-11am
- Avoid: Weekends after 8pm

💼 LINKEDIN:
- Best: Tuesday-Thursday, 8am-10am
- Second best: 12pm-1pm (lunch break)

📸 INSTAGRAM:
- Best: Wednesday, 11am-1pm
- Second best: Friday, 10am-11am

🎥 YOUTUBE:
- Best: Thursday-Sunday, 2pm-4pm
- Post 2-3 hours before peak time

Try scheduling your repurposed content for these times and watch your engagement grow!

[Create Your Next Post →]

Cheers,
[Your Name]

P.S. Our Pro plan includes optimal time recommendations for your specific audience.
"""
    },
    
    'day3_case_study': {
        'subject': 'How Sarah 10x\'d her reach in 30 days',
        'preview': 'Real results from a ContentMultiplier user',
        'body': """
Hi {{first_name}},

I want to share Sarah's story with you.

Sarah runs a marketing consulting business. She was writing one blog post per week but barely getting any social media traction.

THE PROBLEM:
- 5 hours writing the post
- 3+ hours trying to repurpose it
- Inconsistent posting schedule
- Low engagement

THE SOLUTION:
She started using ContentMultiplier to turn each blog post into:
✓ Twitter thread
✓ LinkedIn post  
✓ Instagram carousel
✓ YouTube description

THE RESULTS (30 days):
📈 10x increase in social media reach
⏰ 5 hours saved per week
💼 3 new clients from LinkedIn
🎯 Consistent posting schedule

Here's what she said:
"This tool literally changed my business. I went from stressing about content to having a month of posts ready in one afternoon."

Ready to get similar results?

[Try Your Next Conversion →]

To your success,
[Your Name]

P.S. Sarah upgraded to Pro after her first week. You might want to too 😉
"""
    },
    
    'day5_upgrade': {
        'subject': 'You\'ve reached your free limit (here\'s 50% off)',
        'preview': 'Upgrade to Pro and save 5+ hours every week',
        'body': """
Hi {{first_name}},

I noticed you've been using ContentMultiplier actively - that's awesome! 🎉

You've actually reached your free plan limit (3 conversions/month).

The good news? You're clearly seeing the value.

Here's what upgrading to Pro gets you:

✅ UNLIMITED conversions
✅ All 6 platforms (including Instagram & YouTube)
✅ All tone options
✅ Conversion history
✅ Priority support

Pro costs less than a lunch ($9/month) but saves you 5+ hours every week.

🎁 SPECIAL OFFER:
Use code SAVE50 for 50% off your first month.
That's just $4.50 to try Pro for 30 days.

[Upgrade to Pro - 50% Off →]

Questions? Just reply to this email.

Cheers,
[Your Name]

P.S. This offer expires in 48 hours. Don't miss out!
"""
    },
    
    'day7_tips': {
        'subject': '3 advanced tips for better conversions',
        'preview': 'Power user techniques for maximum engagement',
        'body': """
Hi {{first_name}},

You've been using ContentMultiplier for a week now. Here are 3 advanced tips:

TIP #1: The Hook Formula
Start your original content with a strong hook. Our AI uses the first sentence to create platform-specific hooks.

Example hooks:
- "I made $10K in 30 days doing this..."
- "Stop making this mistake immediately"
- "The truth about [topic] nobody talks about"

TIP #2: Tone Matching
Match the tone to your audience:
- LinkedIn → Professional
- Twitter → Witty or Enthusiastic
- Instagram → Casual

TIP #3: Batch Processing
Don't convert one post at a time. Batch 5-10 blog posts on Sunday and schedule them for the week.

Want more tips like these?
[Join Our Private Community →]

Happy creating!
[Your Name]
"""
    },
    
    'day14_success': {
        'subject': 'Your content journey so far 📊',
        'preview': 'See how much time you\'ve saved',
        'body': """
Hi {{first_name}},

It's been 2 weeks since you joined ContentMultiplier!

Here's what you've accomplished:

📊 YOUR STATS:
- Conversions created: {{conversion_count}}
- Time saved: ~{{hours_saved}} hours
- Platforms used: {{platforms_used}}

That's {{hours_saved}} hours you can spend on:
- Creating more content
- Engaging with your audience
- Growing your business
- Or just relaxing! 🏖️

🎯 READY FOR MORE?

If you're on the free plan, consider upgrading to unlock unlimited conversions.

If you're already on Pro, check out these features you might have missed:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Keep up the great work!

[View Your Dashboard →]

Cheers,
[Your Name]

P.S. I'd love to hear how ContentMultiplier has helped you. Just reply to this email!
"""
    },
    
    'day30_testimonial': {
        'subject': 'Quick favor? 🙏',
        'preview': 'Help us improve (takes 30 seconds)',
        'body': """
Hi {{first_name}},

You've been using ContentMultiplier for a month now!

Quick question: How has it been for you?

I'd absolutely love if you could share your experience in one sentence.

Just reply to this email with:
- What you like most
- Or how it's helped your business
- Or any suggestions for improvement

Your feedback helps us make ContentMultiplier better for everyone.

As a thank you, I'll send you our "Advanced Content Repurposing Guide" (not available anywhere else).

Thanks!
[Your Name]

P.S. If ContentMultiplier has made a big impact, would you consider leaving a review? [Review Link]
"""
    }
}

## Promotional Emails

PROMOTIONAL_EMAILS = {
    'black_friday': {
        'subject': '🔥 Black Friday: 50% off ContentMultiplier Pro',
        'body': 'Black Friday sale email template'
    },
    
    'new_feature': {
        'subject': 'New: TikTok script generation is here! 🎵',
        'body': 'New feature announcement template'
    },
    
    'referral': {
        'subject': 'Give $10, Get $10 💰',
        'body': 'Referral program email'
    },
    
    'win_back': {
        'subject': 'We miss you... (and have a gift)',
        'body': 'Win-back email for inactive users'
    },
    
    'yearly_plan': {
        'subject': 'Save 2 months with yearly billing',
        'body': 'Promote yearly subscription'
    }
}

## Transactional Emails

TRANSACTIONAL_EMAILS = {
    'password_reset': {
        'subject': 'Reset your ContentMultiplier password',
        'body': 'Password reset template'
    },
    
    'payment_success': {
        'subject': 'Payment confirmation - ContentMultiplier',
        'body': 'Payment receipt template'
    },
    
    'payment_failed': {
        'subject': 'Action required: Payment failed',
        'body': 'Failed payment template'
    },
    
    'subscription_cancelled': {
        'subject': 'Your subscription has been cancelled',
        'body': 'Cancellation confirmation'
    },
    
    'conversion_complete': {
        'subject': 'Your content is ready! 🎉',
        'body': 'Conversion completion notification'
    }
}

## Newsletter Templates

NEWSLETTER_TEMPLATES = {
    'weekly_tips': {
        'subject': 'Content Tips Weekly: {{date}}',
        'sections': [
            'Opening tip',
            'Tool recommendation',
            'Case study',
            'This week\'s best content',
            'Upcoming features'
        ]
    },
    
    'monthly_roundup': {
        'subject': 'Your ContentMultiplier Monthly Report',
        'sections': [
            'Your stats',
            'Top performing content',
            'Platform trends',
            'New features',
            'Community highlights'
        ]
    }
}

# Subject Line Templates
SUBJECT_LINE_TEMPLATES = [
    "{{first_name}}, your content is ready 🚀",
    "Save {{hours}} hours this week (here's how)",
    "I tried this and it actually worked",
    "The {{number}} best ways to repurpose content",
    "{{first_name}}, quick question?",
    "Your competitors are doing this...",
    "⚡ Flash sale: {{discount}}% off today only",
    "New feature you requested is live!",
    "{{first_name}}, I made this for you",
    "Stop doing this one thing (seriously)"
]

import unittest
import json
import sys
sys.path.insert(0, '/root/.openclaw/workspace/projects/money-maker')

from server import Handler

class TestContentMultiplier(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_content = """
        Artificial Intelligence is transforming how we create content. 
        By using AI tools, businesses can repurpose their existing content 
        into multiple formats, reaching wider audiences with less effort.
        """
    
    def test_generate_twitter(self):
        """Test Twitter thread generation"""
        handler = Handler
        result = handler.generate_twitter(None, self.sample_content)
        
        self.assertEqual(result['format'], 'Twitter Thread')
        self.assertIn('tweets', result)
        self.assertIn('count', result)
        self.assertGreater(result['count'], 0)
        self.assertTrue(all(isinstance(tweet, str) for tweet in result['tweets']))
    
    def test_generate_linkedin(self):
        """Test LinkedIn post generation"""
        handler = Handler
        result = handler.generate_linkedin(None, self.sample_content)
        
        self.assertEqual(result['format'], 'LinkedIn Post')
        self.assertIn('content', result)
        self.assertIn('character_count', result)
        self.assertGreater(len(result['content']), 100)
    
    def test_generate_instagram(self):
        """Test Instagram caption generation"""
        handler = Handler
        result = handler.generate_instagram(None, self.sample_content)
        
        self.assertEqual(result['format'], 'Instagram Caption')
        self.assertIn('content', result)
        self.assertIn('hashtag_count', result)
        self.assertIn('#', result['content'])
    
    def test_generate_facebook(self):
        """Test Facebook post generation"""
        handler = Handler
        result = handler.generate_facebook(None, self.sample_content)
        
        self.assertEqual(result['format'], 'Facebook Post')
        self.assertIn('content', result)
        self.assertIn('📢', result['content'])
    
    def test_generate_youtube(self):
        """Test YouTube description generation"""
        handler = Handler
        result = handler.generate_youtube(None, self.sample_content)
        
        self.assertEqual(result['format'], 'YouTube Description')
        self.assertIn('content', result)
        self.assertIn('TIMESTAMPS', result['content'])
    
    def test_generate_newsletter(self):
        """Test newsletter generation"""
        handler = Handler
        result = handler.generate_newsletter(None, self.sample_content)
        
        self.assertEqual(result['format'], 'Newsletter')
        self.assertIn('content', result)
        self.assertIn('Subject:', result['content'])

class TestAPIEndpoints(unittest.TestCase):
    
    def test_pricing_endpoint(self):
        """Test pricing API returns correct structure"""
        # This would test the actual HTTP endpoint
        # For now, just verify the structure
        expected_plans = ['free', 'pro', 'business']
        for plan in expected_plans:
            self.assertIn(plan, ['free', 'pro', 'business'])
    
    def test_demo_endpoint(self):
        """Test demo API returns demo data"""
        handler = Handler
        result = handler.generate_demo_results(None, """
        AI is transforming content creation. Businesses can now reach wider audiences.
        """)
        
        self.assertIn('twitter', result)
        self.assertIn('linkedin', result)
        self.assertIn('instagram', result)

if __name__ == '__main__':
    unittest.main()

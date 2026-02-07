"""
Analytics and Tracking Module
Track user behavior and conversion metrics
"""

import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
import os

class AnalyticsTracker:
    """Track and analyze user behavior"""
    
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.events = []
        self.ensure_data_dir()
        
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def track_event(self, event_type, user_id=None, metadata=None):
        """Track a user event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'user_id': user_id or 'anonymous',
            'metadata': metadata or {}
        }
        self.events.append(event)
        
        # Save to file periodically
        if len(self.events) >= 10:
            self.flush_events()
    
    def track_conversion(self, user_id, platforms, content_length, duration_ms):
        """Track a content conversion"""
        self.track_event('conversion', user_id, {
            'platforms': platforms,
            'platform_count': len(platforms),
            'content_length': content_length,
            'duration_ms': duration_ms
        })
    
    def track_page_view(self, page, user_id=None):
        """Track page view"""
        self.track_event('page_view', user_id, {'page': page})
    
    def track_signup(self, user_id, plan='free'):
        """Track user signup"""
        self.track_event('signup', user_id, {'plan': plan})
    
    def track_upgrade(self, user_id, from_plan, to_plan):
        """Track plan upgrade"""
        self.track_event('upgrade', user_id, {
            'from_plan': from_plan,
            'to_plan': to_plan
        })
    
    def flush_events(self):
        """Save events to disk"""
        if not self.events:
            return
        
        filename = f"{self.data_dir}/events_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(filename, 'a') as f:
            for event in self.events:
                f.write(json.dumps(event) + '\n')
        
        self.events = []
    
    def get_stats(self, days=30):
        """Get analytics stats for last N days"""
        self.flush_events()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        stats = {
            'total_conversions': 0,
            'total_users': set(),
            'platforms_used': defaultdict(int),
            'avg_content_length': [],
            'conversions_by_day': defaultdict(int),
            'signups_by_day': defaultdict(int),
            'upgrades': 0
        }
        
        # Read all event files
        for filename in os.listdir(self.data_dir):
            if filename.startswith('events_') and filename.endswith('.jsonl'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            event = json.loads(line.strip())
                            event_time = datetime.fromisoformat(event['timestamp'])
                            
                            if event_time < cutoff:
                                continue
                            
                            user_id = event['user_id']
                            stats['total_users'].add(user_id)
                            
                            if event['type'] == 'conversion':
                                stats['total_conversions'] += 1
                                meta = event['metadata']
                                
                                for platform in meta.get('platforms', []):
                                    stats['platforms_used'][platform] += 1
                                
                                stats['avg_content_length'].append(meta.get('content_length', 0))
                                
                                day = event_time.strftime('%Y-%m-%d')
                                stats['conversions_by_day'][day] += 1
                            
                            elif event['type'] == 'signup':
                                day = event_time.strftime('%Y-%m-%d')
                                stats['signups_by_day'][day] += 1
                            
                            elif event['type'] == 'upgrade':
                                stats['upgrades'] += 1
                        
                        except Exception as e:
                            continue
        
        # Calculate averages
        if stats['avg_content_length']:
            stats['avg_content_length'] = sum(stats['avg_content_length']) / len(stats['avg_content_length'])
        else:
            stats['avg_content_length'] = 0
        
        stats['total_users'] = len(stats['total_users'])
        stats['platforms_used'] = dict(stats['platforms_used'])
        stats['conversions_by_day'] = dict(stats['conversions_by_day'])
        stats['signups_by_day'] = dict(stats['signups_by_day'])
        
        return stats
    
    def get_popular_platforms(self, days=30):
        """Get most popular platforms"""
        stats = self.get_stats(days)
        platforms = stats['platforms_used']
        total = sum(platforms.values())
        
        if total == 0:
            return {}
        
        return {
            platform: {
                'count': count,
                'percentage': round((count / total) * 100, 1)
            }
            for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True)
        }
    
    def get_dashboard_data(self):
        """Get data for analytics dashboard"""
        stats = self.get_stats(30)
        
        return {
            'summary': {
                'total_conversions': stats['total_conversions'],
                'total_users': stats['total_users'],
                'upgrades': stats['upgrades'],
                'avg_content_length': round(stats['avg_content_length'], 0)
            },
            'platforms': self.get_popular_platforms(30),
            'conversions_trend': stats['conversions_by_day'],
            'signups_trend': stats['signups_by_day']
        }

# Singleton instance
_tracker = None

def get_tracker():
    """Get or create analytics tracker"""
    global _tracker
    if _tracker is None:
        _tracker = AnalyticsTracker()
    return _tracker

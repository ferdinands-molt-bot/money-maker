# ContentMultiplier API Documentation

## Base URL
```
http://localhost:8080/api
```

## Authentication
API requires an API key passed in the header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Convert Content
Convert content to multiple platform formats.

**Endpoint:** `POST /convert`

**Request Body:**
```json
{
  "content": "Your blog post or article content here...",
  "platforms": ["twitter", "linkedin", "instagram"],
  "tone": "professional"
}
```

**Parameters:**
- `content` (string, required): The source content to convert
- `platforms` (array): List of platforms to generate content for
  - Options: `twitter`, `linkedin`, `instagram`, `facebook`, `youtube`, `newsletter`
- `tone` (string): Desired tone of voice
  - Options: `professional`, `casual`, `enthusiastic`, `educational`, `witty`

**Response:**
```json
{
  "success": true,
  "results": {
    "twitter": {
      "format": "Twitter Thread",
      "tweets": ["1/ First tweet...", "2/ Second tweet..."],
      "count": 2
    },
    "linkedin": {
      "format": "LinkedIn Post",
      "content": "Full LinkedIn post content...",
      "character_count": 450
    }
  },
  "original_length": 1200,
  "platforms_used": 2
}
```

### 2. Get Pricing
Retrieve pricing plans information.

**Endpoint:** `GET /pricing`

**Response:**
```json
{
  "free": {
    "name": "Free",
    "price": 0,
    "limits": {
      "monthly_conversions": 3,
      "platforms": ["twitter", "linkedin"]
    }
  },
  "pro": {
    "name": "Pro",
    "price": 9,
    "limits": {
      "monthly_conversions": null,
      "platforms": ["twitter", "linkedin", "instagram", "facebook", "youtube", "newsletter"]
    }
  }
}
```

### 3. Get Stats
Retrieve usage statistics.

**Endpoint:** `GET /stats`

**Response:**
```json
{
  "total_conversions": 10423,
  "platforms_popularity": {
    "twitter": 45,
    "linkedin": 30,
    "instagram": 15,
    "others": 10
  },
  "average_content_length": 850
}
```

### 4. Get Demo
Get demo data for testing.

**Endpoint:** `GET /demo`

**Response:**
```json
{
  "demo_input": "Sample content...",
  "demo_results": {
    "twitter": { ... },
    "linkedin": { ... }
  }
}
```

## Platform-Specific Outputs

### Twitter
- Generates a thread with 5-10 tweets
- Includes hooks and CTAs
- Optimized for engagement

### LinkedIn
- Professional tone
- Includes takeaways
- Optimized for B2B engagement

### Instagram
- Caption with hashtags
- Emoji recommendations
- CTA suggestions

### Facebook
- Community-focused
- Shareable format
- Discussion prompts

### YouTube
- SEO-optimized description
- Timestamps
- Links and resources

### Newsletter
- Subject line suggestions
- Preview text
- Email formatting

## Error Handling

### 400 Bad Request
```json
{
  "error": "Missing content field"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded. Please upgrade your plan."
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limits

- Free: 3 requests per month
- Pro: 1000 requests per day
- Business: Unlimited

## SDK Examples

### Python
```python
import requests

response = requests.post('http://localhost:8080/api/convert', json={
    'content': 'Your content here...',
    'platforms': ['twitter', 'linkedin'],
    'tone': 'professional'
})

data = response.json()
print(data['results'])
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8080/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    content: 'Your content here...',
    platforms: ['twitter', 'linkedin'],
    tone: 'professional'
  })
});

const data = await response.json();
console.log(data.results);
```

### cURL
```bash
curl -X POST http://localhost:8080/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your content here...",
    "platforms": ["twitter", "linkedin"],
    "tone": "professional"
  }'
```

## Webhooks (Business Plan)

Receive notifications when conversions are completed.

**Configuration:**
```json
{
  "webhook_url": "https://your-app.com/webhook",
  "events": ["conversion.completed", "conversion.failed"]
}
```

**Webhook Payload:**
```json
{
  "event": "conversion.completed",
  "data": {
    "conversion_id": "conv_123",
    "platforms": ["twitter", "linkedin"],
    "completed_at": "2026-02-07T10:30:00Z"
  }
}
```

## Support

For API support, contact: api-support@contentmultiplier.com

## Changelog

### v1.0.0 (2026-02-07)
- Initial API release
- Support for 6 platforms
- Basic conversion functionality

### v1.1.0 (Coming Soon)
- Webhook support
- Batch conversions
- Custom templates

# 🚀 Deployment Guide

Complete guide for deploying ContentMultiplier to production.

---

## Option 1: Docker (Recommended)

### Prerequisites
- Docker installed
- Docker Compose installed

### Deploy

```bash
# 1. Clone repository
git clone https://github.com/ferdinands-molt-bot/money-maker.git
cd money-maker

# 2. Build and run
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Access app
open http://localhost:8080
```

### Stop
```bash
docker-compose down
```

---

## Option 2: Direct Python

### Prerequisites
- Python 3.8+
- pip

### Deploy

```bash
# 1. Clone repository
git clone https://github.com/ferdinands-molt-bot/money-maker.git
cd money-maker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python server.py

# 5. Access app
open http://localhost:8080
```

---

## Option 3: Heroku

### Prerequisites
- Heroku CLI installed
- Git

### Deploy

```bash
# 1. Login
heroku login

# 2. Create app
heroku create contentmultiplier-app

# 3. Add Python buildpack
heroku buildpacks:set heroku/python

# 4. Deploy
git push heroku main

# 5. Open
heroku open
```

---

## Option 4: Railway

### Prerequisites
- Railway CLI or GitHub integration

### Deploy

1. Fork this repository
2. Connect Railway to GitHub
3. Select repository
4. Deploy automatically

---

## Option 5: DigitalOcean App Platform

### Deploy

1. Fork this repository
2. Go to DigitalOcean App Platform
3. Select "Deploy from GitHub"
4. Select repository
5. Select Python environment
6. Deploy

---

## Option 6: AWS (EC2)

### Prerequisites
- AWS account
- EC2 instance running

### Deploy

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# Clone and run
git clone https://github.com/ferdinands-molt-bot/money-maker.git
cd money-maker
sudo docker-compose up -d
```

---

## Option 7: Google Cloud Run

### Prerequisites
- Google Cloud SDK
- Project created

### Deploy

```bash
# Build
gcloud builds submit --tag gcr.io/PROJECT-ID/contentmultiplier

# Deploy
gcloud run deploy contentmultiplier \
  --image gcr.io/PROJECT-ID/contentmultiplier \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 8: Vercel

For static frontend only (with API routes):

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

---

## Production Checklist

### Security
- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Regular security updates

### Performance
- [ ] Enable CDN (Cloudflare)
- [ ] Set up caching (Redis)
- [ ] Database optimization
- [ ] Image optimization

### Monitoring
- [ ] Set up logging (Sentry)
- [ ] Set up monitoring (Datadog/New Relic)
- [ ] Configure alerts
- [ ] Backup strategy

### Domain & SSL
- [ ] Purchase custom domain
- [ ] Set up DNS
- [ ] Configure SSL certificate
- [ ] Set up redirects (www → non-www)

---

## Environment Variables

Create `.env` file:

```env
# Required
SECRET_KEY=your-random-secret-key
FLASK_ENV=production

# Optional - for AI features
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional - for payments
STRIPE_SECRET_KEY=your-stripe-key
STRIPE_WEBHOOK_SECRET=your-webhook-secret

# Optional - for email
SENDGRID_API_KEY=your-sendgrid-key
FROM_EMAIL=noreply@yourdomain.com

# Optional - for database
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

---

## SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Scaling

### Horizontal Scaling
```bash
# Run multiple instances
docker-compose up -d --scale app=3

# Load balancer (nginx/haproxy)
```

### Database Scaling
- Read replicas
- Connection pooling
- Caching layer

---

## Backup Strategy

### Database
```bash
# Daily backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup_*.sql s3://your-bucket/backups/
```

### Files
```bash
# Sync to S3
aws s3 sync ./data s3://your-bucket/data/
```

---

## Troubleshooting

### App won't start
```bash
# Check logs
docker-compose logs

# Check port
lsof -i :8080

# Restart
docker-compose restart
```

### Performance issues
```bash
# Check CPU/Memory
docker stats

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080
```

---

## Cost Estimates

| Provider | Small (1k users) | Medium (10k users) | Large (100k users) |
|----------|------------------|--------------------|--------------------|
| Heroku | $7/mo | $50/mo | $200/mo |
| Railway | $5/mo | $30/mo | $150/mo |
| DigitalOcean | $6/mo | $24/mo | $100/mo |
| AWS | $10/mo | $50/mo | $300/mo |
| GCP | $10/mo | $45/mo | $250/mo |

---

## Support

For deployment help:
- Open an issue
- Email: deploy@contentmultiplier.com

---

**Happy deploying! 🚀**

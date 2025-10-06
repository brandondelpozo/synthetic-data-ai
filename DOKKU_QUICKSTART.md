# Dokku Quick Deployment Guide

Quick reference for deploying Synthetic Data AI to Dokku.

## One-Time Server Setup

Run these commands on your Dokku server:

```bash
# Create app
dokku apps:create synthetic-data-ai

# Configure builder to use prod.Dockerfile
dokku builder:set synthetic-data-ai selected dockerfile
dokku docker-options:add synthetic-data-ai build '--file prod.Dockerfile'

# Set environment variables
dokku config:set synthetic-data-ai \
  SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" \
  DEBUG=False \
  ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com" \
  OPENAI_API_KEY="your-openai-api-key-here" \
  DJANGO_SECURE_SSL_REDIRECT=True \
  DJANGO_SECURE_HSTS_SECONDS=31536000 \
  DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True \
  DJANGO_SECURE_HSTS_PRELOAD=True \
  DJANGO_SESSION_COOKIE_SECURE=True \
  DJANGO_CSRF_COOKIE_SECURE=True

# Set domain (optional)
dokku domains:set synthetic-data-ai yourdomain.com

# Enable SSL (optional, requires domain)
dokku letsencrypt:enable synthetic-data-ai
```

## Local Setup (One-Time)

```bash
# Add Dokku remote
git remote add dokku dokku@your-server.com:synthetic-data-ai
```

## Deploy

```bash
# Push to deploy
git push dokku main

# Run migrations
dokku run synthetic-data-ai python manage.py migrate

# Create superuser
dokku run synthetic-data-ai python manage.py createsuperuser
```

## Common Commands

```bash
# View logs
dokku logs synthetic-data-ai -t

# Restart app
dokku ps:restart synthetic-data-ai

# Check status
dokku ps:report synthetic-data-ai

# View config
dokku config synthetic-data-ai

# Access shell
dokku enter synthetic-data-ai

# Run Django command
dokku run synthetic-data-ai python manage.py <command>

# Database backup (SQLite)
dokku run synthetic-data-ai cat db.sqlite3 > backup_$(date +%Y%m%d).sqlite3

# Or backup via SSH
scp dokku@your-server.com:/var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3 backup_$(date +%Y%m%d).sqlite3
```

## Update Deployment

```bash
git add .
git commit -m "Your changes"
git push dokku main
```

## Troubleshooting

### Force rebuild
```bash
git commit --allow-empty -m "Rebuild"
git push dokku main
```

### Check environment variables
```bash
dokku config synthetic-data-ai
```

### View recent logs
```bash
dokku logs synthetic-data-ai --num 100
```

### Scale workers
```bash
dokku ps:scale synthetic-data-ai web=2
```

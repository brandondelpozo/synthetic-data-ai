# Quick Deploy Reference - SQLite Edition

## 🚀 Deploy in 5 Minutes

### Step 1: Server Setup (One-Time)
```bash
# SSH to your Dokku server
ssh dokku@your-server.com

# Create app
dokku apps:create synthetic-data-ai

# Set up persistent storage for SQLite
dokku storage:ensure-directory synthetic-data-ai
dokku storage:mount synthetic-data-ai /var/lib/dokku/data/storage/synthetic-data-ai:/synthetic-data-ai/data

# Configure Docker
dokku builder:set synthetic-data-ai selected dockerfile
dokku docker-options:add synthetic-data-ai build '--file prod.Dockerfile'

# Set environment variables (replace with your values)
dokku config:set synthetic-data-ai \
  SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" \
  DEBUG=False \
  ALLOWED_HOSTS="yourdomain.com" \
  OPENAI_API_KEY="your-openai-key" \
  DJANGO_SECURE_SSL_REDIRECT=True \
  DJANGO_SESSION_COOKIE_SECURE=True \
  DJANGO_CSRF_COOKIE_SECURE=True

# Optional: Set domain and SSL
dokku domains:set synthetic-data-ai yourdomain.com
dokku letsencrypt:enable synthetic-data-ai
```

### Step 2: Local Setup (One-Time)
```bash
# Add Dokku remote
cd /Users/brandon.del/Public/Personal/arquitectura-software/synthetic-data-ai
git remote add dokku dokku@your-server.com:synthetic-data-ai
```

### Step 3: Deploy
```bash
# Push to deploy
git push dokku main

# Run migrations
dokku run synthetic-data-ai python manage.py migrate

# Create admin user
dokku run synthetic-data-ai python manage.py createsuperuser
```

### Step 4: Verify
```bash
# Check logs
dokku logs synthetic-data-ai -t

# Check status
dokku ps:report synthetic-data-ai

# Visit your site
open https://yourdomain.com
```

## 📦 Local Development

```bash
# Set your OpenAI key
export OPENAI_API_KEY="your-key"

# Run with Docker
docker-compose up --build

# Access at http://localhost:8000
```

## 🔄 Update & Redeploy

```bash
# Make changes, commit, and push
git add .
git commit -m "Your changes"
git push dokku main

# Run migrations if needed
dokku run synthetic-data-ai python manage.py migrate
```

## 💾 Backup Database

```bash
# Quick backup
dokku run synthetic-data-ai cat db.sqlite3 > backup_$(date +%Y%m%d).sqlite3

# Or via SCP
scp dokku@your-server.com:/var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3 backup.sqlite3
```

## 🔧 Common Commands

```bash
# View logs
dokku logs synthetic-data-ai -t

# Restart
dokku ps:restart synthetic-data-ai

# Run Django command
dokku run synthetic-data-ai python manage.py <command>

# Access shell
dokku enter synthetic-data-ai

# Check config
dokku config synthetic-data-ai

# Force rebuild
git commit --allow-empty -m "Rebuild"
git push dokku main
```

## 📊 Monitoring

```bash
# Check app status
dokku ps:report synthetic-data-ai

# Check disk space
ssh dokku@your-server.com "df -h"

# Check database size
ssh dokku@your-server.com "ls -lh /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3"
```

## 🆘 Troubleshooting

### App won't start
```bash
dokku logs synthetic-data-ai -t
dokku ps:report synthetic-data-ai
```

### Database issues
```bash
dokku run synthetic-data-ai python manage.py migrate
dokku run synthetic-data-ai python manage.py dbshell
```

### Static files not loading
```bash
dokku run synthetic-data-ai python manage.py collectstatic --noinput
dokku ps:restart synthetic-data-ai
```

### Environment variable issues
```bash
dokku config synthetic-data-ai
dokku config:set synthetic-data-ai KEY=value
```

## 📚 Documentation

- **DEPLOYMENT.md** - Full deployment guide
- **DOKKU_QUICKSTART.md** - Detailed Dokku commands
- **SQLITE_NOTES.md** - SQLite configuration and maintenance
- **DEPLOYMENT_CHECKLIST.md** - Complete deployment checklist

## ⚙️ Key Configuration

- **Database:** SQLite (file-based)
- **Web Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Python:** 3.12
- **Django:** 5.2.5

## 🎯 Production Ready

✅ Security headers configured
✅ Static files optimized
✅ Environment-based settings
✅ No hardcoded secrets
✅ SSL/HTTPS support
✅ Persistent storage configured

---

**Need help?** Check the detailed guides in the documentation folder.

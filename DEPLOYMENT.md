# Deployment Guide for Synthetic Data AI

This guide covers deploying the Synthetic Data AI application to Dokku (similar to django-jobs deployment).

## Prerequisites

- A server with Dokku installed
- SSH access to your server
- Git repository set up for your project

## Files Created for Deployment

The following files have been created to support deployment:

1. **Dockerfile** - Development Docker configuration
2. **prod.Dockerfile** - Production-optimized Docker configuration for Dokku
3. **docker-compose.yml** - Local development with Docker Compose
4. **Procfile** - Process configuration for Heroku/Dokku
5. **heroku.yml** - Heroku deployment configuration
6. **.dockerignore** - Files to exclude from Docker builds
7. **.env.example** - Example environment variables

## Local Development with Docker

### Using Docker Compose

1. Set your `OPENAI_API_KEY` environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

2. Build and run the container:
   ```bash
   docker-compose up --build
   ```

3. Access the application at `http://localhost:8000`

4. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Dokku Deployment

### Initial Setup on Dokku Server

1. **Create the Dokku app** (on your server):
   ```bash
   dokku apps:create synthetic-data-ai
   ```

2. **Set up persistent storage for SQLite database**:
   ```bash
   dokku storage:ensure-directory synthetic-data-ai
   dokku storage:mount synthetic-data-ai /var/lib/dokku/data/storage/synthetic-data-ai:/synthetic-data-ai/data
   ```

3. **Set environment variables**:
   ```bash
   # Required settings
   dokku config:set synthetic-data-ai SECRET_KEY="your-super-secret-key-here"
   dokku config:set synthetic-data-ai DEBUG=False
   dokku config:set synthetic-data-ai ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
   dokku config:set synthetic-data-ai OPENAI_API_KEY="your-openai-api-key"
   
   # Security settings for production
   dokku config:set synthetic-data-ai DJANGO_SECURE_SSL_REDIRECT=True
   dokku config:set synthetic-data-ai DJANGO_SECURE_HSTS_SECONDS=31536000
   dokku config:set synthetic-data-ai DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
   dokku config:set synthetic-data-ai DJANGO_SECURE_HSTS_PRELOAD=True
   dokku config:set synthetic-data-ai DJANGO_SESSION_COOKIE_SECURE=True
   dokku config:set synthetic-data-ai DJANGO_CSRF_COOKIE_SECURE=True
   ```

4. **Configure Dockerfile for deployment**:
   ```bash
   dokku builder:set synthetic-data-ai selected dockerfile
   dokku docker-options:add synthetic-data-ai build '--file prod.Dockerfile'
   ```

5. **Set up domain** (optional):
   ```bash
   dokku domains:set synthetic-data-ai yourdomain.com
   ```

6. **Enable SSL with Let's Encrypt** (optional):
   ```bash
   dokku letsencrypt:enable synthetic-data-ai
   ```

### Deploy from Local Machine

1. **Add Dokku remote** (replace with your server details):
   ```bash
   git remote add dokku dokku@your-server.com:synthetic-data-ai
   ```

2. **Deploy the application**:
   ```bash
   git push dokku main
   ```
   
   Or if your branch is named differently:
   ```bash
   git push dokku your-branch:main
   ```

3. **Run migrations**:
   ```bash
   dokku run synthetic-data-ai python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   dokku run synthetic-data-ai python manage.py createsuperuser
   ```

5. **Collect static files** (should happen automatically, but can be run manually):
   ```bash
   dokku run synthetic-data-ai python manage.py collectstatic --noinput
   ```

### Post-Deployment

1. **Check application logs**:
   ```bash
   dokku logs synthetic-data-ai -t
   ```

2. **Restart the application** (if needed):
   ```bash
   dokku ps:restart synthetic-data-ai
   ```

3. **Check application status**:
   ```bash
   dokku ps:report synthetic-data-ai
   ```

## Environment Variables

### Required Variables

- `SECRET_KEY` - Django secret key (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `OPENAI_API_KEY` - Your OpenAI API key for AI data generation

### Optional Variables

- `DEBUG` - Set to `False` in production (default: `True`)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- Security settings (see `.env.example`)

## Database Management

### Backup Database (SQLite)
```bash
# Via Dokku command
dokku run synthetic-data-ai cat db.sqlite3 > backup_$(date +%Y%m%d).sqlite3

# Or via SSH/SCP
scp dokku@your-server.com:/var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3 backup.sqlite3
```

### Restore Database
```bash
# Copy backup to server
scp backup.sqlite3 dokku@your-server.com:/tmp/

# Restore on server
ssh dokku@your-server.com
sudo cp /tmp/backup.sqlite3 /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3
sudo chown 32767:32767 /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3
dokku ps:restart synthetic-data-ai
```

### Access Database Console
```bash
dokku run synthetic-data-ai python manage.py dbshell
```

## Troubleshooting

### View Logs
```bash
dokku logs synthetic-data-ai -t
```

### Access Container Shell
```bash
dokku enter synthetic-data-ai
```

### Rebuild and Redeploy
```bash
git commit --allow-empty -m "Rebuild"
git push dokku main
```

### Check Configuration
```bash
dokku config synthetic-data-ai
```

## SQLite in Production

This project uses SQLite for both development and production:
- Simple setup and deployment
- No separate database server needed
- Perfect for small to medium traffic applications
- Ensure regular backups of the db.sqlite3 file
- Consider PostgreSQL if you need high concurrency

## Updating the Application

1. Make changes to your code
2. Commit changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```
3. Push to Dokku:
   ```bash
   git push dokku main
   ```
4. Run migrations if needed:
   ```bash
   dokku run synthetic-data-ai python manage.py migrate
   ```

## Scaling

To scale the application (increase number of web processes):
```bash
dokku ps:scale synthetic-data-ai web=2
```

## Monitoring

Check resource usage:
```bash
dokku ps:report synthetic-data-ai
```

## Additional Resources

- [Dokku Documentation](http://dokku.viewdocs.io/dokku/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

## Notes

- The application uses WhiteNoise for serving static files in production
- PostgreSQL is recommended for production (configured via DATABASE_URL)
- Static files are automatically collected during deployment
- All sensitive data should be stored in environment variables, not in code

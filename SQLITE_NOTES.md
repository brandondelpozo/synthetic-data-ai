# SQLite Configuration Notes

## Overview

This project uses SQLite for both development and production environments. This is a deliberate choice for simplicity and ease of deployment.

## Why SQLite?

✅ **Advantages:**
- Zero configuration required
- No separate database server to manage
- Perfect for small to medium traffic applications
- File-based, easy to backup
- Built into Python, no additional dependencies
- Excellent for AI/ML applications with moderate concurrency

⚠️ **Considerations:**
- Limited concurrent write operations
- Not ideal for high-traffic applications (1000+ concurrent users)
- Database file grows with data (monitor disk space)
- Requires persistent storage in containerized environments

## Production Deployment with Dokku

### Persistent Storage Setup

Since Docker containers are ephemeral, you MUST configure persistent storage for the SQLite database file:

```bash
# Create storage directory
dokku storage:ensure-directory synthetic-data-ai

# Mount persistent volume
dokku storage:mount synthetic-data-ai /var/lib/dokku/data/storage/synthetic-data-ai:/synthetic-data-ai/data
```

### Database File Location

In the container, the database will be at:
- **Development:** `/synthetic-data-ai/db.sqlite3`
- **Production (mounted):** `/synthetic-data-ai/data/db.sqlite3`

**Note:** You may need to update `settings.py` to use the mounted path in production:

```python
# In settings.py
import os

if os.path.exists('/synthetic-data-ai/data'):
    # Production with persistent storage
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/synthetic-data-ai/data/db.sqlite3',
        }
    }
else:
    # Development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

## Backup Strategy

### Manual Backup

```bash
# From Dokku server
dokku run synthetic-data-ai cat db.sqlite3 > backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Via SCP
scp dokku@your-server.com:/var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3 ./backup.sqlite3
```

### Automated Backup (Cron Job)

Create a cron job on your Dokku server:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cp /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3 /backups/synthetic-data-$(date +\%Y\%m\%d).sqlite3

# Keep only last 30 days
0 3 * * * find /backups -name "synthetic-data-*.sqlite3" -mtime +30 -delete
```

## Database Maintenance

### Check Database Size

```bash
# On server
ls -lh /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3

# Via Dokku
dokku run synthetic-data-ai ls -lh db.sqlite3
```

### Optimize Database (VACUUM)

SQLite databases can become fragmented over time:

```bash
dokku run synthetic-data-ai python manage.py dbshell
# In SQLite shell:
VACUUM;
.quit
```

Or create a management command:

```bash
dokku run synthetic-data-ai python manage.py sqlsequencereset data_generator
```

### Database Integrity Check

```bash
dokku run synthetic-data-ai python manage.py dbshell
# In SQLite shell:
PRAGMA integrity_check;
.quit
```

## Performance Tips

1. **Enable WAL Mode** (Write-Ahead Logging):
   - Better concurrency
   - Faster writes
   - Automatically enabled in Django 4.1+

2. **Connection Settings** in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
           'OPTIONS': {
               'timeout': 20,  # Increase timeout for busy database
           }
       }
   }
   ```

3. **Monitor Database Locks**:
   - If you see "database is locked" errors, consider:
     - Reducing concurrent operations
     - Increasing timeout
     - Migrating to PostgreSQL

## When to Migrate to PostgreSQL

Consider migrating if you experience:
- Frequent "database is locked" errors
- More than 100 concurrent users
- Heavy write operations
- Need for advanced features (full-text search, JSON queries)
- Multiple application servers

## Migration Path to PostgreSQL

If you need to migrate later:

1. **Install PostgreSQL on Dokku:**
   ```bash
   dokku postgres:create synthetic-data-db
   dokku postgres:link synthetic-data-db synthetic-data-ai
   ```

2. **Update requirements.txt:**
   ```
   psycopg2-binary==2.9.9
   dj-database-url==2.2.0
   ```

3. **Update settings.py:**
   ```python
   import dj_database_url
   DATABASE_URL = config('DATABASE_URL', default=None)
   if DATABASE_URL:
       DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
   ```

4. **Export/Import Data:**
   ```bash
   # Export from SQLite
   python manage.py dumpdata > data.json
   
   # Import to PostgreSQL
   python manage.py loaddata data.json
   ```

## Current Configuration

- **Database Engine:** SQLite3
- **File Location:** `db.sqlite3` (development) or `/synthetic-data-ai/data/db.sqlite3` (production)
- **Backup Strategy:** Manual/Cron-based file copy
- **Suitable For:** Small to medium applications, AI data generation workloads

## Monitoring Checklist

- [ ] Monitor database file size weekly
- [ ] Set up automated backups
- [ ] Test backup restoration monthly
- [ ] Check for "database is locked" errors in logs
- [ ] Monitor disk space on server
- [ ] Run VACUUM quarterly

## Support

For issues or questions about SQLite configuration, refer to:
- [Django SQLite Documentation](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

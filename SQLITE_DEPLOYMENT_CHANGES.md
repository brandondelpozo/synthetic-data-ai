# SQLite Deployment Configuration - Change Summary

## Overview

The deployment configuration has been updated to use **SQLite** instead of PostgreSQL for both development and production environments.

## Files Modified

### 1. `requirements.txt`
**Removed:**
- `psycopg2-binary==2.9.9` (PostgreSQL adapter)
- `dj-database-url==2.2.0` (Database URL parser)

**Kept:**
- `gunicorn==22.0.0` (WSGI server)
- `whitenoise==6.7.0` (Static files)

### 2. `synthetic_data_project/settings.py`
**Changed:**
```python
# BEFORE (PostgreSQL support)
import dj_database_url
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# AFTER (SQLite only)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Removed import:**
- `import dj_database_url`

### 3. `docker-compose.yml`
**Removed:**
- PostgreSQL service (`db`)
- PostgreSQL volume (`postgres_data`)
- `DATABASE_URL` environment variable
- `depends_on: db` from web service

**Result:** Simplified single-service configuration

### 4. `prod.Dockerfile`
**Removed:**
- `libpq-dev` (PostgreSQL development libraries)

**Kept:**
- All other system dependencies
- Build optimizations
- Non-root user setup

### 5. `heroku.yml`
**Removed:**
- PostgreSQL addon configuration (`setup.addons`)

### 6. Documentation Files Updated

**DEPLOYMENT.md:**
- Removed PostgreSQL setup instructions
- Added SQLite persistent storage configuration
- Updated backup/restore procedures for SQLite
- Added SQLite-specific notes

**DOKKU_QUICKSTART.md:**
- Removed PostgreSQL creation/linking commands
- Updated backup commands for SQLite file copy
- Simplified deployment steps

**DEPLOYMENT_SUMMARY.md:**
- Updated database configuration section
- Removed PostgreSQL dependencies
- Updated comparison table
- Added SQLite notes

**DEPLOYMENT_CHECKLIST.md:**
- Removed PostgreSQL setup steps
- Added SQLite storage mount steps
- Updated backup procedures
- Updated monitoring checklist

## New Files Created

### `SQLITE_NOTES.md`
Comprehensive guide covering:
- Why SQLite was chosen
- Persistent storage setup for Dokku
- Backup strategies (manual and automated)
- Database maintenance procedures
- Performance tips
- When to migrate to PostgreSQL
- Migration path if needed

## Deployment Changes

### Before (PostgreSQL)
```bash
dokku apps:create synthetic-data-ai
dokku postgres:create synthetic-data-db
dokku postgres:link synthetic-data-db synthetic-data-ai
dokku config:set synthetic-data-ai SECRET_KEY="..." OPENAI_API_KEY="..."
```

### After (SQLite)
```bash
dokku apps:create synthetic-data-ai
dokku storage:ensure-directory synthetic-data-ai
dokku storage:mount synthetic-data-ai /var/lib/dokku/data/storage/synthetic-data-ai:/synthetic-data-ai/data
dokku config:set synthetic-data-ai SECRET_KEY="..." OPENAI_API_KEY="..."
```

## Environment Variables

### Removed
- `DATABASE_URL` - No longer needed

### Kept
- `SECRET_KEY` - Django secret key
- `OPENAI_API_KEY` - OpenAI API key
- `DEBUG` - Debug mode flag
- `ALLOWED_HOSTS` - Allowed hosts list
- Security settings (SSL, HSTS, cookies)

## Backup Strategy

### Before (PostgreSQL)
```bash
dokku postgres:export synthetic-data-db > backup.sql
dokku postgres:import synthetic-data-db < backup.sql
```

### After (SQLite)
```bash
# Backup
dokku run synthetic-data-ai cat db.sqlite3 > backup.sqlite3
# or
scp dokku@server:/var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3 backup.sqlite3

# Restore
scp backup.sqlite3 dokku@server:/tmp/
ssh dokku@server
sudo cp /tmp/backup.sqlite3 /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3
sudo chown 32767:32767 /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3
dokku ps:restart synthetic-data-ai
```

## Benefits of SQLite Configuration

✅ **Simpler deployment** - No database server to manage
✅ **Fewer dependencies** - No PostgreSQL packages needed
✅ **Easier local development** - Works out of the box
✅ **Lower resource usage** - No separate database process
✅ **Faster for small datasets** - No network overhead
✅ **Perfect for AI workloads** - Good for batch processing

## Considerations

⚠️ **Concurrent writes** - Limited compared to PostgreSQL
⚠️ **Scaling** - Best for small to medium traffic
⚠️ **Backups** - Manual file-based backups required
⚠️ **Disk space** - Monitor database file growth

## When to Reconsider

Consider PostgreSQL if you need:
- High concurrent write operations
- Multiple application servers
- Advanced database features
- 1000+ concurrent users
- Frequent "database is locked" errors

## Testing

Test the configuration:

```bash
# Local development
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Production deployment
git push dokku main
dokku run synthetic-data-ai python manage.py migrate
dokku run synthetic-data-ai python manage.py createsuperuser
```

## Rollback Plan

If you need to switch back to PostgreSQL:

1. Restore the PostgreSQL configuration from git history
2. Install PostgreSQL on Dokku
3. Export data from SQLite: `python manage.py dumpdata > data.json`
4. Update settings and requirements
5. Import data to PostgreSQL: `python manage.py loaddata data.json`

## Summary

The deployment configuration is now **simpler and more straightforward** with SQLite:
- ✅ Fewer moving parts
- ✅ Easier to understand
- ✅ Faster to deploy
- ✅ Lower maintenance overhead
- ✅ Suitable for the project's needs

All documentation has been updated to reflect this change, and comprehensive guides are available for backup, maintenance, and potential migration paths.

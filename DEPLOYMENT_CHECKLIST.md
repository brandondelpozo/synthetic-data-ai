# Deployment Checklist

Use this checklist to ensure a smooth deployment of Synthetic Data AI to Dokku.

## Pre-Deployment Checklist

### Local Testing
- [ ] Test application locally with `python manage.py runserver`
- [ ] Test with Docker Compose: `docker-compose up --build`
- [ ] Verify all features work with PostgreSQL (in Docker)
- [ ] Run migrations: `docker-compose exec web python manage.py migrate`
- [ ] Create test superuser: `docker-compose exec web python manage.py createsuperuser`
- [ ] Test AI data generation features
- [ ] Verify static files are served correctly

### Code Preparation
- [ ] All changes committed to Git
- [ ] `.env` file is NOT committed (check `.gitignore`)
- [ ] `requirements.txt` includes all dependencies
- [ ] No hardcoded secrets in code
- [ ] `DEBUG=False` will be set in production

### Credentials Ready
- [ ] Generate Django SECRET_KEY
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- [ ] OpenAI API key available
- [ ] Server SSH access confirmed
- [ ] Domain name ready (if using custom domain)

## Server Setup Checklist

### Initial Dokku Configuration
- [ ] SSH into Dokku server
- [ ] Create app: `dokku apps:create synthetic-data-ai`
- [ ] Set up persistent storage for SQLite:
  ```bash
  dokku storage:ensure-directory synthetic-data-ai
  dokku storage:mount synthetic-data-ai /var/lib/dokku/data/storage/synthetic-data-ai:/synthetic-data-ai/data
  ```
- [ ] Configure builder:
  ```bash
  dokku builder:set synthetic-data-ai selected dockerfile
  dokku docker-options:add synthetic-data-ai build '--file prod.Dockerfile'
  ```

### Environment Variables
- [ ] Set SECRET_KEY
- [ ] Set OPENAI_API_KEY
- [ ] Set DEBUG=False
- [ ] Set ALLOWED_HOSTS (your domain)
- [ ] Set security variables (SSL, HSTS, cookies)
- [ ] Verify all variables: `dokku config synthetic-data-ai`

### Domain and SSL (Optional)
- [ ] Set domain: `dokku domains:set synthetic-data-ai yourdomain.com`
- [ ] Install Let's Encrypt plugin (if not installed)
- [ ] Enable SSL: `dokku letsencrypt:enable synthetic-data-ai`
- [ ] Verify SSL certificate

## Deployment Checklist

### First Deployment
- [ ] Add Dokku remote: `git remote add dokku dokku@your-server.com:synthetic-data-ai`
- [ ] Push to deploy: `git push dokku main`
- [ ] Watch deployment logs for errors
- [ ] Verify build completes successfully
- [ ] Check application starts: `dokku ps:report synthetic-data-ai`

### Post-Deployment Setup
- [ ] Run migrations: `dokku run synthetic-data-ai python manage.py migrate`
- [ ] Create superuser: `dokku run synthetic-data-ai python manage.py createsuperuser`
- [ ] Verify static files: Check admin panel styling
- [ ] Test application access via domain/IP
- [ ] Check logs: `dokku logs synthetic-data-ai -t`

## Testing Checklist

### Functionality Tests
- [ ] Access homepage
- [ ] Login to admin panel
- [ ] Test AI data generation
- [ ] Create dynamic table definition
- [ ] Generate synthetic data
- [ ] Export data to Excel
- [ ] Verify all templates render correctly
- [ ] Test form submissions
- [ ] Check database persistence

### Security Tests
- [ ] HTTPS is working (if SSL enabled)
- [ ] HTTP redirects to HTTPS (if configured)
- [ ] Admin panel requires authentication
- [ ] No debug information exposed
- [ ] Check security headers
- [ ] Verify CSRF protection

### Performance Tests
- [ ] Page load times acceptable
- [ ] AI generation works without timeout
- [ ] Database queries are efficient
- [ ] Static files load quickly

## Monitoring Setup

### Initial Monitoring
- [ ] Set up log monitoring: `dokku logs synthetic-data-ai -t`
- [ ] Check resource usage: `dokku ps:report synthetic-data-ai`
- [ ] Verify database size: `dokku postgres:info synthetic-data-db`
- [ ] Set up backup schedule

### Backup Configuration
- [ ] Test database backup:
  ```bash
  dokku run synthetic-data-ai cat db.sqlite3 > backup_test.sqlite3
  ```
- [ ] Test database restore (copy backup to server and restore)
- [ ] Schedule regular backups (cron job to copy db.sqlite3)
- [ ] Store backups securely (off-server)

## Maintenance Checklist

### Regular Updates
- [ ] Update dependencies regularly
- [ ] Monitor security advisories
- [ ] Test updates locally first
- [ ] Deploy updates: `git push dokku main`
- [ ] Run new migrations if needed

### Monitoring
- [ ] Check logs weekly: `dokku logs synthetic-data-ai --num 100`
- [ ] Monitor disk space: `df -h` (important for SQLite)
- [ ] Check database file size: `ls -lh /var/lib/dokku/data/storage/synthetic-data-ai/db.sqlite3`
- [ ] Review error logs
- [ ] Monitor API usage (OpenAI)

### Backup Schedule
- [ ] Daily database backups
- [ ] Weekly full backups
- [ ] Monthly archive backups
- [ ] Test restore procedure quarterly

## Troubleshooting Reference

### Common Issues
- [ ] Know how to view logs: `dokku logs synthetic-data-ai -t`
- [ ] Know how to restart: `dokku ps:restart synthetic-data-ai`
- [ ] Know how to access shell: `dokku enter synthetic-data-ai`
- [ ] Know how to rebuild: `git commit --allow-empty -m "Rebuild" && git push dokku main`
- [ ] Know how to check config: `dokku config synthetic-data-ai`

### Emergency Contacts
- [ ] Document server provider contact
- [ ] Document domain registrar access
- [ ] Document database backup locations
- [ ] Document rollback procedure

## Documentation

### Keep Updated
- [ ] Document any custom configurations
- [ ] Update environment variables list
- [ ] Document any server-specific settings
- [ ] Keep deployment notes for team

## Post-Launch

### Optimization
- [ ] Monitor performance metrics
- [ ] Optimize slow queries
- [ ] Consider caching if needed
- [ ] Scale workers if needed: `dokku ps:scale synthetic-data-ai web=2`

### User Feedback
- [ ] Collect user feedback
- [ ] Monitor error rates
- [ ] Track feature usage
- [ ] Plan improvements

## Notes

- Check off items as you complete them
- Keep this checklist for future deployments
- Update checklist based on your experience
- Share with team members

## Quick Commands Reference

```bash
# Deploy
git push dokku main

# Logs
dokku logs synthetic-data-ai -t

# Restart
dokku ps:restart synthetic-data-ai

# Run command
dokku run synthetic-data-ai python manage.py <command>

# Backup (SQLite)
dokku run synthetic-data-ai cat db.sqlite3 > backup.sqlite3

# Check status
dokku ps:report synthetic-data-ai
```

---

**Last Updated:** $(date)
**Deployment Status:** [ ] Not Started [ ] In Progress [ ] Completed [ ] Production

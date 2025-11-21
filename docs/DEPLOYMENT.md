# Deployment Guide

## Docker

\`\`\`bash
docker-compose up
\`\`\`

## Gunicorn

\`\`\`bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
\`\`\`

## Production Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY is random
- [ ] ALLOWED_HOSTS configured
- [ ] Database backups enabled
- [ ] Redis persistence enabled
- [ ] SSL/HTTPS enabled
- [ ] Logs configured

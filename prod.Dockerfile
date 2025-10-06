# Production Dockerfile for Dokku deployment (slim version)
FROM python:3.12-slim

# working directory
WORKDIR /synthetic-data-ai

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/synthetic-data-ai \
    DJANGO_SETTINGS_MODULE=synthetic_data_project.settings \
    PORT=8000 \
    WEB_CONCURRENCY=3

# Install system packages required by Django
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential curl \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
COPY . .

RUN python manage.py collectstatic --noinput --clear

# Run as non-root user
RUN chown -R django:django /synthetic-data-ai
USER django

# Run application
CMD gunicorn synthetic_data_project.wsgi:application

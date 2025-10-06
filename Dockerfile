# Pull base image (slim version for faster builds)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /synthetic-data-ai

# Install dependencies
COPY requirements.txt /synthetic-data-ai/
RUN pip install -r requirements.txt

# Copy project
COPY . /synthetic-data-ai/

# Vision One Code Security Demo - Dockerfile
# SECURITY ISSUE: This Dockerfile contains intentional security vulnerabilities

# SECURITY ISSUE: Using outdated base image with known vulnerabilities
FROM python:3.8-slim

# SECURITY ISSUE: Running as root user
USER root

# SECURITY ISSUE: Hardcoded secrets in environment variables
ENV SECRET_KEY="flask-super-secret-key-never-change-this-in-production"
ENV DB_PASSWORD="super_secret_password_123"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
ENV VISION_ONE_API_KEY="fake-vision-one-api-key-12345-abcdef"
ENV JWT_SECRET="jwt-super-secret-key-never-change-this"

# SECURITY ISSUE: Installing packages as root without version pinning
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# SECURITY ISSUE: Setting working directory in root filesystem
WORKDIR /app

# SECURITY ISSUE: Copying all files without .dockerignore
COPY . .

# SECURITY ISSUE: Installing Python packages without version pinning
RUN pip install --no-cache-dir \
    flask \
    requests \
    pyjwt \
    werkzeug \
    sqlite3 \
    pickle-mixin

# SECURITY ISSUE: Creating world-writable directories
RUN mkdir -p /tmp/uploads /tmp/backups /tmp/logs && \
    chmod 777 /tmp/uploads /tmp/backups /tmp/logs

# SECURITY ISSUE: Setting permissive file permissions
RUN chmod 755 /app/src/*.py

# SECURITY ISSUE: Creating a user but still running as root
RUN useradd -m -s /bin/bash appuser && \
    echo "appuser:password123" | chpasswd && \
    usermod -aG sudo appuser

# SECURITY ISSUE: Exposing application on all interfaces
EXPOSE 5000

# SECURITY ISSUE: Running application as root with debug mode
CMD ["python", "src/app.py"]

# SECURITY ISSUE: No health check defined
# SECURITY ISSUE: No resource limits set
# SECURITY ISSUE: No security context defined

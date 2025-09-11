# Sheba Admin Dashboard Backend - Deployment Guide

## Overview
This guide covers deploying the Sheba Admin Dashboard Backend to production environments using Docker, Docker Compose, and traditional server deployment methods.

## Prerequisites

### System Requirements
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Nginx (for production)
- Docker & Docker Compose (for containerized deployment)

### Environment Setup
1. Copy the environment template:
```bash
cp .env.example .env
```

2. Update the `.env` file with your production values:
```env
SECRET_KEY=your_production_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
DB_NAME=sheba_admin_db
DB_USER=sheba_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.yourdomain.com
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password
REDIS_URL=redis://127.0.0.1:6379/1
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
```

## Docker Deployment (Recommended)

### 1. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up -d --build

# Run database migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Populate sample data (optional)
docker-compose exec web python manage.py populate_authentication
docker-compose exec web python manage.py populate_clients
docker-compose exec web python manage.py populate_projects
docker-compose exec web python manage.py populate_content
docker-compose exec web python manage.py populate_communication
docker-compose exec web python manage.py populate_dashboard

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 2. SSL Certificate Setup
Place your SSL certificates in the `ssl/` directory:
```bash
mkdir ssl
# Copy your certificate files
cp your_cert.pem ssl/cert.pem
cp your_key.pem ssl/key.pem
```

### 3. Verify Deployment
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs web
docker-compose logs nginx
docker-compose logs db
```

## Traditional Server Deployment

### 1. Server Setup (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib redis-server nginx -y

# Create application user
sudo useradd --system --shell /bin/bash --home /opt/sheba sheba
sudo mkdir -p /opt/sheba
sudo chown sheba:sheba /opt/sheba
```

### 2. Database Setup
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE sheba_admin_db;
CREATE USER sheba_user WITH PASSWORD 'your_secure_password';
ALTER ROLE sheba_user SET client_encoding TO 'utf8';
ALTER ROLE sheba_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sheba_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sheba_admin_db TO sheba_user;
\q
```

### 3. Application Setup
```bash
# Switch to application user
sudo -u sheba -i

# Clone repository
cd /opt/sheba
git clone <your-repo-url> sheba-backend
cd sheba-backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your production values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test the application
python manage.py runserver 0.0.0.0:8000
```

### 4. Gunicorn Setup
```bash
# Create Gunicorn configuration
cat > /opt/sheba/sheba-backend/gunicorn.conf.py << 'EOF'
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
reload = False
daemon = False
user = "sheba"
group = "sheba"
pidfile = "/opt/sheba/sheba-backend/gunicorn.pid"
accesslog = "/opt/sheba/sheba-backend/logs/gunicorn_access.log"
errorlog = "/opt/sheba/sheba-backend/logs/gunicorn_error.log"
loglevel = "info"
EOF

# Create logs directory
mkdir -p /opt/sheba/sheba-backend/logs
```

### 5. Systemd Service Setup
```bash
# Create systemd service file
sudo tee /etc/systemd/system/sheba-backend.service << 'EOF'
[Unit]
Description=Sheba Admin Dashboard Backend
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=sheba
Group=sheba
WorkingDirectory=/opt/sheba/sheba-backend
Environment=PATH=/opt/sheba/sheba-backend/venv/bin
ExecStart=/opt/sheba/sheba-backend/venv/bin/gunicorn -c gunicorn.conf.py sheba_admin_backend.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable sheba-backend
sudo systemctl start sheba-backend
sudo systemctl status sheba-backend
```

### 6. Nginx Configuration
```bash
# Create Nginx site configuration
sudo tee /etc/nginx/sites-available/sheba-backend << 'EOF'
server {
    listen 80;
    server_name yourdomain.com api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com api.yourdomain.com;

    ssl_certificate /etc/ssl/certs/your_cert.pem;
    ssl_certificate_key /etc/ssl/private/your_key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    client_max_body_size 100M;

    location /static/ {
        alias /opt/sheba/sheba-backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /opt/sheba/sheba-backend/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/sheba-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Monitoring and Maintenance

### 1. Log Monitoring
```bash
# Application logs
tail -f /opt/sheba/sheba-backend/logs/django.log
tail -f /opt/sheba/sheba-backend/logs/gunicorn_access.log
tail -f /opt/sheba/sheba-backend/logs/gunicorn_error.log

# System logs
sudo journalctl -u sheba-backend -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Database Backup
```bash
# Create backup script
cat > /opt/sheba/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/sheba/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -h localhost -U sheba_user -d sheba_admin_db > $BACKUP_DIR/sheba_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "sheba_backup_*.sql" -mtime +7 -delete
EOF

chmod +x /opt/sheba/backup_db.sh

# Add to crontab for daily backups
echo "0 2 * * * /opt/sheba/backup_db.sh" | sudo crontab -u sheba -
```

### 3. Health Checks
```bash
# Create health check script
cat > /opt/sheba/health_check.sh << 'EOF'
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/)
if [ $response -eq 200 ]; then
    echo "✅ Application is healthy"
    exit 0
else
    echo "❌ Application is down (HTTP $response)"
    exit 1
fi
EOF

chmod +x /opt/sheba/health_check.sh
```

## Security Considerations

### 1. Firewall Setup
```bash
# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. SSL/TLS Configuration
- Use Let's Encrypt for free SSL certificates
- Configure strong cipher suites
- Enable HSTS headers
- Regular certificate renewal

### 3. Database Security
- Use strong passwords
- Limit database access to application server only
- Regular security updates
- Enable connection encryption

## Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   sudo systemctl reload nginx
   ```

2. **Database connection errors**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Test connection
   psql -h localhost -U sheba_user -d sheba_admin_db
   ```

3. **Permission errors**
   ```bash
   # Fix file permissions
   sudo chown -R sheba:sheba /opt/sheba/sheba-backend
   sudo chmod -R 755 /opt/sheba/sheba-backend
   ```

4. **Service not starting**
   ```bash
   # Check service logs
   sudo journalctl -u sheba-backend -n 50
   
   # Check configuration
   sudo systemctl status sheba-backend
   ```

## Performance Optimization

### 1. Database Optimization
- Configure PostgreSQL for production workloads
- Set up connection pooling
- Regular VACUUM and ANALYZE operations
- Monitor slow queries

### 2. Caching
- Configure Redis for session storage
- Implement API response caching
- Use CDN for static files

### 3. Application Optimization
- Configure Gunicorn workers based on CPU cores
- Enable gzip compression in Nginx
- Optimize database queries
- Monitor memory usage

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Database read replicas
- Redis clustering
- Container orchestration (Kubernetes)

### Vertical Scaling
- CPU and memory optimization
- Database performance tuning
- Connection pool sizing
- Worker process optimization

For additional support, refer to the API documentation and Django deployment best practices.

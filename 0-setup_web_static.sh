#!/usr/bin/env bash
# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
if [ -L /data/web_static/current ]; then
    unlink /data/web_static/current
fi
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ directory
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_line="location /hbnb_static/ { alias /data/web_static/current/; }"
if ! grep -qF "$config_line" "$config_file"; then
    sed -i "29i $config_line" "$config_file"
fi

# Restart Nginx
service nginx restart

exit 0

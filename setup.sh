# create folder structure
mkdir tmp/
mkdir tmp/static
mkdir tmp/media
mkdir tmp/logs
touch tmp/secrets.json
# install everything
apt update
apt install python3-pip python3-venv python3-dev apache2 libapache2-mod-wsgi-py3 libpq-dev snapd gettext
snap install core
snap refresh core
snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
# create venv and install deps
python3 -m venv tmp/venv
source tmp/venv/bin/activate
pip install -r requirements.txt
# setup apache configs
certbot certonly --apache -d qc-quality-control.de -d www.qc-quality-control.de --register-unsafely-without-email
a2enmod ssl
a2enmod rewrite
ln -s /home/qc-quality-control.de/apache.conf /etc/apache2/sites-available/qc-quality-control.de.conf
a2ensite qc-quality-control.de.conf
systemctl restart apache2

# kampanile3

A customizable chime with web interface.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MatthiasGi/kampanile3/main.svg)](https://results.pre-commit.ci/latest/github/MatthiasGi/kampanile3/main)

## Carillon

To use the carillon via [GrandOrgue](https://github.com/GrandOrgue/grandorgue),
see the [additional information](carillon/README.md) provided in the `carillon`
subdirectory.

## Development

To start development, run the following commands:

```bash
git clone git@github.com:MatthiasGi/kampanile3.git
cd kampanile3

python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development-requirements.txt

pre-commit install

cd kampanile3
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata sample

npm install
python manage.py collectstatic --noinput
python manage.py compilemessages

cp kampanile3/settings/local.example.py kampanile3/settings/local.py
```

Then adjust `kampanile3/settings/local.py` to your needs and run the server:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Production

For production, we assume a Nginx reverse proxy in front of Gunicorn. The Nginx
is used as a reverse proxy and to serve static files.

### Server settings

Prepare the virtual environment and install the production dependencies:

```bash
git clone git@github.com:MatthiasGi/kampanile3.git
cd kampanile3

python -m venv .venv
source .venv/bin/activate
pip install -r requirements/production-requirements.txt

cd kampanile3
python manage.py migrate
python manage.py createsuperuser

npm install
python manage.py collectstatic --noinput
python manage.py compilemessages

cp kampanile3/settings/local.example.py kampanile3/settings/local.py
```

Modify `kampanile3/settings/local.py` to your needs.

### Gunicorn

To setup gunicorn inside of a systemd socket:

```bash
sudo cp deployment/gunicorn.socket.sample /etc/systemd/system/gunicorn.socket
sudo cp deployment/gunicorn.service.sample /etc/systemd/system/gunicorn.service
```

Modify the `/etc/systemd/system/gunicorn.service` to your needs where marked.

Then start and enable the socket:

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

You may check if the socket is running and calling the service:

```bash
sudo systemctl status gunicorn.socket
file /run/gunicorn.sock

curl --unix-socket /run/gunicorn.sock localhost
sudo systemctl status gunicorn
```

### Nginx

```bash
sudo apt install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo cp deployment/kampanile3.sample /etc/nginx/sites-available/kampanile3
sudo ln -s /etc/nginx/sites-available/kampanile3 /etc/nginx/sites-enabled/kampanile3
```

Modify the `/etc/nginx/sites-available/kampanile3` to your needs where marked.
Then test the config file and start nginx:

```bash
sudo nginx -t
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Autostart GrandOrgue

In the case of a regular Raspberry Pi OS installation with a desktop
environment, GrandOrgue can be started automatically by creating the file
`~/.config/labwc/autostart` with the following content:

```text
/usr/bin/lwrespawn /usr/bin/GrandOrgue
```

Think about activating an autologin and configuring GrandOrgue to listen to the
MIDI-ports you want to use.

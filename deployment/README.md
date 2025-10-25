# Deployment on an RaspberryPi

In the following sections, the deployment process of the project on a
RaspberryPi is described as an example. However, the steps can be adapted to
other platforms as well.

## Prerequisites

First, a new microSD card with Raspberry Pi OS needs to be prepared. The
[Raspberry Pi Imager](https://www.raspberrypi.com/software/) can be used to
flash the OS. Select an OS with desktop environment, e.g.,
"Raspberry Pi OS (64-Bit)".

Remember to modify the settings:

1. Set a hostname
2. Set up a user and password
3. Configure the WiFi (if needed)
4. Set the locale settings (i.e., timezone, keyboard layout)
5. Enable SSH access

After flashing the OS, insert the microSD card into the RaspberryPi and power it
on.

## Initial setup

Prepare the RaspberryPi as a production environment by connecting via SSH and
following these steps:

### Update the system

```bash
sudo apt update
sudo apt upgrade
```

### Set basic system settings

Start the Raspberry Pi configuration tool:

```bash
sudo raspi-config
```

Set the following options:

1. `System Options` -> `Boot` -> `Desktop Desktop GUI`
2. `System Options` -> `Auto Login` -> Activate Desktop Auto Login
3. `Interface Options` -> `VNC` -> Enable the VNC server

### Install unattended upgrades

Another recommendation is to install unattended upgrades to keep the system
up-to-date:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
sudo unattended-upgrade --dry-run --debug
```

### Configure audio output

If you're using an audio HAT you probably need to configure it. For example, the
[Adafruit Speaker Bonnet](https://www.adafruit.com/product/3346) has a dedicated
[setup guide](https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage).
The following commands are taken from this guide:

```bash
sudo apt install -y python3-venv wget
python -m venv env --system-site-packages
source env/bin/activate

pip3 install adafruit-python-shell
wget https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/raw/main/i2samp.py
sudo -E env PATH=$PATH python3 i2samp.py
```

After rebooting, run the script again to test the speakers:

```bash
source env/bin/activate
sudo -E env PATH=$PATH python3 i2samp.py
```

After rebooting, you need to reboot again:

```bash
sudo reboot
```

<!-- ### Prepare Adafruit Blinka

Following
[Adafruit's Blinka guide](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
run the following commands:

```bash
source env/bin/activate
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
``` -->

## Setup the server

Prepare the virtual environment and install the production dependencies:

```bash
git clone https://github.com/MatthiasGi/kampanile3.git
cd kampanile3

sudo apt install libasound2-dev npm gettext

python -m venv .venv
source .venv/bin/activate
pip install -e .[rpi]

cd kampanile3
cp kampanile3/settings/local.example.py kampanile3/settings/local.py
```

Modify `kampanile3/settings/local.py` to your needs. Then run the following
commands:

```bash
python manage.py migrate
python manage.py createsuperuser

npm install
python manage.py collectstatic --noinput
python manage.py compilemessages

python manage.py loaddata songs

cd ..
```

### Gunicorn

To setup gunicorn inside of a systemd socket:

```bash
sudo cp deployment/gunicorn.socket.sample /etc/systemd/system/gunicorn.socket
sudo cp deployment/gunicorn.service.sample /etc/systemd/system/gunicorn.service
```

Modify the `/etc/systemd/system/gunicorn.service` to your needs where marked.
Make sure that `gunicorn` runs in the `kampanile3` subdirectory of the project
directory so it picks up the `gunicorn.conf.py`-file.

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
sudo systemctl enable nginx
sudo systemctl restart nginx
```

### Install and autostart GrandOrgue

Install GrandOrgue firstly:

```bash
sudo apt install grandorgue
```

Then connect through VNC and start GrandOrgue once to create the configuration.
Open the carillon, select the MIDI-ports with the help of the webinterface and
save the configuration.

In the case of a regular Raspberry Pi OS installation with a desktop
environment, GrandOrgue can be started automatically by creating the file
`~/.config/labwc/autostart` with the following content:

```text
/usr/bin/lwrespawn /usr/bin/GrandOrgue
```

### Setup firewall

A simple way to setup a firewall is through `ufw`:

```bash
sudo apt install ufw

sudo ufw default deny incoming
sudo ufw allow from <IP-Address-Range>/24 to any port 22    # SSH
sudo ufw allow from <IP-Address-Range>/24 to any port 5900  # VNC
sudo ufw limit ssh

sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### Finished

Now reboot the system, log in the webinterface and setup the carillon as you
like!

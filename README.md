# kampanile3

A customizable chime with web interface.

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

cd kampanile3/settings/local.example.py kampanile3/settings/local.py
```

Then adjust `kampanile3/settings/local.py` to your needs and run the server:

```bash
python manage.py runserver
```

If you want to use MQTT, set the environment variable `MQTT` before starting the
server:

```bash
MQTT=true python manage.py runserver
```

In a runtime, the command `python manage.py checkstrikers` should be run every
minute, e.g. via cron or systemd timer.

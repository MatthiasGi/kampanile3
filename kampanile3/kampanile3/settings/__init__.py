import os

from split_settings.tools import include, optional

env = os.getenv("DJANGO_ENV", "development")

include(
    "base.py",
    f"environments/{env}.py",
    optional("local.py"),
)

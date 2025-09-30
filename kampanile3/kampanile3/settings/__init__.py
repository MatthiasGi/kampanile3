import os
import sys

from split_settings.tools import include, optional

env = os.getenv("DJANGO_ENV", "development")

RUNNING_SERVER = os.getenv("RUNNING_SERVER", "runserver" in sys.argv)

include(
    "base.py",
    f"environments/{env}.py",
    optional("local.py"),
)

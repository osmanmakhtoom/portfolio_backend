import sys
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "apps"))

env = environ.Env()
env.read_env(BASE_DIR / ".env")

APP_ENV = env("APP_ENV")

try:
    if APP_ENV == "DEVELOPMENT":
        from .development import *
    elif APP_ENV == "PRODUCTION":
        from .production import *
    else:
        from .base import *
except ImportError:
    from .base import *

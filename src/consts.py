from pathlib import Path

from src.enums.system import Clients

# Project directory
PROJECT_ROOT = Path(__file__).parent.parent
ENV_DIR = PROJECT_ROOT / "config"

# General config
PYTHON_CONFIG = "pythonConfig"

PASSED_ICON = '✓'
FAILED_ICON = '✘'

# tenants setup
MULTI_OMS_CLIENTS = [Clients.LIRUNEX]
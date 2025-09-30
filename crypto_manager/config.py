from loguru import logger

ETHERSCAN_API_KEY = ""

try:
    from crypto_manager.config_local import *

    logger.debug("Overwrote with values from config_local.py !")
except ImportError:
    logger.debug("No config_local.py, using default values.")

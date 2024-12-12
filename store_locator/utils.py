import logging


# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Log to console
)

logger = logging.getLogger(__name__)

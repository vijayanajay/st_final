"""
logging_config.py
Standard logging configuration for the stock trading app.
"""
import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Sets up logging for the application. Should be called once in the main entry point.
    Args:
        level: Logging level (default: logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

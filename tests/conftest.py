"""
conftest.py
Configure pytest fixtures and setup for testing.
"""
import pytest
import logging
from configs.logging_config import setup_logging

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """
    Set up logging configuration for tests.
    This ensures logs are properly captured by pytest's caplog fixture.
    """
    # Initialize logging at the DEBUG level for tests
    setup_logging(level=logging.DEBUG)

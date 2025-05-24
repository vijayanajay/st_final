"""
conftest.py
Configure pytest fixtures and setup for testing.
"""
import pytest
import logging
from configs.logging_config import setup_logging

# Register custom pytest marks
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark tests as integration tests that verify multiple components working together"
    )

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """
    Set up logging configuration for tests.
    This ensures logs are properly captured by pytest's caplog fixture.
    """
    # Initialize logging at the DEBUG level for tests
    setup_logging(level=logging.DEBUG)

# tests/repositories/__init__.py
import pytest
from pathlib import Path

# Shared fixture to clean up test files
@pytest.fixture(scope="function")
def cleanup_test_files():
    """
    Remove temporary test files created during tests.
    """
    test_files = ["test_memories.json", "test_chat.json"]
    yield
    for file in test_files:
        path = Path(file)
        if path.exists():
            path.unlink()

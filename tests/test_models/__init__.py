# tests/test_models/__init__.py
import pytest
from domain.models.memory import Memory

@pytest.fixture(scope="function")
def clear_memory_state():
    """
    A pytest fixture to clear Memory.all_memories before each test.
    """
    Memory.all_memories.clear()
    yield
    Memory.all_memories.clear()
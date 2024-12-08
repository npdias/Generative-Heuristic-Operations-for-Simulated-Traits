import pytest
import asyncio
import json
from pathlib import Path
from infrastructure.repositories.memory_repository import MemoryRepository
from domain.models.memory import Memory
from domain.models.person import Person

# Test file location for temporary testing
TEST_MEMORY_FILE = "test_memories.json"

@pytest.fixture(scope="function")
def cleanup_test_files():
    """Remove test files after each test."""
    yield
    path = Path(TEST_MEMORY_FILE)
    if path.exists():
        path.unlink()

@pytest.mark.asyncio
async def test_memory_repository_save_and_load(cleanup_test_files):
    # Setup
    person = Person(name="Alice", relation="friend")
    await MemoryRepository.save_memories(file_location=TEST_MEMORY_FILE)

    # Verify file exists
    assert Path(TEST_MEMORY_FILE).exists()

    # Clear current memory and reload
    Memory.all_memories.clear()
    assert len(Memory.all_memories) == 0

    await MemoryRepository.load_memories(file_location=TEST_MEMORY_FILE)

    # Verify memory was reloaded correctly
    assert len(Memory.all_memories) == 1
    reloaded_person = Memory.all_memories[0]
    assert isinstance(reloaded_person, Person)
    assert reloaded_person.name == "Alice"
    assert reloaded_person.relation == "friend"

@pytest.mark.asyncio
async def test_memory_repository_file_not_found(cleanup_test_files):
    # Attempt to load from a non-existent file
    result = await MemoryRepository.load_memories(file_location="non_existent_file.json")
    assert result is False

@pytest.mark.asyncio
async def test_memory_repository_empty_memory_list(cleanup_test_files):
    # Save an empty memory list
    Memory.all_memories.clear()
    await MemoryRepository.save_memories(file_location=TEST_MEMORY_FILE)

    # Verify file exists and is empty
    assert Path(TEST_MEMORY_FILE).exists()
    with open(TEST_MEMORY_FILE, "r") as file:
        data = json.load(file)
        assert data["memories"] == []

    # Reload and verify memory list is still empty
    await MemoryRepository.load_memories(file_location=TEST_MEMORY_FILE)
    assert len(Memory.all_memories) == 0

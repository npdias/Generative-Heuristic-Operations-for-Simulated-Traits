import pytest
import asyncio
import json
from pathlib import Path
from infrastructure.repositories.chat_repository import ChatRepository
from domain.models.interaction import Interaction

# Test file locations for temporary testing
TEST_CHAT_FILE = "test_chat.json"

@pytest.fixture
def cleanup_test_files():
    """
    Cleanup test files after the test runs.
    """
    yield
    if Path(TEST_CHAT_FILE).exists():
        Path(TEST_CHAT_FILE).unlink()

@pytest.mark.asyncio
async def test_chat_repository_save_and_load(cleanup_test_files):
    """
    Test saving and loading interactions with the ChatRepository.
    """
    # Setup: Reset log and create interactions
    chat_repo = ChatRepository()
    chat_repo.chat_log = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
    ]

    # Save interactions to the test file
    await chat_repo.save_chat(file_location=TEST_CHAT_FILE)

    # Verify the file exists
    assert Path(TEST_CHAT_FILE).exists()

    # Clear current chat log and reload from the test file
    chat_repo.chat_log = []
    await chat_repo.load_chat(file_location=TEST_CHAT_FILE)

    # Verify interactions were reloaded correctly
    assert len(chat_repo.chat_log) == 2
    assert chat_repo.chat_log[0]["role"] == "user"
    assert chat_repo.chat_log[0]["content"] == "Hello!"
    assert chat_repo.chat_log[1]["role"] == "assistant"
    assert chat_repo.chat_log[1]["content"] == "Hi there!"

@pytest.mark.asyncio
async def test_chat_repository_file_not_found(cleanup_test_files):
    """
    Test handling of a non-existent file in ChatRepository.load_chat.
    """
    # Attempt to load from a non-existent file
    chat_repo = ChatRepository()
    result = await chat_repo.load_chat(file_location="non_existent_file.json")
    assert result is False

@pytest.mark.asyncio
async def test_interaction_class():
    """
    Test the functionality of the Interaction class.
    """
    # Reset log and create an interaction
    Interaction.reset_log()
    i = Interaction(role="user", content="Test message")
    assert len(Interaction.listed) == 1
    assert Interaction.listed[0]["role"] == "user"
    assert Interaction.listed[0]["content"] == "Test message"

    # Test reset_log
    Interaction.reset_log()
    assert len(Interaction.listed) == 0

    # Test from_dict method
    data = {"role": "assistant", "content": "Here to help!", "ts": 1672531200.123}
    i_from_dict = Interaction.from_dict(data)
    assert i_from_dict.role == "assistant"
    assert i_from_dict.content == "Here to help!"
    assert i_from_dict.ts == 1672531200.123

    # Test invalid role
    with pytest.raises(ValueError):
        Interaction(role="invalid", content="This should fail.")

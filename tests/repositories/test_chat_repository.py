import pytest
import asyncio
import json
from pathlib import Path
from tests.repositories import cleanup_test_files
from infrastructure.repositories.chat_repository import ChatRepository
from domain.models.interaction import Interaction

# Test file locations for temporary testing

TEST_CHAT_FILE = "test_chat.json"

@pytest.mark.asyncio
async def test_chat_repository_save_and_load(cleanup_test_files):
    # Setup
    Interaction(role="user", content="Hello!")
    Interaction(role="assistant", content="Hi there!")
    await ChatRepository.save_chat(file_location=TEST_CHAT_FILE)

    # Verify file exists
    assert Path(TEST_CHAT_FILE).exists()

    # Clear current interactions and reload
    Interaction.reset_log()
    assert len(Interaction.listed) == 0

    await ChatRepository.load_chat(file_location=TEST_CHAT_FILE)

    # Verify interactions were reloaded correctly
    assert len(Interaction.listed) == 2
    assert Interaction.listed[0]["role"] == "user"
    assert Interaction.listed[0]["content"] == "Hello!"
    assert Interaction.listed[1]["role"] == "assistant"
    assert Interaction.listed[1]["content"] == "Hi there!"

@pytest.mark.asyncio
async def test_chat_repository_file_not_found(cleanup_test_files):
    # Attempt to load from a non-existent file
    result = await ChatRepository.load_chat(file_location="non_existent_file.json")
    assert result is False

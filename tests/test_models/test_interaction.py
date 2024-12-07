import pytest
from domain.models.interaction import Interaction

@pytest.fixture(scope="function")
def clear_interaction_log():
    """
    A pytest fixture to clear Interaction.listed before each test.
    """
    Interaction.reset_log()
    yield
    Interaction.reset_log()

def test_interaction_initialization(clear_interaction_log):
    interaction = Interaction(role="user", content="Hello!")
    assert interaction.role == "user"
    assert interaction.content == "Hello!"
    assert len(Interaction.listed) == 1

def test_append_to_log(clear_interaction_log):
    interaction = Interaction(role="assistant", content="Hi there!")
    assert Interaction.listed[-1]["role"] == "assistant"
    assert Interaction.listed[-1]["content"] == "Hi there!"

def test_reset_log(clear_interaction_log):
    Interaction(role="user", content="Hello!")
    Interaction(role="assistant", content="Hi!")
    assert len(Interaction.listed) == 2

    Interaction.reset_log()
    assert len(Interaction.listed) == 0

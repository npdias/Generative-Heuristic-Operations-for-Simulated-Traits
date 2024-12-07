import pytest
from domain.models.memory import Memory
from domain.models.person import Person
from domain.models.event import Event
from domain.models.fact import Fact
from domain.models.conversation import Conversation

# Shared Test Fixtures
@pytest.fixture(scope="function")
def clear_memory_state():
    """
    A pytest fixture to clear Memory.all_memories before each test.
    """
    Memory.all_memories.clear()
    yield
    Memory.all_memories.clear()

# Unit Tests for Memory Class
def test_memory_initialization(clear_memory_state):
    memory = Memory(mem_type="Generic")
    assert memory.mem_type == "Generic"
    assert isinstance(memory.ID, str)
    assert memory in Memory.all_memories

def test_memory_add_to_memory(clear_memory_state):
    initial_count = len(Memory.all_memories)
    memory = Memory(mem_type="TestMemory")
    assert len(Memory.all_memories) == initial_count + 1
    assert Memory.all_memories[-1] == memory

# Unit Tests for Person Class
def test_person_initialization(clear_memory_state):
    person = Person(name="John Doe", relation="friend", alive=True)
    assert person.name == "John Doe"
    assert person.relation == "friend"
    assert person.alive is True
    assert person.mem_type == "Person"
    assert person in Memory.all_memories

def test_person_is_self(clear_memory_state):
    person = Person(name="Self", relation="self")
    assert person.isSelf is True
    assert Memory.identity == person

# Unit Tests for Event Class
def test_event_initialization(clear_memory_state):
    event = Event(note="Meeting", dates=["2024-12-07"])
    assert event.note == "Meeting"
    assert event.dates == ["2024-12-07"]
    assert event.mem_type == "Event"
    assert event in Memory.all_memories

# Unit Tests for Fact Class
def test_fact_initialization(clear_memory_state):
    fact = Fact(source="Book", note="E=mc^2")
    assert fact.source == "Book"
    assert fact.note == "E=mc^2"
    assert fact.mem_type == "Fact"
    assert fact in Memory.all_memories

# Unit Tests for Conversation Class
def test_conversation_initialization(clear_memory_state):
    conversation = Conversation(transcript="Hello, world!", summary="Greeting")
    assert conversation.transcript == "Hello, world!"
    assert conversation.summary == "Greeting"
    assert conversation.mem_type == "Conversation"
    assert conversation in Memory.all_memories

# Integration Tests
def test_memory_all_memories_tracking(clear_memory_state):
    person = Person(name="Alice", relation="colleague", alive=True)
    event = Event(note="Project kickoff", dates=["2024-12-01"])
    fact = Fact(source="Wiki", note="Python is versatile.")
    conversation = Conversation(transcript="How are you?", summary="Simple greeting")

    assert len(Memory.all_memories) == 4
    assert Memory.all_memories[0] == person
    assert Memory.all_memories[1] == event
    assert Memory.all_memories[2] == fact
    assert Memory.all_memories[3] == conversation

def test_interaction_with_memories(clear_memory_state):
    person = Person(name="Bob", relation="friend", alive=False)
    assert len(Memory.all_memories) == 1
    assert person.name == "Bob"

    event = Event(note="Bob's farewell", dates=["2024-01-01"])
    assert len(Memory.all_memories) == 2
    assert event.note == "Bob's farewell"

    fact = Fact(source="Diary", note="Bob moved to another city.")
    assert len(Memory.all_memories) == 3
    assert fact.source == "Diary"

    conversation = Conversation(transcript="Goodbye, Bob!", summary="Farewell exchange")
    assert len(Memory.all_memories) == 4
    assert conversation.summary == "Farewell exchange"

if __name__ == "__main__":
    pytest.main()

import time
from typing import Optional, List, Dict


class Interaction:
    """
    Manages user and system interactions, maintaining a shared log of messages.
    """
    listed: List[Dict] = []
    VALID_ROLES = {"user", "assistant", "system"}

    def __init__(self, role: str, content: str, ts: Optional[float] = None):
        """
        Initialize a new interaction.

        Args:
            role (str): The role of the speaker (e.g., 'user', 'assistant', 'system').
            content (str): The message content.
            ts (Optional[float]): Timestamp for the interaction (default: current time).
        """
        if role not in Interaction.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of {Interaction.VALID_ROLES}.")

        self.ts = ts or time.time()
        self.role = role
        self.content = content
        self.append_log_collections()

    def append_log_collections(self):
        """
        Append this interaction to the shared log.
        """
        Interaction.listed.append(self.__dict__)

    def log_format(self) -> Dict[str, str]:
        """
        Format the interaction for logging.

        Returns:
            dict: A dictionary with a formatted timestamp, role, and content.
        """
        timestamp = time.strftime("%b %d %Y %H:%M:%S", time.localtime(self.ts))
        return {'timestamp': timestamp, 'role': self.role, 'content': self.content}

    @classmethod
    def reset_log(cls):
        """
        Reset the shared log for testing or a new session.
        """
        cls.listed.clear()

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        """
        Create an Interaction instance from a dictionary.

        Args:
            data (dict): Dictionary containing 'role', 'content', and optionally 'ts'.

        Returns:
            Interaction: A new instance of the class.
        """
        return cls(
            role=data.get("role"),
            content=data.get("content"),
            ts=data.get("ts")
        )

    @classmethod
    def to_dict_list(cls) -> List[Dict[str, str]]:
        """
        Retrieve the shared log as a list of dictionaries.

        Returns:
            list: The shared log.
        """
        return cls.listed

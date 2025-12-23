import uuid
from dataclasses import dataclass, field
from typing import List

from task._models.message import Message


@dataclass
class Conversation:
    """
    Represents a conversation with a unique ID and a list of messages.
    
    Attributes:
        id (str): Unique identifier for the conversation, generated automatically
        messages (list[Message]): List of messages in the conversation
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation.
        
        Args:
            message (Message): The message to add to the conversation
        """
        self.messages.append(message)

    def get_messages(self) -> List[Message]:
        """
        Get all messages in the conversation.
        
        Returns:
            List[Message]: List of messages in the conversation
        """
        return self.messages
    
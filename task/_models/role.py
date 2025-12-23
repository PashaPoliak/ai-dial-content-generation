from enum import StrEnum


class Role(StrEnum):
    """
    Enum representing the role of a message in a conversation.
    
    Attributes:
        SYSTEM: System message role
        USER: User message role
        AI: Assistant message role
    """
    SYSTEM = "system"
    USER = "user"
    AI = "assistant"

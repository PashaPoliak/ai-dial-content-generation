from dataclasses import dataclass
from typing import Any, Dict, Optional

from task._models.custom_content import CustomContent
from task._models.role import Role


@dataclass
class Message:
    """
    Represents a message with a role, content, and optional custom content.
    
    Attributes:
        role (Role): The role of the message sender (system, user, or assistant)
        content (str): The text content of the message
        custom_content (Optional[CustomContent]): Optional custom content with attachments
    """
    role: Role
    content: str
    custom_content: Optional[CustomContent] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the message
        """
        result: Dict[str, Any] = {
            "role": self.role.value,
            "content": self.content
        }

        if self.custom_content:
            result["custom_content"] = self.custom_content.to_dict()

        return result

    @classmethod
    def from_dict(cls, data: Dict) -> "Message":
        """
        Create a Message instance from a dictionary.
        
        Args:
            data (Dict): Dictionary containing message data
            
        Returns:
            Message: A new Message instance
        """
        return cls(
            role=Role(data["role"]),
            content=data.get("content", ""),
            custom_content=CustomContent.from_dict(data["custom_content"])
            if data.get("custom_content") else None
        )
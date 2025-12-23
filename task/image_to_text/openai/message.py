from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from task._models.role import Role

class ContentType(StrEnum):
    """
    Enum representing the type of content in a message.
    
    Attributes:
        IMAGE: Image content type
        TEXT: Text content type
    """
    IMAGE = "image_url"
    TEXT = "text"

@dataclass
class ImgUrl:
    """
    Represents an image URL with associated metadata.
    
    Attributes:
        url (str): The URL of the image
    """
    url: str

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the image URL to a dictionary representation.
        
        Returns:
            dict[str, Any]: Dictionary representation of the image URL
        """
        return {
            "url": self.url
        }

@dataclass
class ImgContent:
    """
    Represents image content with an image URL and type.
    
    Attributes:
        image_url (ImgUrl): The image URL object
        type (ContentType): The content type, defaults to IMAGE
    """
    image_url: ImgUrl
    type: ContentType = ContentType.IMAGE

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the image content to a dictionary representation.
        
        Returns:
            dict[str, Any]: Dictionary representation of the image content
        """
        return {
            "image_url": self.image_url.to_dict(),
            "type": self.type.value
        }


@dataclass
class TxtContent:
    """
    Represents text content with associated type.
    
    Attributes:
        text (str): The text content
        type (ContentType): The content type, defaults to TEXT
    """
    text: str
    type: ContentType = ContentType.TEXT

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the text content to a dictionary representation.
        
        Returns:
            dict[str, Any]: Dictionary representation of the text content
        """
        return {
            "text": self.text,
            "type": self.type.value
        }


@dataclass
class ContentedMessage:
    """
    Represents a message with a role and a list of content items.
    
    Attributes:
        role (Role): The role of the message sender
        content (list[ImgContent | TxtContent]): List of content items in the message
    """
    role: Role
    content: list[ImgContent | TxtContent]


    def to_dict(self) -> dict[str, Any]:
        """
        Convert the contented message to a dictionary representation.
        
        Returns:
            dict[str, Any]: Dictionary representation of the contented message
        """
        return {
            "role": self.role.value,
            "content": [content.to_dict() for content in self.content]
        }

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Attachment:
    """
    Represents an attachment with optional title, data, type, and URL.
    
    Attributes:
        title (Optional[str]): Optional title of the attachment
        data (Optional[str]): Optional data content of the attachment
        type (Optional[str]): Optional MIME type of the attachment
        url (Optional[str]): Optional URL where the attachment is located
    """
    title: Optional[str] = None
    data: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        """
        Convert the attachment to a dictionary representation.
        
        Returns:
            Dict[str, Optional[str]]: Dictionary representation of the attachment
        """
        return {
            "title": self.title,
            "data": self.data,
            "type": self.type,
            "url": self.url
        }


@dataclass
class CustomContent:
    """
    Represents custom content with a list of attachments.
    
    Attributes:
        attachments (List[Attachment]): List of attachments in the custom content
    """
    attachments: List[Attachment]

    def to_dict(self) -> Dict[str, List[Dict]]:
        """
        Convert the custom content to a dictionary representation.
        
        Returns:
            Dict[str, List[Dict]]: Dictionary representation of the custom content with attachments
        """
        return {
            "attachments": [attachment.to_dict() for attachment in self.attachments]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CustomContent":
        """
        Create a CustomContent instance from a dictionary.
        
        Args:
            data (Dict): Dictionary containing custom content data
            
        Returns:
            CustomContent: A new CustomContent instance
        """
        attachments = []
        if attachment_data := data.get("attachments"):
            if isinstance(attachment_data, list):
                attachments = [
                    Attachment(**{k: v for k, v in attachment.items()
                                  if k in ["title", "data", "type", "url"]})
                    for attachment in attachment_data
                ]
        return cls(attachments=attachments)

import pytest

from task._models.message import Message
from task._models.role import Role
from task._models.custom_content import CustomContent, Attachment
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl
from tests.test_data import TEST_ATTACHMENT_TITLE, TEST_ATTACHMENT_TYPE, TEST_CONTENT, TEST_ATTACHMENT_URL

TEST_QUESTION = "Check out this image"


class TestMessageModel:
    

    def test_simple_message_creation(self):
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        assert message.role == Role.USER
        assert message.content == TEST_CONTENT
        assert message.custom_content is None

    def test_message_with_custom_content(self):
        
        attachment = Attachment(
            title=TEST_ATTACHMENT_TITLE,
            url=TEST_ATTACHMENT_URL,
            type=TEST_ATTACHMENT_TYPE
        )
        
        custom_content = CustomContent(attachments=[attachment])
        
        message = Message(
            role=Role.USER,
            content=TEST_QUESTION,
            custom_content=custom_content
        )
        
        assert message.role == Role.USER
        assert message.content == TEST_QUESTION
        assert message.custom_content is not None
        assert len(message.custom_content.attachments) == 1
        assert message.custom_content.attachments[0].title == TEST_ATTACHMENT_TITLE

    def test_message_to_dict_simple(self):
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        expected_dict = {
            "role": "user",
            "content": TEST_CONTENT
        }
        
        assert message.to_dict() == expected_dict

    def test_message_to_dict_with_custom_content(self):
        
        attachment = Attachment(
            title=TEST_ATTACHMENT_TITLE,
            url=TEST_ATTACHMENT_URL,
            type=TEST_ATTACHMENT_TYPE
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_QUESTION,
            custom_content=CustomContent(attachments=[attachment])
        )
        
        expected_dict = {
            "role": "user",
            "content": TEST_QUESTION,
            "custom_content": {
                "attachments": [
                    {
                        "title": TEST_ATTACHMENT_TITLE,
                        "data": None,
                        "type": "image/png",
                        "url": TEST_ATTACHMENT_URL
                    }
                ]
            }
        }
        
        assert message.to_dict() == expected_dict

    def test_message_validation_with_invalid_role(self):
        


        with pytest.raises(ValueError):
            Role("invalid_role")

    def test_contented_message_creation(self):
        
        img_url = ImgUrl(url="data:image/png;base64,test_base64")
        img_content = ImgContent(image_url=img_url)
        txt_content = TxtContent(text="Test text")
        
        message = ContentedMessage(
            role=Role.USER,
            content=[img_content, txt_content]
        )
        
        assert message.role == Role.USER
        assert len(message.content) == 2
        assert isinstance(message.content[0], ImgContent)
        assert isinstance(message.content[1], TxtContent)

    def test_contented_message_to_dict(self):
        
        img_url = ImgUrl(url="data:image/png;base64,test_base64")
        img_content = ImgContent(image_url=img_url)
        txt_content = TxtContent(text="Test text")
        
        message = ContentedMessage(
            role=Role.USER,
            content=[img_content, txt_content]
        )
        
        expected_dict = {
            "role": "user",
            "content": [
                {
                    "image_url": {"url": "data:image/png;base64,test_base64"},
                    "type": "image_url"
                },
                {
                    "text": "Test text",
                    "type": "text"
                }
            ]
        }
        
        assert message.to_dict() == expected_dict

    def test_message_with_empty_content(self):
        
        message = Message(
            role=Role.USER,
            content=""
        )
        
        assert message.role == Role.USER
        assert message.content == ""

    def test_message_with_none_content(self):
        

        message = Message(
            role=Role.USER,
            content=""
        )
        
        assert message.role == Role.USER
        assert message.content == ""
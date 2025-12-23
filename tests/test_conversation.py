from task._models.conversation import Conversation
from task._models.message import Message
from task._models.role import Role
from task._models.custom_content import CustomContent, Attachment
from tests.test_data import TEST_ATTACHMENT_URL, TEST_CONTENT


class TestConversationModel:
    

    def test_conversation_creation(self):
        
        conversation = Conversation()
        
        assert conversation.id is not None
        assert conversation.id != ""
        assert isinstance(conversation.messages, list)
        assert len(conversation.messages) == 0

    def test_add_message(self):
        
        conversation = Conversation()
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        conversation.add_message(message)
        
        assert len(conversation.messages) == 1
        assert conversation.messages[0] == message

    def test_get_messages(self):
        
        conversation = Conversation()
        
        message1 = Message(
            role=Role.USER,
            content="First message"
        )
        
        message2 = Message(
            role=Role.AI,
            content="Second message"
        )
        
        conversation.add_message(message1)
        conversation.add_message(message2)
        
        messages = conversation.get_messages()
        
        assert len(messages) == 2
        assert messages[0] == message1
        assert messages[1] == message2

    def test_conversation_with_multiple_roles(self):
        
        conversation = Conversation()
        
        user_message = Message(
            role=Role.USER,
            content="User message"
        )
        
        ai_message = Message(
            role=Role.AI,
            content="AI response"
        )
        
        system_message = Message(
            role=Role.SYSTEM,
            content="System instruction"
        )
        
        conversation.add_message(user_message)
        conversation.add_message(ai_message)
        conversation.add_message(system_message)
        
        messages = conversation.get_messages()
        
        assert len(messages) == 3
        assert messages[0].role == Role.USER
        assert messages[1].role == Role.AI
        assert messages[2].role == Role.SYSTEM

    def test_conversation_with_custom_content(self):
        
        conversation = Conversation()
        
        attachment = Attachment(
            title="test.png",
            url=TEST_ATTACHMENT_URL,
            type="image/png"
        )
        
        custom_content = CustomContent(attachments=[attachment])
        
        message = Message(
            role=Role.USER,
            content="Check out this image",
            custom_content=custom_content
        )
        
        conversation.add_message(message)
        
        messages = conversation.get_messages()
        
        assert len(messages) == 1
        assert messages[0].custom_content is not None
        assert len(messages[0].custom_content.attachments) == 1

    def test_empty_conversation(self):
        
        conversation = Conversation()
        
        messages = conversation.get_messages()
        
        assert len(messages) == 0

    def test_multiple_conversations_have_unique_ids(self):
        
        conversation1 = Conversation()
        conversation2 = Conversation()
        
        assert conversation1.id != conversation2.id

    def test_conversation_to_dict_simulation(self):
        

        conversation = Conversation()
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        conversation.add_message(message)
        

        assert len(conversation.messages) == 1
        assert conversation.messages[0].role == Role.USER
        assert conversation.messages[0].content == TEST_CONTENT

    def test_conversation_with_many_messages(self):
        
        conversation = Conversation()
        

        for i in range(10):
            message = Message(
                role=Role.USER,
                content=f"Message {i}"
            )
            conversation.add_message(message)
        
        messages = conversation.get_messages()
        
        assert len(messages) == 10
        for i, message in enumerate(messages):
            assert message.content == f"Message {i}"
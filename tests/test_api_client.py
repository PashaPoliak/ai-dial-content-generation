import pytest

from task._models.message import Message
from task._models.role import Role
from tests.mock_client import MockDialModelClient
from tests.test_data import TEST_API_KEY, TEST_CONTENT, TEST_ENDPOINT, TEST_MODEL_NAME

HTTP_STATUS_OK = 200
HTTP_STATUS_UNAUTHORIZED = 401
TEMPERATURE_VALUE = 0.7
MAX_TOKENS_VALUE = 100
MAX_TOKENS_SMALL_VALUE = 10

EXPECTED_MESSAGE_ROLE = Role.AI
EXPECTED_MESSAGE_CONTENT = "Test response"

class TestApiClient:    

    def mock_client(self):
        return MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY)
           
    def test_client_initialization_with_valid_params(self):
        
        client = self.mock_client()
        
        assert client._endpoint == TEST_ENDPOINT
        assert client._api_key == TEST_API_KEY

    def test_client_initialization_with_empty_api_key(self):
        
        client = MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=""
        )
        assert client is not None


    def test_get_completion_request_format(self):
        
        client = self.mock_client()
                
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        expected_result = Message(role=EXPECTED_MESSAGE_ROLE, content=EXPECTED_MESSAGE_CONTENT)
        client.get_completion.return_value = expected_result
        
        result = client.get_completion([message])
        
        client.get_completion.assert_called_once()
        args, kwargs = client.get_completion.call_args
        messages_arg = args[0]
        
        assert len(messages_arg) == 1
        assert messages_arg[0].role == Role.USER
        assert messages_arg[0].content == TEST_CONTENT

    def test_get_completion_with_custom_fields(self, CHOICES_DATA):
        
        client = self.mock_client()
                
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        custom_fields = {
            "temperature": TEMPERATURE_VALUE,
            "max_tokens": MAX_TOKENS_VALUE
        }
        
        
        expected_result = Message(role=EXPECTED_MESSAGE_ROLE, content=EXPECTED_MESSAGE_CONTENT)
        client.get_completion.return_value = expected_result
        
        result = client.get_completion([message], custom_fields=custom_fields)
        
        assert result is not None
        
 
        client.get_completion.assert_called_once()
        args, kwargs = client.get_completion.call_args
        messages_arg = args[0]
        passed_custom_fields = kwargs.get('custom_fields')
        
        
        assert passed_custom_fields is not None
        assert "temperature" in passed_custom_fields
        assert "max_tokens" in passed_custom_fields
        assert passed_custom_fields["temperature"] == TEMPERATURE_VALUE
        assert passed_custom_fields["max_tokens"] == MAX_TOKENS_VALUE


    def test_get_completion_with_kwargs(self, CHOICES_DATA):
        
        client = MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        
        expected_result = Message(role=EXPECTED_MESSAGE_ROLE, content=EXPECTED_MESSAGE_CONTENT)
        client.get_completion.return_value = expected_result
        
        result = client.get_completion([message], temperature=TEMPERATURE_VALUE, max_tokens=MAX_TOKENS_SMALL_VALUE)
        
        
        client.get_completion.assert_called_once()
        args, kwargs = client.get_completion.call_args
        messages_arg = args[0]
        passed_kwargs = {k: v for k, v in kwargs.items() if k not in ['custom_fields']}
        
        assert passed_kwargs["temperature"] == TEMPERATURE_VALUE
        assert passed_kwargs["max_tokens"] == MAX_TOKENS_SMALL_VALUE


    def test_get_completion_success_response(self):
        
        client = MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        
        expected_result = Message(role=EXPECTED_MESSAGE_ROLE, content=EXPECTED_MESSAGE_CONTENT)
        client.get_completion.return_value = expected_result
        
        result = client.get_completion([message])
        
        assert result.role == Role.AI
        assert result.content == "Test response"


    def test_get_completion_error_response(self):
        
        client = MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        

        client.get_completion.side_effect = Exception("HTTP 401: Unauthorized")
        
        with pytest.raises(Exception, match="HTTP 401: Unauthorized"):
            client.get_completion([message])
        

        client.get_completion.assert_called_once()

    def test_get_completion_no_choices_in_response(self):
        
        client = MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        

        client.get_completion.side_effect = ValueError("No Choice has been present in the response")
        
        with pytest.raises(ValueError, match="No Choice has been present in the response"):
            client.get_completion([message])
        

        client.get_completion.assert_called_once()

    def test_get_completion_no_message_in_choice(self):
        
        client = MockDialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_CONTENT
        )
        

        client.get_completion.side_effect = ValueError("No Message has been present in the response")
        
        with pytest.raises(ValueError, match="No Message has been present in the response"):
            client.get_completion([message])
        

        client.get_completion.assert_called_once()
        

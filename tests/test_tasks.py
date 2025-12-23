import asyncio
import importlib.util

import pytest
from unittest.mock import MagicMock, Mock, patch

from task._models.message import Message
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl
from task._models.custom_content import Attachment, CustomContent
from tests.mock_client import MockDialModelClient
from tests.test_data import TEST_ATTACHMENT_URL


class AsyncMock(Mock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


def load_task_module(task_path, module_name):
    
    spec = importlib.util.spec_from_file_location(module_name, task_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"Could not load module from {task_path}")


class TestOpenAITask:
    
    
    def test_openai_itt(self):
        

        task_module = load_task_module("task/image_to_text/openai/task_openai_itt.py", "task_openai_itt")
        start_openai_itt = task_module.start

        with patch('task.image_to_text.openai.task_openai_itt.DialModelClient') as mock_client_class, \
             patch('task._utils.model_client.requests.post') as mock_requests_post:

            mock_client_instance = MockDialModelClient()
            mock_client_instance.get_completion.return_value = Mock(
                content="Test analysis result"
            )
            mock_client_class.return_value = mock_client_instance


            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"role": "assistant", "content": "Test analysis result"}}]
            }
            mock_requests_post.return_value = mock_response

            start_openai_itt()


            assert mock_requests_post.call_count == 1


class TestDialTask:
    
    
    def test_dial_itt_upload(self):
        

        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        _put_image = task_module._put_image



        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client:

            mock_http_instance = AsyncMock()
            mock_response_get = MagicMock()
            mock_response_get.json.return_value = {"bucket": "test_bucket"}
            mock_response_get.raise_for_status.return_value = None
            mock_response_put = MagicMock()
            mock_response_put.json.return_value = {"url": TEST_ATTACHMENT_URL}
            mock_response_put.raise_for_status.return_value = None
            mock_http_instance.get.return_value = mock_response_get
            mock_http_instance.put.return_value = mock_response_put
            mock_httpx_client.return_value = mock_http_instance

            result = asyncio.run(_put_image())

            assert result.url == TEST_ATTACHMENT_URL

    def test_dial_itt(self):
        

        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        start_dial_itt = task_module.start



        with patch('task.image_to_text.task_dial_itt.DialModelClient') as mock_client_class, \
             patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post:

            mock_client_instance = MockDialModelClient()
            mock_client_instance.get_completion.return_value = Mock(
                content="Test DIAL analysis result"
            )
            mock_client_class.return_value = mock_client_instance


            mock_http_instance = AsyncMock()
            mock_response_get = MagicMock()
            mock_response_get.json.return_value = {"bucket": "test_bucket"}
            mock_response_get.raise_for_status.return_value = None
            mock_response_put = MagicMock()
            mock_response_put.json.return_value = {"url": TEST_ATTACHMENT_URL}
            mock_response_put.raise_for_status.return_value = None
            mock_http_instance.get.return_value = mock_response_get
            mock_http_instance.put.return_value = mock_response_put
            mock_httpx_client.return_value = mock_http_instance


            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"role": "assistant", "content": "Test DIAL analysis result"}}]
            }
            mock_requests_post.return_value = mock_response

            start_dial_itt()

            mock_requests_post.assert_called_once()


class TestTextToImageTask:
    
    
    def test_tti_save(self):
        
        
        task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
        _save_images = task_module._save_images
        
        TEST_IMAGE_TITLE = "test_image.png"
        TEST_ATTACHMENT_URL = "https://example.com/test_image.png"
        TEST_IMAGE_TYPE = "image/png"
        mock_attachment = Attachment(
            title=TEST_IMAGE_TITLE,
            url=TEST_ATTACHMENT_URL,
            type=TEST_IMAGE_TYPE
        )
        
        
        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('builtins.open', create=True) as mock_open, \
             patch('task.text_to_image.task_tti.datetime') as mock_datetime:

            mock_http_instance = AsyncMock()
            mock_response_get = MagicMock()
            mock_response_get.content = b"fake_image_data"
            mock_response_get.raise_for_status.return_value = None
            mock_http_instance.get.return_value = mock_response_get
            mock_httpx_client.return_value = mock_http_instance

            mock_datetime.now.return_value.strftime.return_value = "20231224_12000"

            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file

            asyncio.run(_save_images([mock_attachment]))

            mock_http_instance.get.assert_called_once_with(f"/v1/{TEST_ATTACHMENT_URL}")
            mock_file.write.assert_called_once_with(b"fake_image_data")


    def test_tti(self):
        

        task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
        start_tti = task_module.start
        

        with patch('task.text_to_image.task_tti.DialModelClient') as mock_client_class, \
             patch('task._utils.model_client.requests.post') as mock_requests_post:

            mock_client_instance = MockDialModelClient()
            mock_client_instance.get_completion.return_value = Mock(
                custom_content=Mock(attachments=[])
            )
            mock_client_class.return_value = mock_client_instance


            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"role": "assistant", "content": "Generated image"}}]
            }
            mock_requests_post.return_value = mock_response

            start_tti()

            mock_requests_post.assert_called_once()
    
    PROMPTS = [
        "Sunny day on Bali",
        "Mountain landscape at sunset",
        "Underwater coral reef",
        "City skyline at night"
    ]
    
    @pytest.mark.parametrize("prompt", PROMPTS)
    def test_start_function_text_to_image(self, prompt):
        

        task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
        start_tti = task_module.start
        

        with patch('task.text_to_image.task_tti.DialModelClient') as mock_client_class, \
             patch('task._utils.model_client.requests.post') as mock_requests_post:

            mock_client_instance = MockDialModelClient()
            mock_client_instance.get_completion.return_value = Mock(
                custom_content=Mock(attachments=[])
            )
            mock_client_class.return_value = mock_client_instance


            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"role": "assistant", "content": "Generated image"}}]
            }
            mock_requests_post.return_value = mock_response

            start_tti()

            mock_requests_post.assert_called_once()


def test_temperature_parameter():

    client = MockDialModelClient()
    
    message = Message(
        role=Role.USER,
        content="Test message"
    )
    

    with patch.object(client, '_make_request') as mock_request:
        TEMPERATURE_VALUE = 0.7
        client.get_completion([message], custom_fields={"temperature": TEMPERATURE_VALUE})



def test_max_tokens_parameter():

    client = MockDialModelClient()
    
    message = Message(
        role=Role.USER,
        content="Test message"
    )
    

    with patch.object(client, '_make_request') as mock_request:
        MAX_TOKENS_VALUE = 100
        client.get_completion([message], custom_fields={"max_tokens": MAX_TOKENS_VALUE})



def test_api_error_handling():

    from task._utils.model_client import DialModelClient

    client = DialModelClient(
        endpoint="https://test-endpoint.com",
        deployment_name="test-model",
        api_key="test-key"
    )

    message = Message(
        role=Role.USER,
        content="Test message"
    )


    with patch('task._utils.model_client.requests.post') as mock_requests_post:

        error_response = Mock()
        error_response.status_code = 401
        error_response.text = "Unauthorized"
        mock_requests_post.return_value = error_response

        try:
            result = client.get_completion([message])

            assert False, "Expected an exception for error response"
        except Exception as e:

            pass

        mock_requests_post.assert_called_once()



def test_empty_api_key_validation():
    


    client = MockDialModelClient()

    assert client is not None


def test_null_api_key_validation():
    


    client = MockDialModelClient()

    assert client is not None



def test_message_model_serialization():
    
    message = Message(
        role=Role.USER,
        content="Test content",
        custom_content=CustomContent(attachments=[
            Attachment(
                title="test.png",
                url="TEST_ATTACHMENT_URL",
                type="image/png"
            )
        ])
    )
    
    expected_dict = {
        "role": "user",
        "content": "Test content",
        "custom_content": {
            "attachments": [
                {
                    "title": "test.png",
                    "data": None,
                    "type": "image/png",
                    "url": "TEST_ATTACHMENT_URL"
                }
            ]
        }
    }
    
    assert message.to_dict() == expected_dict


def test_contented_message_serialization():
    
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
    
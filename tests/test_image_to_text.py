import asyncio
import importlib.util
import pytest
from unittest.mock import MagicMock, Mock, patch, AsyncMock

from task._models.message import Message
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl
from task._models.custom_content import Attachment, CustomContent
from tests.test_data import TEST_ATTACHMENT_URL, TEST_BASE64_IMAGE

TEST_QUESTION = "What do you see on this picture?"


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


class TestImageToText:
    

    def test_openai_itt_base64_image_analysis(self):
        
        task_module = load_task_module("task/image_to_text/openai/task_openai_itt.py", "task_openai_itt")
        start_openai_itt = task_module.start


        with patch('task._utils.model_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"role": "assistant", "content": "Test analysis result"}}]
            }
            mock_post.return_value = mock_response

            start_openai_itt()

            mock_post.assert_called()
            assert mock_post.call_count == 1

    def test_openai_itt_url_image_analysis(self):
        

        task_module = load_task_module("task/image_to_text/openai/task_openai_itt.py", "task_openai_itt")
        start_openai_itt = task_module.start


        with patch('task._utils.model_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"role": "assistant", "content": "Test analysis result"}}]
            }
            mock_post.return_value = mock_response

            start_openai_itt()


            assert mock_post.call_count == 1

    def test_openai_itt_contented_message_creation(self):
        
        img_url = ImgUrl(url=TEST_BASE64_IMAGE)
        img_content = ImgContent(image_url=img_url)
        txt_content = TxtContent(text=TEST_QUESTION)
        
        message = ContentedMessage(
            role=Role.USER,
            content=[img_content, txt_content]
        )
        
        assert message.role == Role.USER
        assert len(message.content) == 2
        assert isinstance(message.content[0], ImgContent)
        assert isinstance(message.content[1], TxtContent)
        assert message.content[1].text == "What do you see on this picture?"

    def test_openai_itt_message_serialization(self):
        
        img_url = ImgUrl(url=TEST_BASE64_IMAGE)
        img_content = ImgContent(image_url=img_url)
        txt_content = TxtContent(text=TEST_QUESTION)
        
        message = ContentedMessage(
            role=Role.USER,
            content=[img_content, txt_content]
        )
        
        expected_dict = {
            "role": "user",
            "content": [
                {
                    "image_url": {"url": TEST_BASE64_IMAGE},
                    "type": "image_url"
                },
                {
                    "text": TEST_QUESTION,
                    "type": "text"
                }
            ]
        }
        
        assert message.to_dict() == expected_dict

    def test_dial_itt_upload_image(self):
        
        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        _put_image = task_module._put_image


        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
             patch('builtins.open', create=True) as mock_file:


            mock_file.return_value.__enter__.return_value.read.return_value = b"fake_image_bytes"
            mock_path.return_value.parent = mock_path
            mock_path.return_value.__truediv__.return_value = mock_path


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

    def test_dial_itt_analysis(self):
        
        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        start_dial_itt = task_module.start


        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post:


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

    def test_dial_itt_message_with_attachment(self):
        
        attachment = Attachment(
            title="test.png",
            url=TEST_ATTACHMENT_URL,
            type="image/png"
        )
        
        custom_content = CustomContent(attachments=[attachment])
        
        message = Message(
            role=Role.USER,
            content=TEST_QUESTION,
            custom_content=custom_content
        )
        
        assert message.role == Role.USER
        assert message.content == "What do you see on this picture?"
        assert message.custom_content is not None
        assert len(message.custom_content.attachments) == 1
        assert message.custom_content.attachments[0].title == "test.png"

    def test_dial_itt_message_serialization_with_attachment(self):
        
        attachment = Attachment(
            title="test.png",
            url=TEST_ATTACHMENT_URL,
            type="image/png"
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
                        "title": "test.png",
                        "data": None,
                        "type": "image/png",
                        "url": TEST_ATTACHMENT_URL
                    }
                ]
            }
        }
        
        assert message.to_dict() == expected_dict

    def test_image_content_types_handling(self):
        

        base64_url = ImgUrl(url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        base64_img_content = ImgContent(image_url=base64_url)
        

        url_img_content = ImgContent(image_url=ImgUrl(url="https://example.com/image.jpg"))
        

        assert base64_img_content.image_url.url.startswith("data:image")
        assert url_img_content.image_url.url.startswith("https://")

    def test_dial_itt_complete_workflow(self):
        
        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        start_async = task_module.start_async

        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post, \
             patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
             patch('builtins.open', create=True) as mock_file, \
             patch('task.image_to_text.task_dial_itt._put_image') as mock_put_image:


            mock_file.return_value.__enter__.return_value.read.return_value = b"fake_image_bytes"
            mock_path.return_value.parent = mock_path
            mock_path.return_value.__truediv__.return_value = mock_path

            mock_attachment = Attachment(
                title="dialx-banner.png",
                url=TEST_ATTACHMENT_URL,
                type="image/png"
            )
            # Create a mock that returns an awaitable result
            mock_put_image.return_value = Mock()
            mock_put_image.return_value.__await__ = lambda x: iter([mock_attachment])


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
                "choices": [{"message": {"role": "assistant", "content": "Complete workflow analysis result"}}]
            }
            mock_requests_post.return_value = mock_response

            asyncio.run(start_async())

            mock_requests_post.assert_called_once()
            
    @pytest.mark.parametrize("filenames,model", [
        (["dialx-banner.png"], "gpt-4o"),
        (["dialx-banner.png"], "anthropic.claude-v3-haiku"),
        (["dialx-banner.png"], "gemini-1.5-pro"),
        (["dialx-banner.png", "dialx-banner.png"], "gpt-4o"),
        (["dialx-banner.png", "dialx-banner.png"], "anthropic.claude-v3-haiku"),
        (["dialx-banner.png", "dialx-banner.png"], "gemini-1.5-pro"),
    ])
    def test_multiple_models_and_images(self, filenames, model):
        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        start_async = task_module.start_async

        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post, \
             patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
             patch('builtins.open', create=True) as mock_file, \
             patch('task.image_to_text.task_dial_itt._put_image') as mock_put_image:

            mock_file.return_value.__enter__.return_value.read.return_value = b"fake_image_bytes"
            mock_path.return_value.parent = mock_path
            mock_path.return_value.__truediv__.return_value = mock_path

            # Mock the _put_image function to avoid async operations
            mock_attachment = Attachment(
                title="dialx-banner.png",
                url=TEST_ATTACHMENT_URL,
                type="image/png"
            )
            # Create a mock that returns an awaitable result
            mock_put_image.return_value = Mock()
            mock_put_image.return_value.__await__ = lambda x: iter([mock_attachment])

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
                "choices": [{"message": {"role": "assistant", "content": f"Analysis result for {model} with {len(filenames)} images"}}]
            }
            mock_requests_post.return_value = mock_response

            asyncio.run(start_async(filenames, model))

            mock_requests_post.assert_called_once()
            assert model in str(mock_requests_post.call_args)
            
    @pytest.mark.parametrize("filenames", [
        (["dialx-banner.png"]),
        (["dialx-banner.png", "dialx-banner.png"]),
        (["dialx-banner.png", "dialx-banner.png", "dialx-banner.png"]),
    ])
    def test_multiple_images_with_openai_model(self, filenames):
        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        start_async = task_module.start_async

        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post, \
             patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
             patch('builtins.open', create=True) as mock_file, \
             patch('task.image_to_text.task_dial_itt._put_image') as mock_put_image:

            mock_file.return_value.__enter__.return_value.read.return_value = b"fake_image_bytes"
            mock_path.return_value.parent = mock_path
            mock_path.return_value.__truediv__.return_value = mock_path

            # Mock the _put_image function to avoid async operations
            mock_attachment = Attachment(
                title="dialx-banner.png",
                url=TEST_ATTACHMENT_URL,
                type="image/png"
            )
            # Create a mock that returns an awaitable result
            mock_put_image.return_value = Mock()
            mock_put_image.return_value.__await__ = lambda x: iter([mock_attachment])

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
                "choices": [{"message": {"role": "assistant", "content": f"Analysis result for gpt-4o with {len(filenames)} images"}}]
            }
            mock_requests_post.return_value = mock_response

            asyncio.run(start_async(filenames, "gpt-4o"))

            mock_requests_post.assert_called_once()
            assert "gpt-4o" in str(mock_requests_post.call_args)
            
    def test_single_image_with_anthropic_model(self):
        task_module = load_task_module("task/image_to_text/task_dial_itt.py", "task_dial_itt")
        start_async = task_module.start_async

        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post, \
             patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
             patch('builtins.open', create=True) as mock_file, \
             patch('task.image_to_text.task_dial_itt._put_image') as mock_put_image:

            mock_file.return_value.__enter__.return_value.read.return_value = b"fake_image_bytes"
            mock_path.return_value.parent = mock_path
            mock_path.return_value.__truediv__.return_value = mock_path

            mock_attachment = Attachment(
                title="dialx-banner.png",
                url=TEST_ATTACHMENT_URL,
                type="image/png"
            )
            # Create a mock that returns an awaitable result
            mock_put_image.return_value = Mock()
            mock_put_image.return_value.__await__ = lambda x: iter([mock_attachment])

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
                "choices": [{"message": {"role": "assistant", "content": "Analysis result for anthropic.claude-v3-haiku with 1 image"}}]
            }
            mock_requests_post.return_value = mock_response

            asyncio.run(start_async(["dialx-banner.png"], "anthropic.claude-v3-haiku"))

            mock_requests_post.assert_called_once()
            assert "anthropic.claude-v3-haiku" in str(mock_requests_post.call_args)
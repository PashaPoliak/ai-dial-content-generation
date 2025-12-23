import asyncio
import importlib.util
from unittest.mock import MagicMock, Mock, patch, AsyncMock, mock_open
from tests.test_data import TEST_ATTACHMENT_URL
from task._models.message import Message
from task._models.role import Role
from task._models.custom_content import Attachment
from task.text_to_image.task_tti import Size, Quality, Style
from tests.mock_client import MockDialModelClient

HTTP_STATUS_OK = 200


def load_task_module(task_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, task_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"Could not load module from {task_path}")


class TestTextToImage:
    def test_size_class_values(self):
        assert Size.square == '1024x1024'
        assert Size.height_rectangle == '1024x1792'
        assert Size.width_rectangle == '1792x1024'

    def test_style_class_values(self):
        assert Style.natural == "natural"
        assert Style.vivid == "vivid"

    def test_quality_class_values(self):
        assert Quality.standard == "standard"
        assert Quality.hd == "hd"

    def test_save_images_function(self):
        task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
        _save_images = task_module._save_images

        TEST_IMAGE_TYPE = "image/png"
        mock_attachment = Attachment(
            title=TEST_IMAGE_TYPE,
            url=TEST_ATTACHMENT_URL,
            type=TEST_IMAGE_TYPE
        )

        with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('builtins.open', mock_open()) as mock_file:

            mock_http_instance = AsyncMock()
            mock_response_get = MagicMock()
            mock_response_get.content = b"fake_image_data"
            mock_response_get.raise_for_status.return_value = None
            mock_http_instance.get.return_value = mock_response_get
            mock_httpx_client.return_value = mock_http_instance

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_save_images([mock_attachment]))
            loop.close()


            mock_http_instance.get.assert_called()
            mock_file.assert_called_once()

    def test_tti_generation(self):
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

    def test_tti_generation_with_parameters(self):
        client = MockDialModelClient()

        prompt = "Sunny day on Bali"
        message = Message(
            role=Role.USER,
            content=prompt
        )

        custom_fields = {
            "size": Size.square,
            "quality": Quality.hd,
            "style": Style.vivid
        }

        result = client.get_completion([message], custom_fields=custom_fields)

        client.get_completion.assert_called_once()
        call_args = client.get_completion.call_args
        args, kwargs = call_args
        assert "custom_fields" in kwargs
        config = kwargs["custom_fields"]
        assert config["size"] == Size.square
        assert config["quality"] == Quality.hd
        assert config["style"] == Style.vivid

    def test_tti_generation_different_prompts(self):
        PROMPTS = [
            "Sunny day on Bali",
            "Mountain landscape at sunset",
            "Underwater coral reef",
            "City skyline at night"
        ]

        for prompt in PROMPTS:
            message = Message(
                role=Role.USER,
                content=prompt
            )

            assert message.role == Role.USER
            assert message.content == prompt

    def test_tti_generation_different_sizes(self):
        client = MockDialModelClient()

        message = Message(
            role=Role.USER,
            content="Test image"
        )

        sizes = [Size.square, Size.height_rectangle, Size.width_rectangle]

        for size in sizes:
            custom_fields = {"size": size}

            client.get_completion.reset_mock()
            result = client.get_completion([message], custom_fields=custom_fields)

            client.get_completion.assert_called_once()
            call_args = client.get_completion.call_args
            args, kwargs = call_args
            assert "custom_fields" in kwargs
            assert kwargs["custom_fields"]["size"] == size

    def test_tti_generation_different_styles(self):
        client = MockDialModelClient()

        message = Message(
            role=Role.USER,
            content="Test image"
        )

        styles = [Style.natural, Style.vivid]

        for style in styles:
            custom_fields = {"style": style}

            client.get_completion.reset_mock()
            result = client.get_completion([message], custom_fields=custom_fields)

            client.get_completion.assert_called_once()
            call_args = client.get_completion.call_args
            args, kwargs = call_args
            assert "custom_fields" in kwargs
            assert kwargs["custom_fields"]["style"] == style

    def test_tti_generation_different_qualities(self):
        client = MockDialModelClient()

        message = Message(
            role=Role.USER,
            content="Test image"
        )

        qualities = [Quality.standard, Quality.hd]

        for quality in qualities:
            custom_fields = {"quality": quality}

            client.get_completion.reset_mock()
            result = client.get_completion([message], custom_fields=custom_fields)

            client.get_completion.assert_called_once()
            call_args = client.get_completion.call_args
            args, kwargs = call_args
            assert "custom_fields" in kwargs
            assert kwargs["custom_fields"]["quality"] == quality

    def test_tti_complete_workflow(self):
        task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
        start_tti = task_module.start

        with patch('task.text_to_image.task_tti.DialModelClient') as mock_client_class, \
             patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
             patch('task._utils.model_client.requests.post') as mock_requests_post, \
             patch('builtins.open', mock_open()) as mock_file:

            mock_client_instance = MockDialModelClient()
            mock_client_instance.get_completion.return_value = Mock(
                custom_content=Mock(attachments=[Mock()])
            )
            mock_client_class.return_value = mock_client_instance


            mock_http_instance = AsyncMock()
            mock_response_get = MagicMock()
            mock_response_get.content = b"fake_image_data"
            mock_response_get.raise_for_status.return_value = None
            mock_http_instance.get.return_value = mock_response_get
            mock_httpx_client.return_value = mock_http_instance


            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {
                    "role": "assistant",
                    "content": "Generated image",
                    "custom_content": {
                        "attachments": [{"title": "generated_image.png", "url": "https://example.com/generated.png", "type": "image/png"}]
                    }
                }}]
            }
            mock_requests_post.return_value = mock_response

            start_tti()

            mock_requests_post.assert_called_once()
            mock_file.assert_called()
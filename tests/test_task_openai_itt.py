import pytest
import importlib.util
from unittest.mock import patch, MagicMock
from pathlib import Path
from tests.test_data import IMAGES
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl
from task._models.role import Role
from tests.mock_client import MockDialModelClient


def load_task_module(task_path, module_name):
    
    spec = importlib.util.spec_from_file_location(module_name, task_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"Could not load module from {task_path}")

@pytest.mark.parametrize("image_url", IMAGES)
def test_start_function_with_various_image_urls(image_url, mock_base64_image=MagicMock()):


    with patch("task._utils.model_client.DialModelClient") as mock_client_class, \
         patch("task._utils.model_client.requests.post") as mock_post:


        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Test response"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response


        task_module = load_task_module("task/image_to_text/openai/task_openai_itt.py", "task_openai_itt")
        start = task_module.start

        mock_client_instance = MockDialModelClient()
        mock_result = MagicMock()
        mock_result.content = "This is a test description of the image"
        mock_client_instance.get_completion.return_value = mock_result
        mock_client_class.return_value = mock_client_instance

        with patch("task.image_to_text.openai.task_openai_itt.Path") as mock_path, \
             patch("builtins.open", create=True) as mock_file, \
             patch("task.image_to_text.openai.task_openai_itt.print") as mock_print:

            mock_file.return_value.__enter__.return_value.read.return_value = b"fake_image_bytes"
            mock_path.return_value.parent = Path(".")
            mock_path.return_value.__truediv__.return_value = "fake_path"

            start()

        mock_client_class.assert_called_once()
        assert mock_client_instance.get_completion.call_count == 1

def test_contented_message_structure_with_base64_image():
    
    from tests.test_data import TEST_BASE64_IMAGE
    img_url = ImgUrl(url=TEST_BASE64_IMAGE)
    img_content = ImgContent(image_url=img_url)
    txt_content = TxtContent(text="What do you see on this picture?")
    
    message = ContentedMessage(
        role=Role.USER,
        content=[img_content, txt_content]
    )
    
    assert message.role == Role.USER
    assert len(message.content) == 2
    assert isinstance(message.content[0], ImgContent)
    assert isinstance(message.content[1], TxtContent)
    assert message.content[1].text == "What do you see on this picture?"


@pytest.mark.parametrize("url", IMAGES)
def test_contented_message_structure_with_url_image(url):
    
    url_img_content = ImgContent(image_url=ImgUrl(url=url))
    url_txt_content = TxtContent(text="What do you see on this picture?")
    
    url_message = ContentedMessage(
        role=Role.USER,
        content=[url_img_content, url_txt_content]
    )
    
    assert url_message.role == Role.USER
    assert len(url_message.content) == 2
    assert isinstance(url_message.content[0], ImgContent)
    assert isinstance(url_message.content[1], TxtContent)
    assert url_message.content[1].text == "What do you see on this picture?"
    assert url_message.content[0].image_url.url == url
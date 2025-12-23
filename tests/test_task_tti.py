import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import importlib.util

from task._models.custom_content import Attachment
from tests.mock_client import MockDialModelClient
from tests.test_data import IMAGES, TEST_ENDPOINT


def load_task_module(task_path, module_name):
    
    spec = importlib.util.spec_from_file_location(module_name, task_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"Could not load module from {task_path}")


@pytest.fixture
def mock_attachment():
    
    return Attachment(
        title='generated_image.png',
        url="https://example.com/generated_image.png",
        type='image/png'
    )


@pytest.fixture
def mock_image_bytes():
    
    return b"fake_image_bytes"


def create_mock_result_with_attachment():
    attachment = Attachment(
        title="generated_image.png",
        url="https://example.com/fake.png",
        type="image/png"
    )
    mock_result = MagicMock()
    mock_result.custom_content.attachments = [attachment]
    return mock_result, attachment


def setup_mock_client(mock_client_class, mock_result):
    mock_client_instance = MockDialModelClient()
    mock_client_instance.get_completion.return_value = mock_result
    mock_client_class.return_value = mock_client_instance
    return mock_client_instance


def setup_mock_responses(status_code=200, has_attachments=True):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    
    if has_attachments:
        mock_response.json.return_value = {
            "choices": [{"message": {
                "role": "assistant",
                "content": "Generated image",
                "custom_content": {
                    "attachments": [{"title": "generated_image.png", "url": "https://example.com/generated.png", "type": "image/png"}]
                }
            }}]
        }
    else:
        mock_response.json.return_value = {
            "choices": [{"message": {"role": "assistant", "content": "Generated image"}}]
        }
    
    return mock_response


@pytest.mark.parametrize("url", IMAGES)
@pytest.mark.asyncio
async def test_save_images_function(url, mock_image_bytes):

    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    _save_images = task_module._save_images
    
    
    attachments = [
        Attachment(
            title='generated_image.png',
            url=url,
            type='image/png'
        )
    ]
    with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
         patch("builtins.open", create=True) as mock_open, \
         patch("task.text_to_image.task_tti.datetime") as mock_datetime:


         mock_http_instance = AsyncMock()
         mock_response_get = MagicMock()
         mock_response_get.content = mock_image_bytes
         mock_response_get.raise_for_status.return_value = None
         mock_http_instance.get.return_value = mock_response_get
         mock_httpx_client.return_value = mock_http_instance
    

         mock_file_instance = MagicMock()
         mock_open.return_value.__enter__.return_value = mock_file_instance
    

         mock_datetime.now.return_value.strftime.return_value = "test_time"
    
         await _save_images(attachments)


         mock_http_instance.get.assert_called()
         assert mock_http_instance.get.call_count == len(attachments)
         for i, attachment in enumerate(attachments):
             mock_http_instance.get.assert_any_call(f"/v1/{attachment.url}")
         mock_file_instance.write.assert_called_with(mock_image_bytes)


def test_size_class():
    

    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    Size = task_module.Size
    
    assert Size.square == '1024x1024'
    assert Size.height_rectangle == '1024x1792'
    assert Size.width_rectangle == '1792x1024'


def test_style_class():
    

    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    Style = task_module.Style
    
    assert Style.natural == "natural"
    assert Style.vivid == "vivid"


def test_quality_class():
    

    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    Quality = task_module.Quality
    
    assert Quality.standard == "standard"
    assert Quality.hd == "hd"


@pytest.mark.parametrize("prompt", [
    "Sunny day on Bali",
    "Mountain landscape at sunset",
    "Underwater coral reef",
    "City skyline at night",
    "Forest in autumn"
])
def test_start_function_success(prompt):
    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    start = task_module.start


    attachment = Attachment(
        title="generated_image.png",
        url="https://example.com/fake.png",
        type="image/png"
    )

    with patch('task.text_to_image.task_tti.DialModelClient') as mock_client_class, \
     patch('task._utils.model_client.requests.post') as mock_requests_post, \
     patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
     patch(
         "task.text_to_image.task_tti._save_images",
         new_callable=MagicMock
     ) as mock_save_images, \
     patch(
         "task.text_to_image.task_tti.print"
     ) as mock_print, \
     patch(
         "asyncio.run"
     ) as mock_asyncio_run:


       mock_result, attachment = create_mock_result_with_attachment()
       setup_mock_client(mock_client_class, mock_result)


       mock_response_with_attachments = setup_mock_responses(status_code=200, has_attachments=True)
       mock_requests_post.return_value = mock_response_with_attachments

       mock_http_instance = AsyncMock()
       mock_httpx_client.return_value = mock_http_instance

       def run_sync_function(coro):
           # Create a new event loop to run the coroutine
           import sys
           if sys.version_info >= (3, 7):
               loop = asyncio.new_event_loop()
               asyncio.set_event_loop(loop)
               try:
                   return loop.run_until_complete(coro)
               finally:
                   loop.close()
                   # Restore original event loop if there was one
                   try:
                       original_loop = asyncio.get_running_loop()
                   except RuntimeError:
                       original_loop = None
                   if original_loop is not None:
                       asyncio.set_event_loop(original_loop)
           else:
               # For older Python versions
               loop = asyncio.new_event_loop()
               asyncio.set_event_loop(loop)
               result = loop.run_until_complete(coro)
               loop.close()
               return result
       mock_asyncio_run.side_effect = run_sync_function

       start()

       mock_requests_post.assert_called_once()
        

def test_start_function_no_attachments():
    

    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    start = task_module.start
    with patch("task.text_to_image.task_tti.DialModelClient") as mock_client_class, \
         patch('task._utils.model_client.requests.post') as mock_requests_post, \
         patch("task.text_to_image.task_tti.print") as mock_print:

         mock_client_instance = MockDialModelClient(
             endpoint=TEST_ENDPOINT,
             deployment_name="imagegeneration@005",
             api_key="test_key"
         )
         mock_result = MagicMock()
         mock_result.custom_content = None
         mock_client_instance.get_completion.return_value = mock_result
         mock_client_class.return_value = mock_client_instance


         mock_response = MagicMock()
         mock_response.status_code = 200
         mock_response.json.return_value = {
             "choices": [{"message": {"role": "assistant", "content": "Generated image"}}]
         }
         mock_requests_post.return_value = mock_response

          

         start("Sunny day on Bali")




def test_start_function_exception():
    

    task_module = load_task_module("task/text_to_image/task_tti.py", "task_tti")
    start = task_module.start
    with patch('task._utils.model_client.requests.post') as mock_requests_post, \
         patch("task.text_to_image.task_tti.print") as mock_print:


         mock_requests_post.side_effect = Exception("Test error")

         start("Sunny day on Bali")


         
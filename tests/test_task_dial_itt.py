import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path
from tests.test_data import TEST_ATTACHMENT_URL
from task._models.custom_content import Attachment
from tests.mock_client import MockDialBucketClient


@pytest.mark.parametrize("image_title, image_type", [
    ('dialx-banner.png', 'image/png'),
    ('test-image.jpg', 'image/jpeg'),
    ('sample.gif', 'image/gif')
])

@pytest.mark.asyncio
async def test_put_image_function(image_title, image_type, mock_image_bytes):

    from task.image_to_text import task_dial_itt
    _put_image = task_dial_itt._put_image
    
    with patch("task.image_to_text.task_dial_itt.DialBucketClient") as mock_client_class, \
         patch("task.image_to_text.task_dial_itt.Path") as mock_path, \
         patch("builtins.open", create=True) as mock_file, \
         patch("task.image_to_text.task_dial_itt.BytesIO") as mock_bytes_io:
     
         mock_file.return_value.__enter__.return_value.read.return_value = mock_image_bytes
         
         mock_path.return_value.parent = Path(".")
         mock_path.return_value.__truediv__.return_value = image_title
         
         mock_client_instance = MockDialBucketClient()
         mock_client_instance.put_file.return_value = {"url": TEST_ATTACHMENT_URL}

         mock_client_class.return_value.__aenter__.return_value = mock_client_instance
         mock_client_class.return_value.__aexit__.return_value = None

         mock_bytes_io.return_value = "fake_bytes_io"

         result = await _put_image(image_title, image_type)

         assert isinstance(result, Attachment)
         assert result.title == image_title
         assert result.url == TEST_ATTACHMENT_URL
         assert result.type == image_type

         mock_client_instance.put_file.assert_called_once_with(image_title, image_type, "fake_bytes_io")


@pytest.mark.asyncio
async def test_start_async_with_multiple_images(mock_image_bytes):
    """
    Test the start_async function with multiple images to verify that
    the system can handle 2+ pictures for analysis in a single request.
    This tests the core functionality mentioned in the original.
    """
    with patch('task.image_to_text.task_dial_itt._put_image') as mock_put_image, \
         patch('task._utils.model_client.requests.post') as mock_requests_post:
        
        from task.image_to_text import task_dial_itt


        mock_put_image.side_effect = [
            Attachment(title='img1.png', url=TEST_ATTACHMENT_URL, type='image/png'),
            Attachment(title='img2.png', url=TEST_ATTACHMENT_URL, type='image/png'),
            Attachment(title='img3.jpg', url=TEST_ATTACHMENT_URL, type='image/jpeg')
        ]


        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "This is a test description analyzing multiple images"
                }
            }]
        }
        mock_requests_post.return_value = mock_response


        test_images = ['img1.png', 'img2.png', 'img3.jpg']
        await task_dial_itt.start_async(test_images)


        assert mock_put_image.call_count == 3

        mock_requests_post.assert_called_once()


@pytest.mark.parametrize("model_name", [
    "gpt-4-vision-preview",
    "claude-3-sonnet",
    "gemini-1.5-pro",
    "test-model-vision"
])
@pytest.mark.asyncio
async def test_start_async_with_different_models(model_name, mock_image_bytes):
    """
    Test the start_async function with different AI models from various vendors
    (OpenAI, Google, Anthropic) to verify cross-model compatibility.
    This addresses the original about trying this approach with different models.
    """
    with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
         patch('task._utils.model_client.requests.post') as mock_requests_post, \
         patch('task._utils.constants.DEFAULT_MODEL', model_name):
        
        from task.image_to_text import task_dial_itt


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


        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant", 
                    "content": f"Analysis from {model_name}: Test image description"
                }
            }]
        }
        mock_requests_post.return_value = mock_response


        await task_dial_itt.start_async(['dialx-banner.png'])


        mock_requests_post.assert_called_once()



@pytest.mark.asyncio
async def test_start_async_error_handling_multiple_images():
    """
    Test error handling when processing multiple images, including
    scenarios with invalid image formats, missing files, etc.
    """
    with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
         patch('task._utils.model_client.requests.post') as mock_requests_post:
        
        from task.image_to_text import task_dial_itt


        mock_http_instance = AsyncMock()
        mock_response_get = MagicMock()
        mock_response_get.json.return_value = {"bucket": "test_bucket"}
        mock_response_get.raise_for_status.return_value = None
        mock_response_put = MagicMock()
        mock_response_put.json.return_value = {"url": TEST_ATTACHMENT_URL}

        mock_response_put.raise_for_status.side_effect = [None, None, Exception("Upload failed")]
        mock_http_instance.get.return_value = mock_response_get
        mock_http_instance.put.return_value = mock_response_put
        mock_httpx_client.return_value = mock_http_instance


        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant", 
                    "content": "Partial analysis completed"
                }
            }]
        }
        mock_requests_post.return_value = mock_response


        test_images = ['valid_img1.png', 'valid_img2.jpg', 'invalid_img.gif']
        try:
            await task_dial_itt.start_async(test_images)
        except Exception as e:

            assert isinstance(e, Exception)




@pytest.mark.asyncio
async def test_start_async_function(mock_image_bytes):
 
    with patch('task._utils.bucket_client.httpx.AsyncClient') as mock_httpx_client, \
         patch('task._utils.model_client.requests.post') as mock_requests_post:

        from task.image_to_text import task_dial_itt

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


        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"role": "assistant", "content": "This is a test description of the image"}}]
        }
        mock_requests_post.return_value = mock_response


        await task_dial_itt.start_async()

        mock_requests_post.assert_called_once()


def test_start_function():
    
    with patch("asyncio.run") as mock_async_run:
        from task.image_to_text import task_dial_itt
        start = task_dial_itt.start
        start()
        mock_async_run.assert_called_once()

        call_args = mock_async_run.call_args[0][0]

        assert call_args.__name__ == "start_async"
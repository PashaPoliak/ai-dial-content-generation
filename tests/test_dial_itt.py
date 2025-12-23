import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from task.image_to_text.task_dial_itt import _put_image, start, start_async
from task._models.custom_content import Attachment
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


TEST_IMAGE_TITLE = 'dialx-banner.png'
TEST_IMAGE_URL = 'http://example.com/test.png'
TEST_IMAGE_TYPE = 'image/png'
TEST_JPG_TITLE = 'test-image.jpg'
TEST_JPG_URL = 'http://example.com/test.jpg'
TEST_JPG_URL_2 = 'http://example.com/test2.jpg'
TEST_JPG_TYPE = 'image/jpeg'


@pytest.mark.asyncio
async def test_put_image_creates_attachment():
    """Test that _put_image creates an attachment correctly."""
    with patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.image_to_text.task_dial_itt.DialBucketClient') as mock_bucket_client_class:
        

        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: mock_path_instance
        mock_path.return_value = mock_path_instance
        mock_path_instance.__str__ = MagicMock(return_value=TEST_IMAGE_TITLE)
        

        mock_file = MagicMock()
        mock_file.read.return_value = b'test_image_data'
        mock_open.return_value.__enter__.return_value = mock_file
        

        mock_bucket_instance = AsyncMock()
        mock_bucket_client_class.return_value.__aenter__.return_value = mock_bucket_instance
        mock_bucket_instance.put_file.return_value = {'url': TEST_IMAGE_URL}
        

        result = await _put_image()
        

        mock_bucket_instance.put_file.assert_called_once()
        assert isinstance(result, Attachment)
        assert result.title == TEST_IMAGE_TITLE
        assert result.url == TEST_IMAGE_URL
        assert result.type == TEST_IMAGE_TYPE


def test_start_function_with_mocked_dependencies():
    
    with patch('task.image_to_text.task_dial_itt.DialModelClient') as mock_model_client_class, \
         patch('task.image_to_text.task_dial_itt.start_async', new_callable=AsyncMock) as mock_start_async, \
         patch('builtins.print') as mock_print, \
         patch('asyncio.run') as mock_asyncio_run:
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = Message(
            role=Role.USER,
            content="Test response"
        )
        mock_model_client_class.return_value = mock_model_instance
        

        mock_attachment = Attachment(
            title=TEST_IMAGE_TITLE,
            url=TEST_IMAGE_URL,
            type=TEST_IMAGE_TYPE
        )
        mock_start_async.return_value = [mock_attachment]
        mock_asyncio_run.return_value = [mock_attachment]
        

        start()


@pytest.mark.asyncio
async def test_put_image_with_different_mime_types():
    """Test _put_image with different image types."""
    with patch('task.image_to_text.task_dial_itt.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.image_to_text.task_dial_itt.DialBucketClient') as mock_bucket_client_class:
        

        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: mock_path_instance
        mock_path.return_value = mock_path_instance
        mock_path_instance.__str__ = MagicMock(return_value=TEST_JPG_TITLE)
        

        mock_file = MagicMock()
        mock_file.read.return_value = b'test_image_data'
        mock_open.return_value.__enter__.return_value = mock_file
        

        mock_bucket_instance = AsyncMock()
        mock_bucket_client_class.return_value.__aenter__.return_value = mock_bucket_instance
        mock_bucket_instance.put_file.return_value = {'url': TEST_JPG_URL}
        

        await _put_image()


def test_start_function_multiple_images():
    
    with patch('task.image_to_text.task_dial_itt.DialModelClient') as mock_model_client_class, \
         patch('task.image_to_text.task_dial_itt.start_async', new_callable=AsyncMock) as mock_start_async, \
         patch('builtins.print') as mock_print, \
         patch('asyncio.run') as mock_asyncio_run:
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = Message(
            role=Role.USER,
            content="Test response with multiple images"
        )
        mock_model_client_class.return_value = mock_model_instance
        

        mock_attachments = [
            Attachment(
                title=TEST_IMAGE_TITLE,
                url=TEST_IMAGE_URL,
                type=TEST_IMAGE_TYPE
            ),
            Attachment(
                title=TEST_JPG_TITLE,
                url=TEST_JPG_URL_2,
                type=TEST_JPG_TYPE
            )
        ]
        mock_start_async.return_value = mock_attachments
        mock_asyncio_run.return_value = mock_attachments
        

        start()
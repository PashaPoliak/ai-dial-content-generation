from datetime import datetime
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from task.text_to_image.task_tti import _save_images, start
from task._models.custom_content import Attachment
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


@pytest.mark.asyncio
async def test_save_images_with_png_attachments():
    """Test _save_images function with PNG attachments."""
    with patch('task.text_to_image.task_tti.DialBucketClient') as mock_bucket_client_class, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.text_to_image.task_tti.datetime') as mock_datetime:
        

        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        

        test_attachments = [
            Attachment(
                title='test1.png',
                url='http://example.com/test1.png',
                type='image/png'
            )
        ]
        

        mock_bucket_instance = AsyncMock()
        mock_bucket_instance.get_file.return_value = b'test_image_data'
        mock_bucket_client_class.return_value.__aenter__.return_value = mock_bucket_instance
        

        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle
        
        await _save_images(test_attachments)


@pytest.mark.asyncio
async def test_save_images_with_multiple_attachments():
    """Test _save_images function with multiple attachments."""
    with patch('task.text_to_image.task_tti.DialBucketClient') as mock_bucket_client_class, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.text_to_image.task_tti.datetime') as mock_datetime:
        

        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        

        test_attachments = [
            Attachment(
                title='test1.png',
                url='http://example.com/test1.png',
                type='image/png'
            ),
            Attachment(
                title='test2.png',
                url='http://example.com/test2.png',
                type='image/png'
            )
        ]
        

        mock_bucket_instance = AsyncMock()
        mock_bucket_instance.get_file.return_value = b'test_image_data'
        mock_bucket_client_class.return_value.__aenter__.return_value = mock_bucket_instance
        

        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle
        
        await _save_images(test_attachments)


def test_start_function_with_mocked_dependencies():
    
    with patch('task.text_to_image.task_tti.DialModelClient') as mock_model_client_class, \
         patch('task.text_to_image.task_tti._save_images') as mock_save_images, \
         patch('builtins.print') as mock_print:
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = Message(
            role=Role.USER,
            content="Test response",
            custom_content=MagicMock()
        )
        mock_model_client_class.return_value = mock_model_instance
        

        mock_custom_content = MagicMock()
        mock_custom_content.attachments = [
            Attachment(
                title='generated.png',
                url='http://example.com/generated.png',
                type='image/png'
            )
        ]
        mock_model_instance.get_completion.return_value.custom_content = mock_custom_content
        

        mock_save_images.return_value = None
        
        start()


def test_start_function_with_custom_fields():
    
    with patch('task.text_to_image.task_tti.DialModelClient') as mock_model_client_class, \
         patch('task.text_to_image.task_tti._save_images') as mock_save_images, \
         patch('builtins.print') as mock_print:
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = Message(
            role=Role.USER,
            content="Test response",
            custom_content=MagicMock()
        )
        mock_model_client_class.return_value = mock_model_instance
        

        mock_custom_content = MagicMock()
        mock_custom_content.attachments = [
            Attachment(
                title='generated.png',
                url='http://example.com/generated.png',
                type='image/png'
            )
        ]
        mock_model_instance.get_completion.return_value.custom_content = mock_custom_content
        

        mock_save_images.return_value = None
        
        start()


def test_start_function_with_google_model():
    
    with patch('task.text_to_image.task_tti.DialModelClient') as mock_model_client_class, \
         patch('task.text_to_image.task_tti._save_images') as mock_save_images, \
         patch('builtins.print') as mock_print:
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = Message(
            role=Role.USER,
            content="Test response with Google model",
            custom_content=MagicMock()
        )
        mock_model_client_class.return_value = mock_model_instance
        

        mock_custom_content = MagicMock()
        mock_custom_content.attachments = [
            Attachment(
                title='generated_google.png',
                url='http://example.com/generated_google.png',
                type='image/png'
            )
        ]
        mock_model_instance.get_completion.return_value.custom_content = mock_custom_content
        

        mock_save_images.return_value = None
        
        start()
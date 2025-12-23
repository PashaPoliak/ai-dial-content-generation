import base64
from unittest.mock import MagicMock, patch

from task.image_to_text.openai.task_openai_itt import start
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent


def test_start_function_with_mocked_dependencies():
    
    with patch('task.image_to_text.openai.task_openai_itt.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.image_to_text.openai.task_openai_itt.DialModelClient') as mock_model_client_class, \
         patch('builtins.print') as mock_print:
        

        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: mock_path_instance
        mock_path.return_value = mock_path_instance
        mock_path_instance.__str__ = MagicMock(return_value='dialx-banner.png')
        

        mock_file = MagicMock()
        mock_file.read.return_value = b'test_image_data'
        mock_open.return_value.__enter__.return_value = mock_file
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = ContentedMessage(
            role=Role.USER,
            content=[
                TxtContent(text="Test response")
            ]
        )
        mock_model_client_class.return_value = mock_model_instance
        

        start()


def test_start_function_base64_encoding():
    
    with patch('task.image_to_text.openai.task_openai_itt.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.image_to_text.openai.task_openai_itt.DialModelClient') as mock_model_client_class, \
         patch('builtins.print') as mock_print:
        

        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: mock_path_instance
        mock_path.return_value = mock_path_instance
        mock_path_instance.__str__ = MagicMock(return_value='dialx-banner.png')
        

        test_image_data = b'test_image_bytes'
        expected_base64 = base64.b64encode(test_image_data).decode('utf-8')
        
        mock_file = MagicMock()
        mock_file.read.return_value = test_image_data
        mock_open.return_value.__enter__.return_value = mock_file
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = ContentedMessage(
            role=Role.USER,
            content=[
                TxtContent(text="Test response")
            ]
        )
        mock_model_client_class.return_value = mock_model_instance
        

        start()


def test_start_function_with_different_models():
    
    with patch('task.image_to_text.openai.task_openai_itt.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.image_to_text.openai.task_openai_itt.DialModelClient') as mock_model_client_class, \
         patch('builtins.print') as mock_print:
        

        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: mock_path_instance
        mock_path.return_value = mock_path_instance
        mock_path_instance.__str__ = MagicMock(return_value='dialx-banner.png')
        

        mock_file = MagicMock()
        mock_file.read.return_value = b'test_image_data'
        mock_open.return_value.__enter__.return_value = mock_file
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = ContentedMessage(
            role=Role.USER,
            content=[
                TxtContent(text="Test response for different model")
            ]
        )
        mock_model_client_class.return_value = mock_model_instance
        

        start()


def test_start_function_with_downloadable_image():
    
    with patch('task.image_to_text.openai.task_openai_itt.Path') as mock_path, \
         patch('builtins.open', create=True) as mock_open, \
         patch('task.image_to_text.openai.task_openai_itt.DialModelClient') as mock_model_client_class, \
         patch('builtins.print') as mock_print:
        

        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: mock_path_instance
        mock_path.return_value = mock_path_instance
        mock_path_instance.__str__ = MagicMock(return_value='dialx-banner.png')
        

        mock_file = MagicMock()
        mock_file.read.return_value = b'test_image_data'
        mock_open.return_value.__enter__.return_value = mock_file
        

        mock_model_instance = MagicMock()
        mock_model_instance.get_completion.return_value = ContentedMessage(
            role=Role.USER,
            content=[
                TxtContent(text="Test response with downloadable image")
            ]
        )
        mock_model_client_class.return_value = mock_model_instance
        

        start()
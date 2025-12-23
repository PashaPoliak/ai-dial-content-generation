import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from task.image_to_text.openai.message import ImgUrl


def test_base64_image_logic_with_mock():
    with patch("task.image_to_text.openai.task_openai_itt.Path") as mock_path, \
         patch("builtins.open", mock_open(read_data=b"fake_image_bytes")) as mock_file, \
         patch("task.image_to_text.openai.task_openai_itt.DialModelClient") as MockClientClass:
        
        mock_path.return_value.parent = Path(".")
        mock_path.return_value.__truediv__.return_value = "fake_path"
        
        mock_client_instance = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "This is a test description of the image"
        mock_client_instance.get_completion.return_value = mock_result
        
        MockClientClass.return_value = mock_client_instance
        
        from task.image_to_text.openai.task_openai_itt import start
        start()
        
        assert mock_client_instance.get_completion.called


def test_img_url_logic_directly():
    base64_image_empty = ""
    img_url = ImgUrl(url=f"data:image/png;base64,{base64_image_empty}" if base64_image_empty else "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg")
    assert img_url.url == "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"
    
    base64_image_valid = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    img_url = ImgUrl(url=f"data:image/png;base64,{base64_image_valid}" if base64_image_valid else "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg")
    expected_url = f"data:image/png;base64,{base64_image_valid}"
    assert img_url.url == expected_url
    
    base64_image_none = None
    img_url = ImgUrl(url=f"data:image/png;base64,{base64_image_none}" if base64_image_none else "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg")
    assert img_url.url == "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"

    base64_image_whitespace = "   "
    img_url = ImgUrl(url=f"data:image/png;base64,{base64_image_whitespace}" if base64_image_whitespace.strip() else "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg")
    assert img_url.url == "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"


if __name__ == "__main__":
    test_base64_image_logic_with_mock()
    test_img_url_logic_directly()
    
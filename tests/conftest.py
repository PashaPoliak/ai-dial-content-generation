import base64
import os
from pathlib import Path
import pytest
from tests.test_data import TEST_API_KEY, TEST_ATTACHMENT_TITLE, TEST_ATTACHMENT_URL



os.environ['DIAL_API_KEY'] = TEST_API_KEY


@pytest.fixture
def CHOICES_DATA():
    from tests.test_data import CHOICES_DATA
    return CHOICES_DATA


@pytest.fixture
def mock_image_bytes():
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent / file_name
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    return image_bytes


@pytest.fixture
def mock_base64_image(mock_image_bytes):
    return base64.b64encode(mock_image_bytes).decode('utf-8')




@pytest.fixture
def mock_attachment():
    from task._models.custom_content import Attachment
    return Attachment(
        title=TEST_ATTACHMENT_TITLE,
        data=None,
        type="image/png",
        url=TEST_ATTACHMENT_URL
    )


@pytest.fixture
def prompts():
    return [
        "Sunny day on Bali",
        "Mountain landscape at sunset",
        "Underwater coral reef",
        "City skyline at night",
        "Forest in autumn"
    ]
TEST_API_KEY = "test_key"
TEST_MODEL_NAME = "test-model"
TEST_CONTENT = "Test TTI!"
TEST_ATTACHMENT_TYPE = "image/png"
TEST_ATTACHMENT_TITLE = "dialx-banner.png"
TEST_BASE64_IMAGE = "data:image/png;base64,test_base64"
TEST_ATTACHMENT_URL = "https://raw.githubusercontent.com/PashaPoliak/ai-dial-content-generation/refs/heads/main/dialx-banner.png"
TEST_ENDPOINT="https://test-endpoint.com/deployments/test-model/chat/completions"
API_KEY_ERROR_MESSAGE = "API key cannot be null or empty"
IMAGE_GENERATION_MODEL = "imagegeneration@005"

IMAGES =[
    "https://animals.com/media/2019/11/Elephant-male-1024x535.jpg",
    "https://animals.com/test-image.png",
    "https://animals.com/sample.jpg"
]

CHOICES_DATA = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Test response"
            }
        }
    ]
}
import os

DIAL_URL = 'https://ai-proxy.lab.epam.com'
"""
Base URL for the DIAL service.
"""

DIAL_CHAT_COMPLETIONS_ENDPOINT = DIAL_URL + '/openai/deployments/{model}/chat/completions'
"""
Endpoint template for DIAL chat completions API.
"""

API_KEY = os.getenv('DIAL_API_KEY', '')
"""
API key for authenticating with the DIAL service, retrieved from environment variables.
"""

DEFAULT_MODEL = "anthropic.claude-v3-haiku"
"""
Default model name to use when no specific model is specified.
"""

DEFAULT_IMAGE_URL="https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"
"""
Default image URL used for testing and examples.
"""

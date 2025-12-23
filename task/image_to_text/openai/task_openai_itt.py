import base64
import logging
from pathlib import Path

from task._utils.constants import API_KEY, DEFAULT_IMAGE_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl

from task._models.message import Message

def convert_contented_message_to_message(contented_message: ContentedMessage) -> Message:
    """
    Convert a ContentedMessage to a standard Message object.
    
    Args:
        contented_message (ContentedMessage): The ContentedMessage to convert
        
    Returns:
        Message: A standard Message object with combined content
    """
    text_content = ""
    for content_item in contented_message.content:
        if isinstance(content_item, TxtContent):
            text_content += content_item.text
        elif isinstance(content_item, ImgContent):
            text_content += f"[Image: {content_item.image_url.url}] "
    
    return Message(
        role=contented_message.role,
        content=text_content
    )


def start() -> None:
    """
    Start the image analysis process using OpenAI's GPT-4 Vision model.
    
    This function loads an image, converts it to base64, and sends it to the model
    for analysis with a prompt asking what is visible in the image.
    """
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name='gpt-4o',
        api_key=API_KEY
    )

    if not base64_image:
       img_url = ImgUrl(url=DEFAULT_IMAGE_URL)
    else:
       img_url = ImgUrl(url=f"data:image/png;base64,{base64_image}")
    
    img_content = ImgContent(image_url=img_url)
    txt_content = TxtContent(text="What do you see on this picture?")
    
    message = ContentedMessage(
        role=Role.USER,
        content=[img_content, txt_content]
    )
    
    message_as_message = convert_contented_message_to_message(message)
    
    result = client.get_completion([message_as_message])
    logging.info(result.content)


if __name__ == "__main__":
    start()

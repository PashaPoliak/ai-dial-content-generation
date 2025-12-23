import asyncio
from io import BytesIO
from pathlib import Path
import logging
from typing import List, Optional

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image(file_name: str = 'dialx-banner.png', mime_type: str = 'image/png') -> Attachment:
    """
    Upload an image file to the DIAL bucket and return an attachment object.
    
    Args:
        file_name (str): Name of the image file to upload. Defaults to 'dialx-banner.png'
        mime_type (str): MIME type of the image. Defaults to 'image/png'
        
    Returns:
        Attachment: An attachment object containing the uploaded image information
    """
    image_path = Path(__file__).parent.parent.parent / file_name
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as client:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        
        image_io = BytesIO(image_bytes)
        
        result = await client.put_file(file_name, mime_type, image_io)
        
        return Attachment(
            title=file_name,
            url=result.get("url"),
            type=mime_type
        )


async def start_async(filenames: Optional[List[str]] = None, model: str = 'anthropic.claude-v3-haiku') -> None:
    """
    Asynchronously analyze images using a specified model.
    
    Args:
        filenames (Optional[List[str]]): List of image filenames to analyze. Defaults to ['dialx-banner.png']
        model (str): Name of the model to use for analysis. Defaults to 'anthropic.claude-v3-haiku'
    """
    if filenames is None:
        filenames = ['dialx-banner.png']
        
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name=model,
        api_key=API_KEY
    )
    
    attachments = []
    for filename in filenames:
        attachments.append(await _put_image(filename))
    
    logging.info("Attachments: %s", attachments)
    
    message = Message(
        role=Role.USER,
        content="Analyze these images and describe what you see. If multiple images are provided, compare and contrast them.",
        custom_content=CustomContent(attachments=attachments)
    )
    
    result = client.get_completion([message])
    
    logging.info(f"Model {model}: {result.content}")


def start(filenames: Optional[List[str]] = None) -> None:
    """
    Synchronously start the image analysis process.
    
    Args:
        filenames (Optional[List[str]]): List of image filenames to analyze. Defaults to None
    """
    asyncio.run(start_async(filenames))


if __name__ == "__main__":
    start()
    
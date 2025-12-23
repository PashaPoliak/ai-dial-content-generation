import asyncio
from datetime import datetime
import logging
from typing import List

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    """
    Class representing the size options for generated images.
    
    Attributes:
        square (str): Square image size (1024x1024)
        height_rectangle (str): Portrait rectangle image size (1024x1792)
        width_rectangle (str): Landscape rectangle image size (1792x1024)
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    Class representing the style options for generated images.
    
    Attributes:
        natural (str): Natural style for more realistic images
        vivid (str): Vivid style for more dramatic images
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    Class representing the quality options for generated images.
    
    Attributes:
        standard (str): Standard quality
        hd (str): High definition quality
    """
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: List[Attachment]):
    """
    Save image attachments locally with timestamped filenames.
    
    Args:
        attachments (List[Attachment]): List of image attachments to save
    """
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as client:
        for attachment in attachments:
            if attachment.url:
                image_bytes = await client.get_file(attachment.url)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}.png"
                
                with open(filename, "wb") as f:
                    f.write(image_bytes)
                
                logging.info(f"Image saved locally as {filename}")


async def start_async(prompt: str = "Sunny day on Bali") -> None:
    """
    Asynchronously generate an image based on the given prompt.
    
    Args:
        prompt (str): The text prompt to generate an image from. Defaults to "Sunny day on Bali"
    """
    try:
        client = DialModelClient(
            endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
            deployment_name='dall-e-3',
            api_key=API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=prompt
        )
        
        custom_fields = {
            "size": Size.square,
            "quality": Quality.hd,
            "style": Style.vivid
        }
        
        result = client.get_completion(
            messages=[message],
            custom_fields=custom_fields
        )
        
        if result.custom_content and result.custom_content.attachments:
            await _save_images(result.custom_content.attachments)
            logging.info("Image generation completed successfully!")
        else:
            logging.info("No attachments found in the response.")
            
    except Exception as e:
        logging.error(f"Error during image generation: {e}")


def start(prompt: str = "Sunny day on Bali") -> None:
    """
    Synchronously start the image generation process.
    
    Args:
        prompt (str): The text prompt to generate an image from. Defaults to "Sunny day on Bali"
    """
    asyncio.run(start_async(prompt))


if __name__ == "__main__":
    start()

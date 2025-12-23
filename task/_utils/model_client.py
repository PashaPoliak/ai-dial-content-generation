import json
from typing import Any, Dict, List, Optional

import requests

from task._models.message import Message
from task._utils.request import print_request


class DialModelClient:
    """
    Client for interacting with DIAL model completion service.
    
    This client provides methods to get completions from DIAL models.
    
    Attributes:
        _endpoint (str): The API endpoint for the model
        _api_key (str): API key for authentication
    """
    _endpoint: str
    _api_key: str

    def __init__(self, endpoint: str, deployment_name: str, api_key: str):
        """
        Initialize the DIAL model client.
        
        Args:
            endpoint (str): The API endpoint template for the model
            deployment_name (str): Name of the model deployment
            api_key (str): API key for authentication
            
        Raises:
            ValueError: If the API key is null or empty
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        self._endpoint = endpoint.format(
            model=deployment_name
        )
        self._api_key = api_key


    def get_completion(self, messages: List[Message], custom_fields: Optional[Dict[str, Any]] = None, **kwargs) -> Message:
        """
        Get completion from the DIAL model.
        
        Args:
            messages (List[Message]): List of messages to send to the model
            custom_fields (Optional[Dict[str, Any]]): Optional custom fields for the request
            **kwargs: Additional parameters to pass to the model
            
        Returns:
            Message: The response message from the model
            
        Raises:
            ValueError: If no choices or message is present in the response
            Exception: If the HTTP request fails
        """
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }

        request_data: Dict[str, Any] = {
            "messages": [msg.to_dict() for msg in messages],
            **kwargs
        }
        if custom_fields:
            request_data["custom_fields"] = {
                "configuration": {**custom_fields}
            }

        print_request(endpoint=self._endpoint, request_data=request_data, headers=headers)

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            import logging
            logging.info(json.dumps(data, indent=2))
            choices = data.get("choices", [])
            if choices:
                if message := choices[0].get("message"):
                    return Message.from_dict(message)
                raise ValueError("No Message has been present in the response")
            raise ValueError("No Choice has been present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

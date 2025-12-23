from io import BytesIO
from typing import Any, Dict, Optional

import httpx


class DialBucketClient:
    """
    Async client for interacting with DIAL bucket storage service.
    
    This client provides methods to upload and download files from a DIAL bucket.
    It should be used as an async context manager.
    
    Attributes:
        api_key (str): API key for authentication
        base_url (str): Base URL of the DIAL service
        _bucket_id (Optional[str]): Cached bucket ID
        _client (Optional[httpx.AsyncClient]): HTTP client instance
    """
    def __init__(self, api_key: str , base_url: str):
        """
        Initialize the DIAL bucket client.
        
        Args:
            api_key (str): API key for authentication
            base_url (str): Base URL of the DIAL service
        """
        self.api_key = api_key
        self.base_url = base_url
        self._bucket_id: Optional[str] = None
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """
        Async context manager entry point.
        
        Creates and returns an HTTP client with appropriate headers.
        
        Returns:
            DialBucketClient: Self instance for use in context manager
        """
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={'Api-Key': self.api_key},
        )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Async context manager exit point.
        
        Closes the HTTP client if it exists.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_value: Exception value if an exception occurred
            traceback: Traceback if an exception occurred
        """
        if self._client:
            await self._client.aclose()


    async def _get_bucket(self) -> str:
        """
        Get the bucket ID from the DIAL service.
        
        Fetches the bucket ID from the service if not already cached.
        
        Returns:
            str: The bucket ID
            
        Raises:
            RuntimeError: If the client is not initialized
            ValueError: If no appdata or bucket is found in response
        """
        if not self._bucket_id:
            if self._client is None:
                raise RuntimeError("Client not initialized. Use as context manager.")
            response = await self._client.get('/v1/bucket')
            response.raise_for_status()

            bucket_json = response.json()
            if "appdata" in bucket_json:
                self._bucket_id = bucket_json["appdata"]
            elif "bucket" in bucket_json:
                self._bucket_id = bucket_json["bucket"]
            else:
                raise ValueError("No appdata or bucket found")

        if self._bucket_id is None:
            raise RuntimeError("Bucket ID could not be determined")
        return self._bucket_id


    async def put_file(
        self, name: str, mime_type: str, content: BytesIO
    ) -> Dict[str, Any]:
        """
        Upload a file to the DIAL bucket.
        
        Args:
            name (str): Name of the file
            mime_type (str): MIME type of the file
            content (BytesIO): File content as BytesIO object
            
        Returns:
            Dict[str, Any]: Response from the upload operation
            
        Raises:
            RuntimeError: If the client is not initialized
        """
        path = await self._get_bucket()

        if self._client is None:
            raise RuntimeError("Client not initialized. Use as context manager.")
        response = await self._client.put(
            f"/v1/files/{path}/{name}",
            files={name: (name, content, mime_type)},
        )
        response.raise_for_status()
        return response.json()

    async def get_file(self, url: str) -> bytes:
        """
        Download a file from the DIAL service.
        
        Args:
            url (str): URL of the file to download
            
        Returns:
            bytes: Content of the downloaded file
            
        Raises:
            RuntimeError: If the client is not initialized
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use as context manager.")
        response = await self._client.get(f"/v1/{url}")
        response.raise_for_status()
        return response.content


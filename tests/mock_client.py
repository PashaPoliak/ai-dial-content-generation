from unittest.mock import MagicMock, AsyncMock

class MockAttachment:
    def __init__(self, url: str):
        self.url = url


class MockCustomContent:
    def __init__(self, attachments):
        self.attachments = attachments


class MockResult:
    def __init__(self, image_url: str):
        self.custom_content = MockCustomContent(
            attachments=[MockAttachment(image_url)]
        )


class MockDialModelClient:
    def __init__(self, endpoint=None, deployment_name=None, api_key=None, *args, **kwargs):

        if endpoint and deployment_name:
            self._endpoint = endpoint.format(model=deployment_name)
        else:
            self._endpoint = endpoint
        self._api_key = api_key

        self.get_completion = MagicMock()
        self._make_request = MagicMock()


class MockDialBucketClient:
    def __init__(self, *args, **kwargs):

        self.get_file = AsyncMock()
        self.put_file = AsyncMock()

        self._client = AsyncMock()
        self._bucket_id = "mock_bucket_id"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _get_bucket(self):
        return self._bucket_id
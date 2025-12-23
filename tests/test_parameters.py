from unittest.mock import Mock, patch

from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role
from tests.test_data import CHOICES_DATA, TEST_API_KEY, TEST_ENDPOINT, TEST_MODEL_NAME

TEST_MESSAGE_CONTENT = "Test message"

TEMPERATURE_VALUE = 0.7
MAX_TOKENS_VALUE = 100
FREQUENCY_PENALTY_VALUE = 0.5
PRESENCE_PENALTY_VALUE = 0.5
SEED_VALUE = 42
N_VALUE = 3
INVALID_TEMPERATURE = 2.0
INVALID_MAX_TOKENS = 999999
INVALID_FREQUENCY_PENALTY = 3.0
BOUNDARY_TEMPERATURE = 0.0
BOUNDARY_MAX_TOKENS = 1
BOUNDARY_FREQUENCY_PENALTY = -2.0
BOUNDARY_PRESENCE_PENALTY = -2.0


class TestParameterSpecific:
    

    def test_temperature_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA

            mock_post.return_value = mock_response
            
            temperature_value = TEMPERATURE_VALUE
            client.get_completion([message], custom_fields={"temperature": temperature_value})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["temperature"] == temperature_value

    def test_max_tokens_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA

            mock_post.return_value = mock_response
            
            max_tokens_value = MAX_TOKENS_VALUE
            client.get_completion([message], custom_fields={"max_tokens": max_tokens_value})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["max_tokens"] == max_tokens_value

    def test_frequency_penalty_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA

            mock_post.return_value = mock_response
            
            frequency_penalty_value = FREQUENCY_PENALTY_VALUE
            client.get_completion([message], custom_fields={"frequency_penalty": frequency_penalty_value})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["frequency_penalty"] == frequency_penalty_value

    def test_presence_penalty_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            
            presence_penalty_value = PRESENCE_PENALTY_VALUE
            client.get_completion([message], custom_fields={"presence_penalty": presence_penalty_value})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["presence_penalty"] == presence_penalty_value

    def test_seed_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            
            seed_value = SEED_VALUE
            client.get_completion([message], custom_fields={"seed": seed_value})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["seed"] == seed_value

    def test_multiple_parameters(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            
            custom_fields = {
                "temperature": TEMPERATURE_VALUE,
                "max_tokens": MAX_TOKENS_VALUE,
                "frequency_penalty": FREQUENCY_PENALTY_VALUE,
                "presence_penalty": PRESENCE_PENALTY_VALUE,
                "seed": SEED_VALUE
            }
            
            client.get_completion([message], custom_fields=custom_fields)
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            config = request_data["custom_fields"]["configuration"]
            
            assert config["temperature"] == TEMPERATURE_VALUE
            assert config["max_tokens"] == MAX_TOKENS_VALUE
            assert config["frequency_penalty"] == FREQUENCY_PENALTY_VALUE
            assert config["presence_penalty"] == PRESENCE_PENALTY_VALUE
            assert config["seed"] == SEED_VALUE

    def test_n_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            
            n_value = N_VALUE
            client.get_completion([message], custom_fields={"n": n_value})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["n"] == n_value

    def test_stop_sequences_parameter(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            
            stop_sequences = ["\n", "STOP", "END"]
            client.get_completion([message], custom_fields={"stop": stop_sequences})
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            assert request_data["custom_fields"]["configuration"]["stop"] == stop_sequences

    def test_parameter_boundary_values(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            

            boundary_params = {
                "temperature": BOUNDARY_TEMPERATURE,
                "max_tokens": BOUNDARY_MAX_TOKENS,
                "frequency_penalty": BOUNDARY_FREQUENCY_PENALTY,
                "presence_penalty": BOUNDARY_PRESENCE_PENALTY,
            }
            
            client.get_completion([message], custom_fields=boundary_params)
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            config = request_data["custom_fields"]["configuration"]
            
            assert config["temperature"] == BOUNDARY_TEMPERATURE
            assert config["max_tokens"] == BOUNDARY_MAX_TOKENS
            assert config["frequency_penalty"] == BOUNDARY_FREQUENCY_PENALTY
            assert config["presence_penalty"] == BOUNDARY_PRESENCE_PENALTY

    def test_parameter_validation_not_performed_by_client(self):
        
        client = DialModelClient(
            endpoint=TEST_ENDPOINT,
            deployment_name=TEST_MODEL_NAME,
            api_key=TEST_API_KEY
        )
        
        message = Message(
            role=Role.USER,
            content=TEST_MESSAGE_CONTENT
        )
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = CHOICES_DATA
            mock_post.return_value = mock_response
            

            invalid_params = {
                "temperature": INVALID_TEMPERATURE,
                "max_tokens": INVALID_MAX_TOKENS,
                "frequency_penalty": INVALID_FREQUENCY_PENALTY,
            }
            
            client.get_completion([message], custom_fields=invalid_params)
            

            args, kwargs = mock_post.call_args
            request_data = kwargs['json']
            
            assert "custom_fields" in request_data
            assert "configuration" in request_data["custom_fields"]
            config = request_data["custom_fields"]["configuration"]
            
            assert config["temperature"] == INVALID_TEMPERATURE
            assert config["max_tokens"] == INVALID_MAX_TOKENS
            assert config["frequency_penalty"] == INVALID_FREQUENCY_PENALTY
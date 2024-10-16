import pytest
from unittest.mock import Mock

@pytest.fixture
def api_mock_instance_valid() -> Mock:
    # A mock for the API which returns something succesfull and valid
    mock_response = Mock()
    mock_response.json.return_value = [{'id':1}]
    mock_response.status_code = 200
    # Highjacking a varibale in the class 
    # to easily have access to the expected result
    mock_response.string_converted_expected_result = "{'id': 1}"
    return mock_response


import json
import pytest
from unittest.mock import patch, Mock
from api_interactor.fetcher import fetcher
import requests

pytestmark = pytest.mark.fetcher_test

@pytest.fixture
def fetcher_instance() -> fetcher:
    return fetcher()

@patch('requests.get')
class TestFetchAll:
    
    @pytest.mark.parametrize('routes', ['users/1', '/albums/1/photos', 'photos/2'])
    def test_routes_construction(
        self, mock_get: Mock,
        fetcher_instance: fetcher,
        routes: list[str]) -> None:
        _ = fetcher_instance.fetch_all_of_topic(routes)
        mock_get.assert_called_with(f'https://jsonplaceholder.typicode.com/{routes}')
    

    @pytest.mark.parametrize('mock_list_from_get_call, status_code, expected_output',
                             [([{'id':1}], 200, "{'id': 1}"),
                              ([], 404, "The selected ID is invalid")])
    def test_expected_output(
        self, mock_get: Mock,
        fetcher_instance: fetcher,
        mock_list_from_get_call: list[dict[str, int | str]],
        status_code: int,
        expected_output: str) -> None:
        mock_response = Mock()
        response_json_dict = mock_list_from_get_call
        mock_response.json.return_value = response_json_dict
        mock_response.status_code = status_code
        mock_get.return_value = mock_response
        string = fetcher_instance.fetch_all_of_topic('users/1')
        assert string == expected_output


@pytest.mark.parametrize('json_list, expected_string_output',
                        [([{'id':1}], "{'id': 1}"),
                         ([{'name': 'bob'}], "{'name': 'bob'}"),
                         ([{'name': 'bob'}, {'id': 1}], "{'name': 'bob'}\n{'id': 1}"),
                         ([{'id': 1}, {'name': 'bob'}], "{'id': 1}\n{'name': 'bob'}"),
                         ([], '')])
class TestJsonListToString:
    @pytest.fixture
    def fetcher_instance(json_list) -> fetcher:
        return fetcher()

    def test_istance_of_string(
        self,
        fetcher_instance: fetcher,
        json_list: list[dict[str, int | str]],
        expected_string_output: str)-> None:
        # Test that a string is returned
        assert isinstance(fetcher_instance.convert_list_of_dicts_to_string(json_list), str)
        
    def test_number_of_new_lines(
        self,
        fetcher_instance: fetcher,
        json_list: list[dict[str, int | str]],
        expected_string_output: str)-> None:
        # Test that the string divided by the right amount of new lines
        assert len(json_list) - 1 == fetcher_instance.convert_list_of_dicts_to_string(json_list).count('\n') or\
            len(json_list) == 0 and fetcher_instance.convert_list_of_dicts_to_string(json_list).count('\n') == 0
    
    def test_expected_output(
        self,
        fetcher_instance: fetcher,
        json_list: list[dict[str, int | str]],
        expected_string_output: str)-> None:
        # Test that the string appears as expected
        assert fetcher_instance.convert_list_of_dicts_to_string(json_list) == expected_string_output



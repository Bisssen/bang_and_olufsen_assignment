
import json
import pytest
from unittest.mock import patch, Mock
from api_interactor.fetcher import fetcher
import requests

pytestmark = pytest.mark.fetcher_test

@pytest.fixture
def fetcher_instance() -> fetcher:
    return fetcher()


def combine_parametrize_list(list_1: list[any], list_2: list[any]) -> list[any]:
    if len(list_1[0]) == 1:
        combined_list = [tuple([tup]+[value]) for tup, value in zip(list_1, list_2)]
    else:
        combined_list = [list(tup)+[value] for tup, value in zip(list_1, list_2)]
    
    return combined_list

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
    def test_return_string(
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


class TestFetcher:
    # json_object_to_string_pairs = [([{'id':1}], "{'id': 1}"),
    #                                ([{'name': 'bob'}], "{'name': 'bob'}"),
    #                                ([{'name': 'bob'}, {'id': 1}], "{'name': 'bob'}\n{'id': 1}"),
    #                                ([{'id': 1}, {'name': 'bob'}], "{'id': 1}\n{'name': 'bob'}"),
    #                                ([], '')]
    
    mock_json_objects = [([{'id':1}]),
                         ([{'name': 'bob'}]),
                         ([{'name': 'bob'}, {'id': 1}]),
                         ([{'id': 1}, {'name': 'bob'}]),
                         ([])]

    string_outputs = [("{'id': 1}"),
                      ("{'name': 'bob'}"),
                      ("{'name': 'bob'}\n{'id': 1}"),
                      ("{'id': 1}\n{'name': 'bob'}"),
                      ('')]

    json_object_to_string_pairs = combine_parametrize_list(mock_json_objects, string_outputs)
    tmp = combine_parametrize_list(mock_json_objects, string_outputs)


    @pytest.mark.parametrize('_input, _output', json_object_to_string_pairs)
    def test_list_of_dict_string_convertion(
        self,
        fetcher_instance: fetcher,
        _input: list[dict[str, int | str]],
        _output: str)-> None:
        # Test that a string is returned
        assert isinstance(fetcher_instance.convert_list_of_dicts_to_string(_input), str)
        # # Test that the string divided by the right amount of new lines
        assert len(_input) - 1 == fetcher_instance.convert_list_of_dicts_to_string(_input).count('\n') or\
            len(_input) == 0 and fetcher_instance.convert_list_of_dicts_to_string(_input).count('\n') == 0
        # Test that the string appears as expected
        assert fetcher_instance.convert_list_of_dicts_to_string(_input) == _output



import pytest
from unittest.mock import patch, Mock
from api_interactor.fetcher import fetcher

pytestmark = pytest.mark.fetcher

@pytest.fixture
def fetcher_instance() -> fetcher:
    return fetcher()


@patch('requests.get')
class TestFetchAll:
    get_test_parameters = [([{'id':1}], 200, "{'id': 1}"),
                           ([], 404, "The selected ID is invalid")]


    @pytest.mark.parametrize('routes', ['users/1', '/albums/1/photos', 'photos/2'])
    def test_routes_construction(
            self,
            mock_get: Mock,
            fetcher_instance: fetcher,
            api_mock_instance_valid: Mock,
            routes: str) -> None:
        # Use the predifined mock
        mock_response = api_mock_instance_valid
        mock_get.return_value = mock_response
        _ = fetcher_instance.fetch_all_of_topic(routes)
        mock_get.assert_called_with(f'https://jsonplaceholder.typicode.com/{routes}')
    

    
    @pytest.mark.parametrize('mock_list_from_get_call, status_code, expected_output',
                             get_test_parameters)
    def test_expected_output(
            self,
            mock_get: Mock,
            fetcher_instance: fetcher,
            api_mock_instance_valid: Mock,
            mock_list_from_get_call: list[dict[str, int | str]],
            status_code: int,
            expected_output: str) -> None:
        # Use the predifined mock, but a new instance would result in the same
        mock_response = api_mock_instance_valid
        # Load the testing values
        mock_response.json.return_value = mock_list_from_get_call
        mock_response.status_code = status_code
        mock_get.return_value = mock_response
        string = fetcher_instance.fetch_all_of_topic('users/1')
        assert string == expected_output
    
    @pytest.mark.parametrize('mock_list_from_get_call, status_code, expected_output',
                            get_test_parameters)
    def test_print_output(
            self,
            mock_get: Mock,
            fetcher_instance: fetcher,
            api_mock_instance_valid: Mock,
            capsys: pytest.CaptureFixture[str],
            mock_list_from_get_call: list[dict[str, int | str]],
            status_code: int,
            expected_output: str) -> None:
        # Use the predifined mock, but a new instance would result in the same
        mock_response = api_mock_instance_valid
        # Load the testing values
        mock_response.json.return_value = mock_list_from_get_call
        mock_response.status_code = status_code
        mock_get.return_value = mock_response
        fetcher_instance.fetch_and_print_all_of_topic('users/1')
        # Capture the print output
        captured_output = capsys.readouterr()
        # Get the only the string part
        string = captured_output.out
        # The funcion is supposed to add a leading line change
        # and the print function adds a lagging line change
        # So add it to the output
        expected_output = '\n' + expected_output + '\n'
        assert string == expected_output


@pytest.mark.parametrize('json_list, expected_string_output',
                        [([{'id':1}], "{'id': 1}"),
                         ([{'name': 'bob'}], "{'name': 'bob'}"),
                         ([{'name': 'bob'}, {'id': 1}], "{'name': 'bob'}\n{'id': 1}"),
                         ([{'id': 1}, {'name': 'bob'}], "{'id': 1}\n{'name': 'bob'}"),
                         ([], '')])
def test_expected_output_of_convert_list_of_dicts_to_string(
        fetcher_instance: fetcher,
        json_list: list[dict[str, int | str]],
        expected_string_output: str)-> None:
    # Test that a string is returned
    assert isinstance(fetcher_instance.convert_list_of_dicts_to_string(json_list), str)
    # Test that the string divided by the right amount of new lines
    assert len(json_list) - 1 == fetcher_instance.convert_list_of_dicts_to_string(json_list).count('\n') or\
        len(json_list) == 0 and fetcher_instance.convert_list_of_dicts_to_string(json_list).count('\n') == 0
    # Test that the output matches the expected output
    assert fetcher_instance.convert_list_of_dicts_to_string(json_list) == expected_string_output
    




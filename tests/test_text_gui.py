import pytest
from unittest.mock import patch, Mock
from api_interactor.text_gui import text_gui


pytestmark = pytest.mark.text_gui

@pytest.fixture
def text_gui_instance() -> text_gui:
    return text_gui()

def test_route_map(
        text_gui_instance: text_gui,
        capsys: pytest.CaptureFixture[str]) -> None:
    expected_output = 'users - > albums - > photos\n'\
                       '      | > todos\n'\
                       '      | > posts  - > comments' + '\n'  # Additional \n added from the print function
    text_gui_instance.print_route_map()
    # Read the printed output and get the string
    captured_output = capsys.readouterr()
    string = captured_output.out
    assert string == expected_output
    
def test_activate_exit(text_gui_instance: text_gui) -> None:
    text_gui_instance.activate_exit()
    assert text_gui_instance.exit

def test_next_state(text_gui_instance: text_gui) -> None:
    test_state = 'test_state'
    text_gui_instance.set_next_state(test_state)
    assert text_gui_instance.state == test_state

@pytest.mark.parametrize('user_input', 
                        ['1', 'q'])
@pytest.mark.parametrize('function_input', 
                        ['user', 'album', 'photo', 'post', 'comment'])
def test_inspect_specific(
        text_gui_instance: text_gui,
        user_input: str,
        function_input: str,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]) -> None:
    # Temporary change the input function to return users/1
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    # Set the state of the gui to a known dummy variable
    pre_state = 'test'
    text_gui_instance.state = pre_state
    text_gui_instance.inspect_specific(function_input)
    captured_output = capsys.readouterr()
    string = captured_output.out
    if user_input.isdigit():
        assert text_gui_instance.state == function_input
    else:
        assert text_gui_instance.state == pre_state
        assert string == f'\nThe {function_input} ID must be an integer\n'    


# def inspect_specific(self, id_type: str) -> None:
#     '''
#     This function asks the user what ID they want to inspect
#     goes to the next state based on the provided id_type
#     '''
#     user_input = input('\n'
#                         f'Type the ID of the desired {id_type}'
#                         'or q to go back:\n')
#     if user_input.isdigit():
#         # Set the current selected id
#         self.selected_ids[id_type] = user_input
#         # Set the next state based on the provided id_type
#         self.set_next_state(id_type)
#     elif not user_input == 'q':
#         self.inspect_specific(id_type)
#         print(f'The {id_type} ID must be an integer')

@patch('requests.get')
class TestApiRelatedTextGuiFunctions:

    def test_specific_path_request(
            self,
            mock_get: Mock,
            text_gui_instance: text_gui,
            api_mock_instance_valid: Mock,
            monkeypatch: pytest.MonkeyPatch,
            capsys: pytest.CaptureFixture[str]) -> None:
        # Temporary change the input function to return users/1
        monkeypatch.setattr('builtins.input', lambda _: 'users/1')
        # Use the predifined mock
        mock_response = api_mock_instance_valid
        mock_get.return_value = mock_response
        text_gui_instance.inspect_specific_path()
        captured_output = capsys.readouterr()
        string = captured_output.out[1:-1]  # Remove leading and lagging line change
        assert string == api_mock_instance_valid.string_converted_expected_result



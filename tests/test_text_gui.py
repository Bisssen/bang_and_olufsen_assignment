import pytest
from unittest.mock import patch, Mock
from api_interactor.text_gui import text_gui, TOP, USER, ALBUM, POST, PHOTO, COMMENT

# Mark
pytestmark = pytest.mark.text_gui

# Class fixture
@pytest.fixture
def text_gui_instance() -> text_gui:
    return text_gui()

text_gui_path = 'api_interactor.text_gui.text_gui'
fetcher_path = 'api_interactor.fetcher.fetcher'

# Patches
set_next_state_patch = patch(f'{text_gui_path}.set_next_state')
fetch_and_print_all_patch = patch(f'{fetcher_path}.fetch_and_print_all_of_topic')
inspect_specific_patch = patch(f'{text_gui_path}.inspect_specific')
set_next_state_patch = patch(f'{text_gui_path}.set_next_state')

# Commenæy used testing parameterizations
list_of_complex_states = [TOP, USER, ALBUM, POST]



def get_and_run_function(
        text_gui_instance: text_gui,
        function_name: str) -> None:
    # Gets and runs a state function based on the state name 
    # Get the selected function
    func = getattr(text_gui_instance, function_name + '_state')
    # Run it with the fixtures text gui instance
    func()

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

@fetch_and_print_all_patch
def test_specific_path_request(
        fetch_and_print_all_of_topic_mock: Mock,
        text_gui_instance: text_gui,
        monkeypatch: pytest.MonkeyPatch) -> None:
    # Temporary change the input function to return users/1
    monkeypatch.setattr('builtins.input', lambda _: 'users/1')

    text_gui_instance.inspect_specific_path()
    fetch_and_print_all_of_topic_mock.assert_called_with('users/1')

@pytest.mark.parametrize('user_input', 
                        ['1', 'q'])
@pytest.mark.parametrize('function_input', 
                        [USER, ALBUM, PHOTO, POST, COMMENT])
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

@pytest.mark.parametrize('function_names', list_of_complex_states)
# All states react the same to q and default
def test_exit_paths(
        text_gui_instance: text_gui,
        function_names: str,
        monkeypatch: pytest.MonkeyPatch) -> None:
    # Temporary change the input function to return test
    monkeypatch.setattr('builtins.input', lambda _: 'q')
    get_and_run_function(text_gui_instance, function_names)

    assert text_gui_instance.exit

@pytest.mark.parametrize('function_names', list_of_complex_states)
# All states react the same to q and default
def test_invalid_options_path(
        text_gui_instance: text_gui,
        function_names: str,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]) -> None:
    # Temporary change the input function to return test
    monkeypatch.setattr('builtins.input', lambda _: 'test')
    get_and_run_function(text_gui_instance, function_names)

    # Capture the print output
    captured_output = capsys.readouterr()
    string = captured_output.out
    assert string == '\nInvalid option\n'

@pytest.mark.parametrize('user_input', ['1', '2', '3', '5'])
@pytest.mark.parametrize('function_name', list_of_complex_states)
@fetch_and_print_all_patch
def test_print_all_of_topic_in_states(
        fetch_and_print_all_of_topic_mock: Mock,
        user_input: str,
        function_name: str,
        text_gui_instance: text_gui,
        monkeypatch: pytest.MonkeyPatch) -> None:
    valid_tries = {}
    valid_tries[TOP] = ['1']
    valid_tries[USER] = ['1', '2', '3', '5']
    valid_tries[ALBUM] = ['1', '2']
    valid_tries[POST] = ['1', '2']

    # Only test the paths that should result in an API call
    if user_input not in valid_tries[function_name]:
        return

    # Temporary change the input function
    monkeypatch.setattr('builtins.input', lambda _: user_input)

    # Populate the selected ids dict
    text_gui_instance.selected_ids[function_name] = '1'

    # Run the state function
    get_and_run_function(text_gui_instance, function_name)

    fetch_and_print_all_of_topic_mock.assert_called_once()


@pytest.mark.parametrize('user_input', ['2', '3', '4', '6'])
@pytest.mark.parametrize('function_name', list_of_complex_states)
@inspect_specific_patch
def test_inspect_specific_path(
        inspect_specific_mock: Mock,
        user_input: str,
        function_name: str,
        text_gui_instance: text_gui,
        monkeypatch: pytest.MonkeyPatch) -> None:
    valid_tries = {}
    valid_tries[TOP] = ['2']
    valid_tries[USER] = ['4', '6']
    valid_tries[ALBUM] = ['3']
    valid_tries[POST] = ['3']

    # Only test the paths that should result in an API call
    if user_input not in valid_tries[function_name]:
        return

    # Temporary change the input function
    monkeypatch.setattr('builtins.input', lambda _: user_input)

    # Run the state function
    get_and_run_function(text_gui_instance, function_name)

    # Ensure the path calls inspect_specific
    inspect_specific_mock.assert_called_once()

@pytest.mark.parametrize('function_name, expected_state_argument', 
                        [(USER, TOP), (POST, USER), (ALBUM, USER)])
@set_next_state_patch
def test_set_state_path(
    set_next_state_mock: Mock,
    function_name: str,
    expected_state_argument : str,
    text_gui_instance: text_gui,
    monkeypatch: pytest.MonkeyPatch) -> None:
    # Temporary change the input function
    monkeypatch.setattr('builtins.input', lambda _: '9')

    # Run the state function
    get_and_run_function(text_gui_instance, function_name)

    # Ensure the path calls inspect_specific
    set_next_state_mock.assert_called_with(expected_state_argument)

@pytest.mark.parametrize('function_name, expected_state_argument', 
                        [(PHOTO, ALBUM), (COMMENT, POST)])
@fetch_and_print_all_patch
@set_next_state_patch
def test_function_calls_in_end_states(
    set_next_state_mock: Mock,
    fetch_and_print_all_of_topic_mock: Mock,
    function_name: str,
    expected_state_argument : str,
    text_gui_instance: text_gui) -> None:
    
    # Populate the selected ids dict
    text_gui_instance.selected_ids[function_name] = '1'

    # Run the state function
    get_and_run_function(text_gui_instance, function_name)

    # Ensure the paths sets the correct next state
    set_next_state_mock.assert_called_with(expected_state_argument)
    # Ensure the end paths correctly calls fetch_and_print_all_of_topic
    fetch_and_print_all_of_topic_mock.assert_called_with(f'/{function_name}s/1')

@pytest.mark.parametrize('function_name, user_input', 
                        [('inspect_specific_path', '3'),
                         ('print_route_map', '4'),
                         ('activate_exit', '9')])
def test_unique_top_function_calls(
    monkeypatch: pytest.MonkeyPatch,
    function_name: str,
    user_input: str,
    text_gui_instance: text_gui) -> None:

    @patch(f'{text_gui_path}.{function_name}')
    def test_inspect_activate_exit_call(
        function_mock: Mock) -> None:
        text_gui_instance.top_state()

        # Ensure the expected function is called
        function_mock.assert_called_once()

    # Temporary change the input function
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    
    test_inspect_activate_exit_call()
import requests


class fetcher():
    def __init__(self) -> None:
        # Base URL
        self.root_url = 'https://jsonplaceholder.typicode.com/'

    def fetch_and_print_all_of_topic(self, topic: str) -> None:
        
        json_string = self.fetch_all_of_topic(topic)
        # Make a line change to make the reponse easier to read
        print(f'\n{json_string}')

    def fetch_all_of_topic(self, topic: str) -> str:
        response = requests.get(self.root_url + topic)
        # This is not quite correct but the main error will be 404
        # and I won't handle all the errors in the scope of this project
        if not response.status_code == 200:
            return 'The selected ID is invalid'
        json_list = response.json()
        # If there are multiple elements, then print them with line changes
        if isinstance(json_list, list):
            return self.convert_list_of_dicts_to_string(json_list)
        else:
            return str(json_list)

    def convert_list_of_dicts_to_string(self, json_list: list[dict[str, int | str]]) -> str:
        final_string = ''
        for json_dict in json_list:
            final_string += str(json_dict) + '\n'

        final_string = final_string[:-1]

        return final_string

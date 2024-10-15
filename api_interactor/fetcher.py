import requests as rq

class fetcher():
    def __init__(self) -> None:
        # Base URL
        self.root_url = 'https://jsonplaceholder.typicode.com/'
    
    def fetch_all_of_topic(self, topic: str) -> None:
        response = rq.get(self.root_url + topic)
        # There is way more response codes but I won't handle them in
        # the scope of this project
        if response.status_code == 404:
            print('The selected ID is invalid')
            return
        json_list = response.json()
        # If there are multiple elements, then print them with line changes
        if isinstance(json_list, list):
            print(convert_list_of_dicts_to_string(json_list))
        else:
            print(json_list)

def convert_list_of_dicts_to_string(json_list: list[dict]) -> str:
    final_string = ''
    for json_dict in json_list:
        final_string += str(json_dict) + '\n'
    
    final_string = final_string[:-1]

    return final_string
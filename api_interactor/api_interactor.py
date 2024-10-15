import requests as rq
import time


class api_interactor():
    def __init__(self, desired_topics: list[str] = []) -> None:
        '''
        1. iCreate a `Python` application (with v3.10 or hgher) using Object Oriented Programming principles that makes use of type hints throughout the code. The application will interact with the JSONplaceholder API (https://jsonplaceholder.typicode.com/).
        The application should be able to fetch and print data from the JSONplaceholder API. Specifically, it should fetch data from at least two different endpoints, such as `/posts` and `/users`.
        '''
        # Base URL
        self.root_url = 'https://jsonplaceholder.typicode.com/'

        # A list of the topics we are interested in
        self.desired_topics = desired_topics

        # A dict of the desired topics and their max id
        self.request_topics: dict[str, int] = {}

    def get_setup_data(self) -> None:
        '''
        Looks up the possible ids of post and users.
        This data is used to populate options and ensure no requests are made to wrong places
        '''
        # for topic in self.desired_topics:
        #     response = rq.get(self.root_url + topic)
        #     # TODO do something with status code
        #     # If the topic is invalid this should throw an error or something
            
        #     response_jsons = response.json()
        #     valid_ids = []
        #     # Look through all the options and capture all valid ids
        #     for repsonse_json in response_jsons:
        #         valid_ids.append(repsonse_json['id'])
        #     # Save the valid ids
        #     self.request_topics[topic] = valid_ids
        
        response = rq.get(self.root_url + 'users/2/albums')
        print(response.json())
        
    def loop(self) -> None:
        # TODO make welcome message that lists number of options
        while True:
            user_input = input('1. Fetch all users\n'
                               '2. Fetch specific user\n'
                               '9. Exit\n')
            match user_input:
                case '1':
                    print(self.convert_list_of_dicts_to_string(self.fetch_all_of_topic('users')))
                case '9':
                    break
                case default:
                    print('Invalid option')


    
    def fetch_all_of_topic(self, topic: str) -> list[dict]:
        response = rq.get(self.root_url + topic)
        # TODO do something with status code
        # If the topic is invalid this should throw an error or something
        return response.json()

    def convert_list_of_dicts_to_string(self, json_list: list[dict]) -> str:
        final_string = ''
        for json_dict in json_list:
            final_string += str(json_dict) + '\n'
        
        final_string = final_string[:-1]

        return final_string

    def test(self) -> None:    
        response = rq.get(self.root_url + 'posts')
        print(response.json())
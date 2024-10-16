from .fetcher import fetcher
# STATES
TOP = 'top'
USER = 'user'
ALBUM = 'album'
PHOTO = 'photo'
POST = 'post'
COMMENT = 'comment'


class text_gui():
    def __init__(self) -> None:
        self.fetcher: fetcher = fetcher()

        # Boolean that makes the gui exit
        self.exit = False
        # The states must be named something_state
        # The self.inspect_specific function only works if
        # the states are named after the topic they inspect
        # e.g. user_inspect_state
        self.state: str = TOP

        # Dict that keeps track of which ids the user have selected
        self.selected_ids: dict[str, str] = {}

    def loop(self) -> None:
        first = True

        while not self.exit:
            # Ensure the state exists
            if not hasattr(self, self.state + '_state'):
                raise ValueError(
                    f'State used that does not exist: {self.state}.'
                    'All states must be named: something_state'
                    )

            # Make a line skip except for when the program have just started
            if first:
                first = False
            else:
                print('')

            # Call the current state
            getattr(self, self.state + '_state')()

    def top_state(self) -> None:
        user_input = input('1. Display the data of all the users\n'
                           '2. Inspect a specific user\n'
                           '3. Display data from specific path\n'
                           '4. Show route map\n'
                           '9 / q. Exit\n')
        match user_input:
            case '1':
                self.fetcher.fetch_and_print_all_of_topic('users')
            case '2':
                self.inspect_specific('user')
            case '3':
                self.inspect_specific_path()
            case '4':
                self.print_route_map()
            case '9' | 'q':
                self.activate_exit()
            case default:
                print('Invalid option\n')

    def user_state(self) -> None:
        user_input = input('1. Display the data of the user\n'
                           '2. Display the data of the user\'s todos\n'
                           '3. Display the data of the user\'s albums\n'
                           '4. Inspect a specific album\n'
                           '5. Display the data of the user\'s posts\n'
                           '6. Inspect a specific post\n'
                           '9. Return\n'
                           'q. Exit\n ')
        match user_input:
            case '1':
                self.fetcher.fetch_and_print_all_of_topic(
                    'users/' + self.selected_ids['user']
                    )
            case '2':
                self.fetcher.fetch_and_print_all_of_topic(
                    'users/' + self.selected_ids['user'] + '/todos'
                    )
            case '3':
                self.fetcher.fetch_and_print_all_of_topic(
                    'users/' + self.selected_ids['user'] + '/albums'
                    )
            case '4':
                self.inspect_specific('album')
            case '5':
                self.fetcher.fetch_and_print_all_of_topic(
                    'users/' + self.selected_ids['user'] + '/posts'
                    )
            case '6':
                self.inspect_specific('post')
            case '9':
                self.set_next_state(TOP)
            case 'q':
                self.activate_exit()
            case default:
                print('Invalid option\n')

    def album_state(self) -> None:
        user_input = input('1. Display the data of the album\n'
                           '2. Display the data of the album\'s photos\n'
                           '3. Inspect a specific photo\n'
                           '9. Return\n'
                           'q. Exit\n')
        match user_input:
            case '1':
                self.fetcher.fetch_and_print_all_of_topic(
                    '/albums/' + self.selected_ids['album']
                    )
            case '1':
                self.fetcher.fetch_and_print_all_of_topic(
                    '/albums/' + self.selected_ids['album'] + '/photos'
                    )
            case '3':
                self.inspect_specific('photo')
            case '9':
                self.set_next_state(USER)
            case 'q':
                self.activate_exit()
            case default:
                print('\nInvalid option')

    def photo_state(self) -> None:
        self.fetcher.fetch_and_print_all_of_topic('/photos/' +
                                                  self.selected_ids['photo'])
        self.set_next_state(ALBUM)

    def post_state(self) -> None:
        user_input = input('1. Display the data of the post\n'
                           '2. Display the data of the post\'s comments\n'
                           '3. Inspect a specific comment\n'
                           '9. Return\n'
                           'q. Exit\n')
        match user_input:
            case '1':
                self.fetcher.fetch_and_print_all_of_topic(
                    '/posts/' + self.selected_ids['post']
                    )
            case '2':
                self.fetcher.fetch_and_print_all_of_topic(
                    '/posts/' + self.selected_ids['post'] + '/comments'
                    )
            case '3':
                self.inspect_specific('comment')
            case '9':
                self.set_next_state(USER)
            case 'q':
                self.activate_exit()
            case default:
                print('\nInvalid option')

    def comment_state(self) -> None:
        self.fetcher.fetch_and_print_all_of_topic('/comments/' +
                                                  self.selected_ids['comment'])
        self.set_next_state(POST)

    def inspect_specific(self, id_type: str) -> None:
        '''
        This function asks the user what ID they want to inspect
        goes to the next state based on the provided id_type
        '''
        user_input = input('\n'
                           f'Type the ID of the desired {id_type}'
                           'or q to go back:\n')
        if user_input.isdigit():
            # Set the current selected id
            self.selected_ids[id_type] = user_input
            # Set the next state based on the provided id_type
            self.set_next_state(id_type)
        elif not user_input == 'q':
            self.inspect_specific(id_type)
            print(f'The {id_type} ID must be an integer')

    def inspect_specific_path(self) -> None:
        user_input = input('\n'
                           f'Type the path of the desired topic:\n'
                           f'{self.fetcher.root_url}')
        self.fetcher.fetch_and_print_all_of_topic(user_input)

    def print_route_map(self) -> None:
        print('users - > albums - > photos\n'
              '      | > todos\n'
              '      | > posts  - > comments')

    def activate_exit(self) -> None:
        self.exit = True

    def set_next_state(self, next_state: str) -> None:
        self.state = next_state

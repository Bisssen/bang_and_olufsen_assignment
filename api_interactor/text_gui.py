from .fetcher import fetcher

class text_gui():
    def __init__(self, fetch: fetcher) -> None:
        self.fetcher = fetch

        self.exit = False
    
    def loop(self) -> None:
        while True:
            user_input = input('1. Display the data of all the users\n'
                               '2. Inspect a specific user\n'
                               '3. Display data from specific path\n'
                               '4. Show route map\n'
                               '9 / q. Exit\n')
            match user_input:
                case '1':
                    self.fetcher.fetch_all_of_topic('users')
                case '2':
                    self.inspect_specific('user')
                case '3':
                    pass
                case '4':
                    print('users - > albums - > photos\n'
                          '      | > todos\n'
                          '      | > posts  - > comments\n')
                case '9' | 'q':
                    break
                case default:
                    print('Invalid option')
            
            if self.exit:
                return

    def inspect_specific(self, id_type: str):
        '''
        This function asks the user which ID it should select
        The type input is used to determine what kind of ID the program should be asking for
        and to determine where to go to next
        # TODO give an example on how what the getattr finds
        '''
        user_input = input(f'Type the ID of the desired {id_type} or q to go back:\n')
        if user_input.isdigit():
            # Get the function from the class based on the id type
            func = getattr(self, 'inspect_' + id_type)
            func(user_input)
        elif not user_input == 'q':
            self.inspect_specific(id_type)
            print(f'The {id_type} ID must be an integer')
            
    def inspect_user(self, user_id: str) -> None:
        while True:
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
                        self.fetcher.fetch_all_of_topic('users/' + user_id)
                    case '2':
                        self.fetcher.fetch_all_of_topic('users/' + user_id + '/todos')
                    case '3':
                        self.fetcher.fetch_all_of_topic('users/' + user_id + '/albums')
                    case '4':
                        self.inspect_specific('album')
                    case '5':
                        self.fetcher.fetch_all_of_topic('users/' + user_id + '/posts')
                    case '6':
                        self.inspect_specific('post')
                    case '9':
                        break
                    case 'q':
                        self.exit = True
                    case default:
                        print('Invalid option')
            if self.exit:
                return
        
    def inspect_album(self, album_id: str) -> None:
        while True:
            user_input = input('1. Display the data of album\n'
                               '2. Inspect a specific photo\n'
                               '9. Return\n'
                               'q. Exit\n')
            match user_input:
                    case '1':
                        self.fetcher.fetch_all_of_topic('/albums/' + album_id)
                    case '2':
                        self.inspect_specific('photo')
                    case '9':
                        break
                    case 'q':
                        self.exit = True
                    case default:
                        print('Invalid option')
            if self.exit:
                return

    def inspect_photo(self, photo_id: str) -> None:
        self.fetcher.fetch_all_of_topic('/photos/' + photo_id)

    def inspect_post(self, post_id: str) -> None:
        self.fetcher.fetch_all_of_topic('/posts/' + post_id)

        

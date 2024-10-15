from api_interactor.api_interactor import api_interactor



if __name__ == "__main__":
    tmp = api_interactor(['users', 'posts'])
    tmp.loop()
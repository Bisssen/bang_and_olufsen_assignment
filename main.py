from api_interactor.fetcher import fetcher
from api_interactor.text_gui import text_gui


if __name__ == "__main__":
    fetch: fetcher = fetcher()
    gui: text_gui = text_gui(fetch)
    gui.loop()

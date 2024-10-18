# Bang & Olufsen Coding Assignment
## The application
The application is a simple text GUI, which enables the user to make **GET** calls to https://jsonplaceholder.typicode.com and print the response. The full path to a resource can be used or the nested routes can be explored through the GUI.

### How to run the application:
1. Install the necessary Python packages by typing:
```properties
pip install requirement.txt
```  
2. Run the application by typing:
```properties
python main.py
```

## Tests
The tests associated with the application can be run by typing:
```properties
pytest
```
The tests are divided into two groups: the text GUI and the fetcher. These test groups can be individually run by typing:
```properties
pytest -m fetcher
```
```properties
pytest -m text_gui
```


### Tests through GitHub Actions
Alternatively, the tests can be run through the GitHub Actions:
1. Navigate to the [GitHub](https://github.com/Bisssen/bang_and_olufsen_assignment) page.
2. Click the [*Actions*](https://github.com/Bisssen/bang_and_olufsen_assignment/actions) bar.
3. Click [*Run tests*](https://github.com/Bisssen/bang_and_olufsen_assignment/actions/workflows/run_test_action.yaml) in the left column.
4. Click *Run workflow* and select *Run workflow* in the drop down.

### Test coverage report
The test coverage report can be generated in the console by typing:
```properties
pytest --cov .
```
The test coverage report can also be created in HTML format:
1. Type the following command:
```properties
pytest --cov-report html --cov .
```
2. A directory called *htmlcov* should now have been created. Navigate into it.
3. Open the HTML file called *index* with any browser.

## Mypy
Mypy can be used to ensure type hinting is utilized throughout the project by typing:
```properties
mypy tests api_interactor
```
The **pyproject.toml** file also ensures that missing type hinting is highlighted by Visual Studio Code.

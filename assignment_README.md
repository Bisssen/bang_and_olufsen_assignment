IMPORTANT
=========

This task will be reviewed by Bang & Olufsen Developer(s). To maintain anonymity, please do not provide your name or email address or any other personal identifiable information.

Introduction
============

This task aims to evaluate following skills
* Object oriented programming skills in Python
* Level of awareness around Python Type Hinting and Static Type Checking
* Understanding of test coverage and test design skills
* Auto-test writing skills using Python's Test Framework like pytest
* Continuous Integration/Continuous Deployment (CI/CD) skills
* Technical writing and documentation skills
* Comfort level with respect to using Linux based development environment

Task Description
================

1. Create a `Python` application (with v3.10 or higher) using Object Oriented Programming principles that makes use of type hints throughout the code. The application will interact with the JSONplaceholder API (https://jsonplaceholder.typicode.com/).
The application should be able to fetch and print data from the JSONplaceholder API. Specifically, it should fetch data from at least two different endpoints, such as `/posts` and `/users`.
2. Write type hinting for all your function and method definitions in your code. Introduce static type checking into your codebase using a tool like `Mypy`. Your code should pass all Mypy checks without any errors. You can run Mypy on your codebase with the command `mypy your_code.py.`
3. Write tests for your application's interaction with the JSONplaceholder API using `pytest` framework. Your tests should use important pytest features like fixtures for setup and teardown, parametrization for running the same test function with different arguments, and markers for categorizing tests. You can make use of the `requests-mock` package to mock the responses from the JSONplaceholder API. The tests should not make actual network requests. Ensure that your tests cover both successful API requests and failure scenarios.
Provide a test coverage report using a tool like `pytest-cov`.
4. Implement a GitHub workflow to automate the execution of the pytest suite, triggered manually via the GitHub Actions user interface.
5. Write a `README` file detailing how to run your application, how to run tests, how to check for type errors using `Mypy`, and how to view the test coverage report. Your README should be clear, concise, and complete, demonstrating your technical writing and documentation skills.

Submission
==========
Please share your solution with us by pushing your code to a GitHub repository and providing the repository link, ensuring it is public or accessible with the appropriate permissions.


Estimated completion time: 1-2 days

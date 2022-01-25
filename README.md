# RPG Character Manager

This is a character manager to create resources for tabletop RPG games

## Requirements

- Postgresql

## Installation

1. Clone the project
2. Create a virtual environment to install dependencies. In console, type "pip install -r requirements.txt"
3. On line 174 of main.py, change "db_url" value to match your Postgresql configuration.
4. Run the server. In console, type "uvicorn main:app"

## Usage

To test the routes and see the requierements and returns of each endpoint, go to "localhost:8000/docs".

To run the tests, type "pytest" in the console.

## Contributing
This is a WIP by Rodrigo Ibaceta. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
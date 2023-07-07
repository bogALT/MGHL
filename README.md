# mvn package analyzer
This project will analyse the passed package on maven repository and provide a buch of metrics for code quality evaluation.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. 

### Prerequisites

Install requirements from `requirements.txt`.
Create the following folders:

-`gh_repos`

-`HTML_Reports`

-`packages`

-`pom_jar`
in the project folder

### Installing

Enter the folder

## Running the tests

usage: python3 main.py [-h] [-gav GAV] [-slimit SLIMIT]

options:
  -h, --help      show this help message and exit
  -gav GAV        insert group artefact and version (default: None)
  -slimit SLIMIT  files bigger than this will not be examined (default: None)

### Usage

Example of usage: `python3 main.py -gav org.lucee:lucee:5.4.0.80`
Output will be saved in `HTML_Report` folder

## Authors

  - **Bojan Poletan** - *Something* -
    [PurpleBooth](https://github.com/bogalt)

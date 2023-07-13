# MVN Packages Analyzer


Project course application. This application will analize the passed maven package in GAV form and prompt some evaluated metrics that may be used for code evaluation.

## Installation

Download the project from the GitHub page and enter into it with the terminal. Install the components in `requirements.txt`. No more installations are required


## Usage

```python
usage: main.py [-h] [-gav GAV] [-slimit SLIMIT]

description app

options:
  -h, --help      show this help message and exit
  -gav GAV        insert group artefact and version (default: None)
  -slimit SLIMIT  files bigger than this will not be examined (default: None)
```

# returns
It will print an outpt on the screen and save an HTML file in `HTML_Reports` directory called `<g_a_v.html>` where `g`, `a` and `v` are: `group id`, `artefact id` and `version`.

# Usage Examples
```python
python3 main.py -gav com.alibaba:fastjson:2.0.30 -slimit 0.1
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

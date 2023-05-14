# Script for fully automatic creation of a repository for porting cppquiz.org questions from C++17 to C++20

Based on previous porting repo forks: https://github.com/TartanLlama/cppquiz17

## Features

1. Fully automatic export questions to directory structure and create GitHub repo with issues
2. Generate customized `README.md` for each question containing link to Compiler Explorer with the source code of the question, links to standard C++17 (and possible C++20) in its explanation.
3. Script to export questions as json after porting questions
4. Simple error handling

## Usage

*Requires `python3` and `gh` (logged in)*

```
$ ./create_repo.sh
$ ./create_issues.sh
```

Note: GitHub has an internal limit for queries (i.g. `issue create`): 20q/min, 150q/hour, so there is a separate script for creating issues and it takes some time to be completed.

To manually import/export questions from/to json use [this python script](/src/cppquiz_port.py):

```
usage: cppquiz_port.py [-h] {from_json,to_json} ...

CppQuizPort import/export utility.

positional arguments:
  {from_json,to_json}
    from_json          Export questions from JSON file to directory structure.
    to_json            Export questions from directory structure to JSON file.

optional arguments:
  -h, --help           show this help message and exit
```

## Algorithm

1. Create subdirectory `cppquiz20` in the current directory and initialize git repository there
2. Download published questions and export them to a directory structure in `/cppquiz20`
3. Paste to each question directory automatically customized [`README.md`](/readmes/README_QUESTION.md), paste [`README.md`](/readmes/README_REPOSITORY.md) of the repository 
4. Add [pull request](/readmes/TEMPLATE_PULL_REQUEST.md) template
5. Create remote private GitHub repository and push local one
6. Create issues for each question using customized text from [`README.md`](/readmes/README_QUESTION.md)

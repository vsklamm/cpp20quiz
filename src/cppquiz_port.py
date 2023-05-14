import argparse
import json
import os
import re
import sys
import urllib.parse
from typing import Tuple

import requests


class CppQuizPort:
    @staticmethod
    def normalize_newlines(text: str) -> str:
        return text.replace("\r\n", "\n")

    @staticmethod
    def format_reference(match: Tuple[str]) -> str:
        full_reference = match[0]
        section_name = match[2]
        paragraph_number = match[5]
        full_link = "https://timsong-cpp.github.io/cppwp/n4659/" + section_name
        if paragraph_number:
            full_link = full_link + "#" + paragraph_number
        return "<em><a href=\"" + full_link + "\">" + full_reference + "</a></em>"

    @staticmethod
    def standard_refs(text: str) -> list:
        section_name = u'(\[(?P<section_name>[\w:]+(\.[\w:]+)*)\])'
        possible_paragraph = u'(¶(?P<paragraph>\d+(\.\d+)*))*'
        regex = re.compile('§(' + section_name + possible_paragraph + ')')
        matches = regex.findall(text)
        return [CppQuizPort.format_reference(match) for match in matches]

    @staticmethod
    def compiler_explorer_link(source_code: str):
        editor = {
            "type": "component",
            "componentName": "codeEditor",
            "componentState": {
                "id": 1,
                "lang": "c++",
                "source": source_code,
                "options": {"compileOnChange": True, "colouriseAsm": True},
            },
        }

        compiler_details = {
            "gcc": {
                "compiler": "gsnapshot",
                "options": f"-std=c++20 -Wall -Wextra -Wno-unused -Wunused-value"
            },
            "clang": {
                "compiler": "clang_trunk",
                "options": f"-std=c++20 -stdlib=libc++ -Wall -Wextra -Wno-unused"
                " -Wno-unused-parameter -Wunused-result -Wunused-value"
            },
            "msvc": {
                "compiler": "vcpp_v19_latest_x64",
                "options": f"/std:c++20 /W4 /wd4100 /wd4101 /wd4189"
            },
        }

        compiler_output = [[{
            "type": "component",
            "componentName": "compiler",
            "componentState": {
                "id": compiler_id,
                "source": 1,
                "filters": {"b": 1, "execute": 1, "intel": 1, "commentOnly": 1, "directives": 1},
                **compiler_details[compiler_name],
            },
        },  {
            "type": "component",
            "componentName": "output",
            "componentState": {"compiler": compiler_id, "source": 1},
        }] for compiler_id, compiler_name in enumerate(("gcc", "msvc"), start=1)]

        executor = {
            "type": "component",
            "componentName": "executor",
            "componentState": {
                "id": 1,
                "source": 1,
                "compilationPanelShown": 1,
                **compiler_details["clang"],
            },
        }

        obj = {
            "version": 4,
            "content": [
                {
                    "type": "row",
                    "content": [
                        {"type": "column",
                         "content": [editor, executor]},
                        {"type": "column", "width": 30,
                         "content": compiler_output[0]},
                        {"type": "column", "width": 30,
                         "content": compiler_output[1]}
                    ],
                }
            ],
        }

        payload = json.dumps(obj)
        ceFragment = urllib.parse.quote(payload)
        url = "https://godbolt.org/#" + ceFragment
        return url
    
    @staticmethod
    def download_json(url: str) -> dict:
        """Download and return the JSON data from the given URL."""
        print("Downloading questions database...")
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def from_json(this, data):
        print("Importing data from JSON...")
        
        if not os.path.exists('questions'):
            os.makedirs('questions')

        questions = data["questions"]
        for question in questions:
            question_dir = os.path.join('questions', str(question["id"]))
            if not os.path.exists(question_dir):
                os.makedirs(question_dir)

            meta_data = {
                "id": question["id"],
                "result": question["result"],
                "answer": question["answer"],
                "state": "PUB",
                "difficulty": question["difficulty"]
            }

            with open(os.path.join(question_dir, "meta_data.json"), "w", encoding="utf-8") as file:
                json.dump(meta_data, file, indent=3)

            with open(os.path.join(question_dir, "question.cpp"), "w", encoding="utf-8") as file:
                question_text = this.normalize_newlines(question["question"])
                file.write(question_text)

            with open(os.path.join(question_dir, "hint.md"), "w", encoding="utf-8") as file:
                file.write(this.normalize_newlines(question["hint"]))

            with open(os.path.join(question_dir, "explanation.md"), "w", encoding="utf-8") as file:
                explanation_text = this.normalize_newlines(
                    question["explanation"])
                file.write(explanation_text)

            # Update README.md
            with open(os.path.join('..', 'readmes', 'README_QUESTION.md'), "r", encoding="utf-8") as file:
                readme_content = file.read()
            readme_content = readme_content.replace(
                '@@compiler_explorer_link@@', this.compiler_explorer_link(question_text))
            cpp17_refs = this.standard_refs(explanation_text)
            if cpp17_refs:
                cpp20_possible_refs = [ref.replace('n4659', 'std20') for ref in cpp17_refs]
                readme_content = readme_content.replace(
                    '@@c++17_standard_refs@@',
                    '    Links to C++17 standard used in the explanation for the current question:\n\n' +
                    '\n'.join(["        * " + ref for ref in cpp17_refs]) + '\n\n' +
                    '        Possible links to C++20 standard (⚠️Generated automatically for the convenience, can be invalid):\n\n' +
                    '\n'.join(["        * " + ref for ref in cpp20_possible_refs]))
                
            else:
                readme_content = readme_content.replace(
                    '@@c++17_standard_refs@@',
                    '    There is no links to C++17 standard used in the explanation for the current question so might be helpful to add some\n\n')
            with open(os.path.join(question_dir, 'README.md'), "w", encoding="utf-8") as file:
                file.write(readme_content)

        print("Import completed successfully.")
        
    @classmethod
    def to_json(this, dir_path):
        print(f"Exporting data to JSON from directory: {dir_path}")
        
        cpp_standard = os.path.basename(dir_path)
        question_dirs = sorted(os.listdir(dir_path), key=int)
        questions = []

        for question_dir in question_dirs:
            question_path = os.path.join(dir_path, question_dir)
            question = {}

            with open(os.path.join(question_path, "meta_data.json"), "r", encoding="utf-8") as file:
                meta_data = json.load(file)
                question.update(meta_data)

            with open(os.path.join(question_path, "question.cpp"), "r", encoding="utf-8") as file:
                question["question"] = this.normalize_newlines(file.read())

            with open(os.path.join(question_path, "hint.md"), "r", encoding="utf-8") as file:
                question["hint"] = this.normalize_newlines(file.read())

            with open(os.path.join(question_path, "explanation.md"), "r", encoding="utf-8") as file:
                question["explanation"] = this.normalize_newlines(file.read())

            questions.append(question)

        data = {
            "version": 1,
            "cpp_standard": "C++20",
            "questions": questions
        }

        with open(f"{cpp_standard}_updated.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=3)
            
        print("Export completed successfully.")

def main():
    parser = argparse.ArgumentParser(
        description="CppQuizPort import/export utility.",
        add_help=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser(
        "from_json", help="Export questions from JSON file to directory structure.")
    import_parser.add_argument("file_path", nargs='?', default=None, help="Path to the JSON file.")

    export_parser = subparsers.add_parser(
        "to_json", help="Export questions from directory structure to JSON file.")
    export_parser.add_argument(
        "dir_path", help="Path to the directory containing questions.")
    
    args = parser.parse_args()

    if args.command == "from_json":
        if args.file_path is not None:
            with open(args.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            CppQuizPort.from_json(data)
        else:
            data = CppQuizPort.download_json("https://cppquiz.org/static/published.json")
            CppQuizPort.from_json(data)
    elif args.command == "to_json":
        CppQuizPort.to_json(args.dir_path)
        


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Script execution failed: {e}")
        sys.exit(1) 

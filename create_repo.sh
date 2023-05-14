#!/bin/bash

# Check if "gh" utility exists in the system
if ! command -v gh &>/dev/null; then
  echo "Error: 'gh' utility is not installed. Please install it before running this script."
  exit 1
fi

# Check if "gh auth status" command returns a successful exit code
if ! gh auth status &>/dev/null; then
  echo "Error: 'gh auth status' command failed. Please ensure Git authentication is set up correctly."
  exit 1
fi

# Create subdirectory and initialize git repository
mkdir cppquiz20
cd cppquiz20

# Check if python3 is installed
if ! command -v python3 &>/dev/null; then
  echo "Error: Python3 is not installed. Please install it before running this script."
  exit 1
fi

# Create local repo
git init
mkdir .github
cp ../readmes/TEMPLATE_PULL_REQUEST.md ./.github/pull_request_template.md

# Run script to export questions from json
python3 ../src/cppquiz_port.py from_json
if [ $? -ne 0 ]; then
  echo "Error: Failed to import questions. Please check your setup and try again."
  exit 1
fi

cp ../readmes/README_REPOSITORY.md README.md

# Commit changes
git add . && git commit -m "Export all questions" --quiet
if [ $? -ne 0 ]; then
  echo "Error: Failed to commit changes. Please check your setup and try again."
  exit 1
fi

git branch -M main

# Create private remote repo and push commit
gh repo create -d "Porting questions on cppquiz.org to C++20" --private --source=. --disable-wiki --push
if [ $? -ne 0 ]; then
  echo "Error: Failed to create repository or push commit. Please check your setup and try again."
  exit 1
fi

echo "Repository created successfully."

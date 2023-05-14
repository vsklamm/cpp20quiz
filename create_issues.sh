#!/bin/bash

echo "⚠️ GitHub has a limit for API queries, creating issues process will take more than a hour..."

# Create GitHub issues in reverse numeric order so GitHub will show them in the right order

cd cppquiz20/questions
# Save directory names in an array
dirs=(*/)
# Convert array to multiline string and sort in reverse order
sorted_dirs=$(printf "%s\n" "${dirs[@]}" | sort -nr)

# Loop over lines in the sorted string
while IFS= read -r question_dir; do
    gh issue create --title "Question #${question_dir%%/}" --body "$(cat $question_dir/README.md)"
    if [ $? -ne 0 ]; then
        echo "The 'gh issue create' command failed in directory $question_dir. Stopping the loop."
        break
    fi
    sleep 24.1 # > 60min * 60sec / 150qu
done <<<"$sorted_dirs"

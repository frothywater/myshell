#!/bin/bash

exec > source.md

output() {
    echo "[$1]()"
    echo '```python'
    cat $1
    echo '```'
    echo
}

export -f output
find myshell -name "*.py" -type f -exec bash -c 'output "$0"' {} \;

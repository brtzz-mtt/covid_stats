#!/bin/bash

printf "\n"

if [ $1 = "build" ]; then
    nohup python3 main.py > nohup.log 2>&1 &
    NOHUP_PID=$!
    ./toolbox.sh checkup # executes checkup instructions
    rm templates/plots/*.html
    rm -R build/* 2>/dev/null
    wget -k -K -E -r -l 10 -p -N -F --restrict-file-names=windows --directory-prefix=build/ -nH http://127.0.0.1:5000/ # exports static website
    kill $NOHUP_PID
elif [ $1 = "checkup" ]; then
    coverage run -m --source=. pytest test.py -v # runs app tests
    coverage html --omit="data.py,*test.py" # creates a coverage report under ./htmlcov
    printf "\n"
    coverage report -m # prints report's summary to stdout
    printf "\n"
    pipreqs --savepath requirements.txt # saves current requirements
    pylint modules/ # see https://github.com/PyCQA
elif [ $1 = "push" ]; then
    git status
    git add -A
    git commit -a
    git push
    git checkout master
    git pull
    git merge dev
    git push
    git checkout dev
else
    echo "???"
fi

printf "\n"

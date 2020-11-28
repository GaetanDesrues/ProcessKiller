#!/usr/bin/env bash

# setup python interpreter
py=python

# Create a temporary directory `/tmp/tmp.XXXX`
PID_DIR="/tmp/tmp.known_location"
mkdir -p $PID_DIR

# function to start a task identifed by first argument $1
function start() {
  $py "start_$1.py" &
  echo $! > "$PID_DIR/$1.pid"
}

# define tasks according to python modules' filename
tasks=("my_task_1" "my_task_2")

# Start long tasks saving the pids in `/tmp/tmp.XXXX/<my_task_*>.pid`
for task in ${tasks[@]}; do start $task; done

# Start the main program
printf "Now try to '^C'\n\n"
$py start_main.py

# After end of main, print process list
printf "\n --- Processes:\n"
ps -A | grep python

# delete folder
rm -r $PID_DIR
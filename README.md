# Terminal TO-DO List Application

## Video Demo:  [Watch on Youtube](https://youtu.be/xtpRCzKbLwc)

### Description: todo.py

------

The terminal TODO List Application is a simple TODO list functionality built within the terminal. This project is meant to create task lists within your working environment with backend support to access them anytime. The program allows users to specify, access, modify and view their lists and tasks all via the command line. The program currently uses a procedural approach and is based off on `sqlite3` database for storage and `rich` terminal text formatter for output.

------

The `~/project` directory currently contains:

- `project.py`: The main program
- `test_project.py`: Unit tests in `pytest`
- `requirements.txt`: List of all required libraries
- `lists.db`: A sqlite database for backend storage

------

The motivation behind this project was my day to day struggle remembering the tasks I need to do for a certain project. Only if I had a way of getting all the stuff listed somewhere alongside the terminal I'm working on without those pesky hassles of getting GUI apps to do the same. Low and behold, `todo.py`. I was always fascinated by the UNIX coreutil tools and the convinence they offer to us programmers, which inspired the design.

## Usage

    Usage: python todo.py [OPTION]... [LIST]... [TASK]...
    A terminal TO-DO list application.

    Options:
    Mandatory arguments to long options are mandatory for short options too.
    -N, --new-list      Creates a new list
    -l, --list          List all existing lists
    -d, --delete        Delete an existing list
    -n, --new-task      Creates a new task in the list
    -v, --view          View an existing list with tasks
    -m, --mark          Mark a task as completed
    -r, --remove        Remove a task from the list
    -h, --help          Display this help and exit

    The new-list, view and delete arguments support atmost three list operations simultaneously.
    The new-task, mark and remove arguments supports atmost two tasks in a single list at a time.
    The mark and remove arguments also support input as initials of the task to be marked/removed.


## Next Steps
Improving upon the codebase using more valid approach and succinct code.

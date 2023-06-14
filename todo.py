# Imported libraries
from rich.console import Console
from rich.table import Table, Column
from rich.theme import Theme
from rich.tree import Tree
import sqlite3
import sys

# Setting up rich themes and console
custom_theme = Theme(
    {
        "warning": "indian_red1",
        "error": "bold red1",
        "normal": "cyan2",
        "task": "bold cyan1",
        "marked_task": "strike color(152)",
        "success": "green3",
    }
)
console = Console(theme=custom_theme)

# Usage Documentation
DOC = """Usage: python todo.py [OPTION]... [LIST]... [TASK]...
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
"""

# Setting up flags
SHORT_FLAGS = ["N", "l", "d", "n", "v", "m", "r", "h"]
LONG_FLAGS = [
    "new-list",
    "list",
    "delete",
    "new-task",
    "view",
    "mark",
    "remove",
    "help",
]


# Main function
def main():
    options = get_flags()
    connection, cursor = db_init()
    perform_ops(options, cursor)
    db_save(connection)


# Database setup
def db_init():
    """Creates a database named lists and returns the connection and the cursor object to the same"""
    con = sqlite3.connect("lists.db")
    cur = con.cursor()
    return con, cur


def db_save(con):
    """Commits changes to the database and closes the connection"""
    con.commit()
    con.close()


# Flag/option setup
def collect_args():
    """Checks for arguments passed and filters out flags/options"""
    if len(sys.argv) < 2:
        sys.exit(
            console.print(
                "Usage: python project.py [OPTION]... [LIST]... [TASK]... \nUse -h or --help for more details",
                style="normal",
            )
        )
    else:
        inp_flags = [arg.lstrip("-") for arg in sys.argv[1:] if "-" in arg]
        return inp_flags


def seperate_flags(flags: list):
    """Seperates the long and the short flags"""
    for flag in flags:
        if flag in LONG_FLAGS:
            return flags
        else:
            return list(flag)


def flag_check(flags: list):
    """Checks for a legal flag"""
    for flag in flags:
        if flag not in [*SHORT_FLAGS, *LONG_FLAGS]:
            sys.exit(
                console.print(
                    "todo.py: invalid option: Use -h or --help for more details.",
                    style="error",
                )
            )
    else:
        return flags


def get_flags():
    """Abstracts out the flag functionality"""
    args = collect_args()
    flags = seperate_flags(args)
    return flag_check(flags)


# List operation setup
def create_list(name: str, cur):
    """Creates a new list specified if it does not exist"""
    cur.execute(
        """SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?""",
        (name.replace(" ", "_"),),
    )
    check = cur.fetchone()
    # Check for existence
    if check[0] == 0:
        cur.execute("CREATE TABLE {}(task, status)".format(name.replace(" ", "_")))
        console.print(f"List: [b]{name}[/b] created!", style="success")
    else:
        raise IndexError


def view_lists(cur):
    """Outputs all the lists in the database"""
    cur.execute(
        "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
    )
    lists = cur.fetchall()
    tree = Tree("Your lists", style="italic bold magenta")
    for list in lists:
        tree.add(list[0].replace("_", " "), style="not italic cyan u")
    console.print(tree)
    return tree


def delete_list(name: str, cur):
    """Deletes the list specified by the user"""
    console.print(
        f"Do you really want to delete list [b]{name}[/b]? (y/N) ", style="warning"
    )
    choice = input()
    if choice in ["y", "Y", "yes"]:
        try:
            cur.execute("DROP TABLE {}".format(name.replace(" ", "_")))
            console.print(f"List: [b]{name}[/b] deleted!", style="warning")
        except sqlite3.OperationalError:
            sys.exit(
                console.print(
                    "todo.py: invalid name: no such list found", style="error"
                )
            )
    else:
        sys.exit()


# Task operation setup
def make_task(list, task, cur):
    """Creates a new task in the list specified and sets its status"""
    status = "undone"
    cur.execute(
        """INSERT INTO {} VALUES (?, ?)""".format(list.replace(" ", "_")),
        (task, status),
    )
    console.print("List successfully modified.", style="success")


def view_tasks(list, cur):
    """'View the tasks in the corresponding list specified and format based on status"""
    try:
        cur.execute("""SELECT * FROM {}""".format(list.replace(" ", "_")))
    except sqlite3.OperationalError:
        sys.exit(
            console.print(
                "todo.py: invalid list: specified list not found.", style="error"
            )
        )
    table = Table(Column(list, justify="center"))
    entries = cur.fetchall()
    for entry in entries:
        cur.execute(
            "SELECT status FROM {} WHERE task=?".format(list.replace(" ", "_")),
            (entry[0],),
        )
        status = cur.fetchall()
        if status[0][0] == "undone":
            table.add_row(entry[0], style="task")
        else:
            table.add_row(entry[0], style="marked_task")
    console.print(table)
    return table


def mark_task(list, task_initials, cur):
    """'Marks the status of the task as completed based on the initials of the task"""
    cur.execute(
        'UPDATE {} SET status = "done" WHERE task LIKE ?'.format(
            list.replace(" ", "_")
        ),
        (f"{task_initials}%",),
    )
    console.print("List successfully modified.", style="success")


def remove_task(list, task_initials, cur):
    cur.execute(
        "DELETE FROM {} WHERE task LIKE ?".format(list.replace(" ", "_")),
        (f"{task_initials}%",),
    )
    console.print("List successfully modified.", style="success")


# User specified operation
def perform_ops(flags: list, cur):
    """Extracts out the list name and tasks and performs operation based on flags specified"""
    inp_texts = [text for text in sys.argv[1:] if "-" not in text]
    if len(inp_texts) > 3:
        sys.exit(
            console.print(
                "todo.py: invalid usage: number of arguments exceeded limit.",
                style="error",
            )
        )
    try:
        for flag in flags:
            if flag in ["N", "new-list"]:
                blank_check(inp_texts)
                for list in inp_texts:
                    create_list(list, cur)
            if flag in ["l", "list"]:
                view_lists(cur)
            if flag in ["d", "delete"]:
                blank_check(inp_texts)
                for list in inp_texts:
                    delete_list(list, cur)
            if flag in ["n", "new-task"]:
                list = inp_texts[0]
                tasks = check_names(inp_texts, cur)
                for task in tasks:
                    make_task(list, task, cur)
            if flag in ["v", "view"]:
                for list in inp_texts:
                    view_tasks(list, cur)
            if flag in ["m", "mark"]:
                list = inp_texts[0]
                tasks = check_names(inp_texts, cur)
                for task in tasks:
                    mark_task(list, task, cur)
            if flag in ["r", "remove"]:
                list = inp_texts[0]
                tasks = check_names(inp_texts, cur)
                for task in tasks:
                    remove_task(list, task, cur)
            if flag in ["h", "help"]:
                console.print(DOC, style="normal")
    except IndexError:
        sys.exit(
            console.print(
                "todo.py: invalid usage: incorrect number of arguments specified.",
                style="error",
            )
        )


# Checking user input names
def check_names(names: list, cur):
    cur.execute(
        "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
    )
    existing_lists = cur.fetchall()
    if (names[0].replace(" ", "_"),) not in existing_lists:
        sys.exit(
            console.print(
                "todo.py: invalid list: specified list not found.", style="error"
            )
        )
    tasks = names[1:]
    blank_check(tasks)
    for task in tasks:
        if (task,) in existing_lists:
            sys.exit(
                console.print(
                    "todo.py: invalid arguments: A task cannot be a list name",
                    style="error",
                )
            )
    else:
        return tasks


# Checks for a blank list
def blank_check(args):
    if args == []:
        raise IndexError


# Invoking main
if __name__ == "__main__":
    main()

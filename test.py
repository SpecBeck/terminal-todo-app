import sqlite3
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.table import Table, Column
from rich.tree import Tree
import sys


# Setting up rich
custom_theme = Theme({
    "warning": "bold red1",
    "task": "cyan3",
    "completed_task": "strike color(152)",
    "success": "bold green3"
})
console = Console(theme=custom_theme)

# Docstring
DOC = """Usage: python todo.py [OPTION]... [LIST]... [TASK]...
A terminal TO-DO list application.

Mandatory arguments to long options are mandatory for short options too.
-N, --new-list      Creates a new list 
-l, --list          List all existing lists
-d, --delete        Delete an existing list
-n, --new-task      Creates a new task in the list
-v, --view          View an existing list with tasks
-m, --mark          Mark a task as completed
-h, --help          Display this help and exit
"""
# Checking flags
SHORT_FLAGS = ["N", "l", "d", "n", "v", "m", "h"]
LONG_FLAGS = ["new-list", "list", "delete", "new-task", "view", "mark", "help"]
def collect_args():
    if len(sys.argv) < 2:
        sys.exit("Usage: python todo.py [OPTION]... [LIST]... [TASK]...")
    else:
        inp_flags = [arg.lstrip('-') for arg in sys.argv[1:] if "-" in arg]
        return inp_flags


def seperate_flags(flags):
    for flag in flags:
        if flag in LONG_FLAGS:
            return flags
        else:
            return list(flag)
        
def flag_check(flags):
    for flag in flags:
        if flag not in [*SHORT_FLAGS, *LONG_FLAGS]:
            sys.exit("Invalid option! Use -h or --help for more info!")
    else: 
        return flags

def filter_flags():
    args = collect_args()
    flags = seperate_flags(args)
    return flag_check(flags)


def perform_ops(flags, cur):
    inp_texts = [text for text in sys.argv[1:] if "-" not in text]
    try:
        for flag in flags:
            if flag in ["N", "new-list"]:
                create_list(inp_texts[0], cur)
            if flag in ["l", "list"]:
                view_lists(cur)
            if flag in ["d", "delete"]:
                delete_list(inp_texts[0], cur)
            if flag in ["n", "new-task"]:
                make_task(inp_texts[0], inp_texts[1], cur)
            if flag in ["v", "view"]:
                view_tasks(inp_texts[0], cur)
            if flag in ["m", "mark"]:
                completed_task(inp_texts[0], inp_texts[1], cur)
            if flag in ["h", "help"]:
                console.print(DOC)
    except IndexError:
        sys.exit("Incorrect number of arguments specified!")

# Database setup
def db_init():
    db = sqlite3.connect("lists.db")
    cur = db.cursor()
    return db, cur

def db_save(db):
    db.commit()
    db.close()


# List operations
def create_list(table, cur):
    cur.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?""", (table,))
    check = cur.fetchone()
    if check[0] == 0:
        cur.execute("CREATE TABLE {}(date, task, status)".format(table.replace(" ", "_")))
        console.print(f"List: [{table}] created!", style="success")


def view_lists(cur):
    cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'")
    lists = cur.fetchall()
    tree = Tree("Your lists", style="italic bold magenta")
    for list in lists:
        tree.add(list[0].replace("_", " "), style="cyan u")
    console.print(tree)
    return cur.fetchall()


def delete_list(table, cur):
    choice = input(f"Do you really want to delete list {table}? [y/N] ")
    if choice in ["y", "Y", "yes"]:
        cur.execute("DROP TABLE {}".format(table.replace(" ", "_")))
        console.print(f"List: [{table}] deleted!", style="warning")


# Task operations
def make_task(list, task, cur):
    dt = datetime.now()
    status = "undone"
    cur.execute("""INSERT INTO {} VALUES (?, ?, ?)""".format(list.replace(" ", "_")), (dt, task, status))

def view_tasks(list, cur):
    cur.execute("""SELECT * FROM {}""".format(list.replace(" ", "_")))
    table = Table(Column(list, justify="center"), title="Your lists")
    entries = cur.fetchall()
    for entry in entries:
        cur.execute("SELECT status FROM {} WHERE task=?".format(list.replace(" ", "_")), (entry[1],))
        status = cur.fetchall()
        if status[0][0] == "undone":
            table.add_row(entry[1], style="task")
        else:
            table.add_row(entry[1], style="completed_task")
    console.print(table)
    return cur.fetchall()

def completed_task(list, task, cur):
    cur.execute('UPDATE {} SET status = "done" WHERE task LIKE ?'.format(list.replace(" ", "_")), (f"{task}%", ))

def main():
    flags = filter_flags()
    db, cur = db_init()
    perform_ops(flags, cur)
    db_save(db)

if __name__ == "__main__":
    main()
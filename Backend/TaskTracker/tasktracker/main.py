# A dumb task manager commandline application.
# Copyright (C) 2024 Behnam (Wired Unwell)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import click
import datetime as dt
import json
from pprint import pp
import random
from prettytable import PrettyTable as pt
from prettytable import from_json

from trogon import tui


@tui()
@click.group()
def cli():
    pass


@click.command("list", help="List tasks")
@click.option(
    "-nd", "--nodone", default=False, is_flag=True, help="Don't list finished tasks."
)
@click.option(
    "-nt", "--notodo", default=False, is_flag=True, help="Don't list unstarted tasks."
)
@click.option(
    "-np",
    "--noinprogress",
    default=False,
    is_flag=True,
    help="Don't list inprogress tasks.",
)
@click.option(
    "-DD",
    "--duedate",
    default=None,
    is_flag=False,
    # type=dt.datetime,
    help="List tasks due",
)
@click.option(
    "-D", "--directory", default="./tasks", is_flag=False, help="Tasks directory"
)
def list_tasks(nodone, notodo, noinprogress, directory, duedate):
    # print("List tasks")
    with open(directory, "r", encoding="utf-8") as tasks_file:
        tasks = json.load(tasks_file)
    del_index = []
    for id in tasks:
        if (
            nodone
            and tasks[id]["status"] == "done"
            or notodo
            and tasks[id]["status"] == "todo"
            or noinprogress
            and tasks[id]["status"] == "inprogress"
        ):
            del_index += [id]
    for id in del_index:
        del tasks[id]

    table = pt()
    table.field_names = ["ID", "Status", "Title", "Deadline"]
    for item in tasks:
        icon = ""
        if tasks[item]["status"] == "done":
            icon = ""
        elif tasks[item]["status"] == "todo":
            icon = ""
        elif tasks[item]["status"] == "inprogress":
            icon = ""
        table.add_row(
            [
                tasks[item]["id"],
                icon,
                tasks[item]["title"],
                tasks[item]["duedate"],
            ]
        )
    print(table)


cli.add_command(list_tasks)


@click.command("new", help="Add a new task.")
@click.argument("title")
@click.option(
    "-D",
    "--description",
    default="",
)
@click.option(
    "-dd",
    "--duedate",
    default=dt.datetime.strftime(
        dt.datetime.now() + dt.timedelta(days=3), "%Y-%m-%d %H:%M"
    ),
    help="Due time/Deadline, format: 'yyyy-mm-dd HH:MM'. i.e. 2021-11-21 21:31",
)
@click.option(
    "-cd",
    "--createdtime",
    default=dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M"),
    help="Change the creation time of a task",
)
@click.option(
    "-s",
    "--status",
    default="todo",
    help="Change the status/progress of a task",
)
@click.option(
    "-D", "--directory", default="./tasks", is_flag=False, help="Tasks directory"
)
# Sorry, the date handling could be way better here
def new_task(title, description, duedate, createdtime, directory, status):
    try:
        duedate = dt.datetime.strptime(duedate, "%Y-%m-%d %H:%M")
    except ValueError:
        print("\033[1;31mDuedate format is broken\033[0m")
    except TypeError:
        if type(duedate) == "datetime":
            print("Already a datetime")
    else:
        try:
            createdtime = dt.datetime.strptime(createdtime, "%Y-%m-%d %H:%M")
        except ValueError:
            print("\033[1;31mCreated time format is broken\033[0m")
        except TypeError:
            if type(createdtime) == "datetime":
                print("Already a datetime")
        else:
            with open(directory, "r", encoding="utf-8") as tasks_file:
                tasks = json.load(tasks_file)
            task = {
                "id": str(len(tasks) + 1),
                "title": str(title),
                "duedate": str(duedate),
                "createdtime": str(createdtime),
                "status": str(status),
            }
            with open(directory, "w", encoding="utf-8") as tasks_file:
                while task["id"] in tasks:
                    task["id"] = str(random.randrange(100000, 999999))
                tasks[task["id"]] = task
                json.dump(tasks, tasks_file)


cli.add_command(new_task)


@click.command(name="edit", help="Edit and update your tasks")
@click.argument("id")
@click.option(
    "-d", "--done", default=False, is_flag=True, help="Set task's status to done"
)
@click.option(
    "-t", "--todo", default=False, is_flag=True, help="Set task's status to todo"
)
@click.option(
    "-p",
    "--inprogress",
    default=False,
    is_flag=True,
    help="Set task's status to in progress.",
)
@click.option("--delete", default=False, is_flag=True, help="Delete task.")
@click.option("-T", "--title", help="Change task's title.")
@click.option("-de", "--description", help="Change task's description.")
@click.option(
    "-D", "--directory", default="./tasks", is_flag=False, help="Tasks directory"
)
def edit_task(id, done, todo, inprogress, delete, title, description, directory):
    with open(directory, "r", encoding="utf-8") as tasks_file:
        tasks = json.load(tasks_file)
    if id in tasks:
        # This /is/ a cool variable name.
        wtf = True
        if delete:
            del tasks[id]
            wtf = False
        if done:
            tasks[id]["status"] = "done"
            wtf = False
        if todo:
            tasks[id]["status"] = "todo"
            wtf = False
        if inprogress:
            tasks[id]["status"] = "inprogress"
            wtf = False
        if title:
            tasks[id]["title"] = title
            wtf = False
        if description:
            tasks[id]["description"] = description
            wtf = False
        if wtf:
            print("Did you write the right command? Use --help.")
        else:
            tasks[id]["updatedtime"] = dt.datetime.strftime(
                dt.datetime.now(), "%Y-%m-%d %H:%M"
            )
        with open(directory, "w", encoding="utf-8") as tasks_file:
            json.dump(tasks, tasks_file)
    else:
        print("\033[1;31mCheck the id properly, I didn't find the task.\033[0m")


cli.add_command(edit_task)


@click.command(name="show", help="Show a task and its details")
@click.argument("id")
@click.option(
    "-D", "--directory", default="./tasks", is_flag=False, help="Tasks directory"
)
def show_task(id, directory):
    with open(directory, "r", encoding="utf-8") as tasks_file:
        tasks = json.load(tasks_file)
    if id in tasks:
        for key in tasks[id]:
            if tasks[id][key] != None:
                print(
                    "\033[3" + str(random.randrange(1, 8)) + "m" + tasks[id][key],
                    end="\t",
                )
        print("\033[0m")
    else:
        print("\033[1;31mCheck the id properly, I didn't find the task.\033[0m")


cli.add_command(show_task)

# cli.add_command(list_tasks, name="l")
# cli.add_command(new_task, "n")
# cli.add_command(edit_task, name="e")
# cli.add_command(show_task, name="s")

if __name__ == "__main__":
    cli()

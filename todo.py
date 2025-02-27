import subprocess
import argparse
import csv
import random
from typing import Optional
from typing import Sequence
from datetime import date
from time import sleep
from tqdm import tqdm
import sys


def write_file(fname, rows):
    with open(fname, "w") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "start", "end", "status"])
        writer.writeheader()
        writer.writerows(rows)


class TaskManager:
    def nrow(self):
        cnt = 0
        with open("taskfile0.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cnt += 1
        return cnt

    # Swap task order
    def make_top(self, id):
        self.swap_order(id, 1)

    def swap_order(self, id, to):
        if not (1 <= id <= self.nrow()):
            raise IndexError("Index is out of bound, so bad omegalul")

        if not (1 <= to <= self.nrow()):
            raise IndexError("Index is out of bound, so bad omegalul")

        id -= 1
        to -= 1
        rows = []
        with open("taskfile0.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        rows[id], rows[to] = rows[to], rows[id]

        write_file("taskfile0.csv", rows)

    # Delete Task
    def erase_task(self, id):
        if not (1 <= id <= self.nrow()):
            raise IndexError("Index is out of bound, so bad omegalul")
        tmp = []
        with open("taskfile0.csv", "r") as file, open("archived.csv", "a") as out:
            cnt = 1
            reader = csv.DictReader(file)
            writer = csv.DictWriter(out, fieldnames=["name", "start", "end", "status"])
            for row in reader:
                if cnt == id:
                    writer.writerow(row)
                else:
                    tmp.append(row)
                cnt += 1
        write_file("taskfile0.csv", tmp)

    # Add Task
    def add_task(self, name, end):
        if len(name) > 16:
            raise ValueError("Length of name is <= 16")
        with open("taskfile0.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "start", "end", "status"])
            writer.writerow(
                {"name": name, "start": self.getdate(), "end": end, "status": "0%"}
            )

    # printing
    def clear_screen(self):
        _ = subprocess.run("clear")

    def display(self):
        self.bar()
        id = 1
        with open("taskfile0.csv") as file:
            reader = csv.DictReader(file)
            print(self.format(-1, "Quest", "Start", "End", "Status"))
            for row in reader:
                print(
                    self.format(
                        id, row["name"], row["start"], row["end"], row["status"]
                    )
                )
                id += 1

    def bar(self):
        self.clear_screen()
        for i in tqdm(range(10)):
            sleep(random.choice([0.1, 0.2]))
        self.clear_screen()

    def format(self, id, quest, start, end, status):
        tmp = [
            self.getid(id),
            self.space(2),
            quest,
            self.space(21 - len(quest)),
            start,
            self.space(20 - len(start)),
            end,
            self.space(20 - len(end)),
            status,
        ]
        return "".join(tmp)

    def getdate(self):
        today = date.today()
        return today.strftime("%d/%m/%Y")

    def space(self, cnt):
        return " " * cnt

    def getid(self, i):
        if i == -1:
            return "##"
        if i < 10:
            return f"0{i}"
        return f"{i}"

def main(argv: Optional[Sequence[str]] = None) -> int:
    task_manager = TaskManager()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--add",
        nargs=2,
        type=str,
        help="enter name and deadline to add task to the list",
    )

    parser.add_argument(
        "-s", "--swap", nargs=2, type=int, help="swap the order of two tasks"
    )

    parser.add_argument(
        "-t", "--top", type=int, help="move task to top of the list"
    )

    parser.add_argument(
        "-e", "--erase", nargs="+", type=int, help="erase tasks from the list"
    )

    args = parser.parse_args(argv)

    if args.add != None:
        name = args.add[0]
        deadline = args.add[1]
        task_manager.add_task(name, deadline)
    if args.swap != None:
        first = args.swap[0]
        second = args.swap[1]
        try:
            task_manager.swap_order(first, second)
        except IndexError as error:
            print(error)
            return 1
    if args.top != None:
        id = args.top
        task_manager.make_top(id)
    if args.erase != None:
        ls = sorted(args.erase, reverse=True)
        for i in range(len(ls)):
            task_manager.erase_task(ls[i])
    task_manager.display()
    return 0


if __name__ == "__main__":
    sys.exit(main())

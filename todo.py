import subprocess
import argparse
import csv
import random
from datetime import date
from time import sleep
from tqdm import tqdm

def write_file(fname, tmp):
    with open(fname, "w") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "start", "end", "status"])
        writer.writeheader()
        for row in tmp:
            nm = row["name"]
            st = row["start"]
            ed = row["end"]
            ss = row["status"]
            writer.writerow({"name": nm, "start": st, "end": ed, "status": ss})

class Task:
    # Swap task order
    def make_top(self, id):
        self.swap_order(id, 0)

    def swap_order(self, id, to):
        id -= 1
        to -= 1
        tmp = []
        with open("taskfile0.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                nm = row["name"]
                st = row["start"]
                ed = row["end"]
                ss = row["status"]
                tmp.append({"name": nm, "start": st, "end": ed, "status": ss})
        tmp[id], tmp[to] = tmp[to], tmp[id]
        write_file("taskfile0.csv", tmp)
        self.display()

    # Delete Task
    def del_task(self, id):
        tmp = []
        with open("taskfile0.csv", "r") as file, open("archived.csv", "a") as out:
            cnt = 1
            reader = csv.DictReader(file)
            writer = csv.DictWriter(out, fieldnames=["name", "start", "end", "status"])
            for row in reader:
                nm = row["name"]
                st = row["start"]
                ed = row["end"]
                ss = row["status"]
                if cnt == id:
                    writer.writerow({"name": nm, "start": st, "end": ed, "status": ss})
                else:
                    tmp.append({"name": nm, "start": st, "end": ed, "status": ss})
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
        self.display()

    # printing
    def clear_screen(self):
        _ = subprocess.run("clear")

    def display(self):
        self.clear_screen()
        for i in tqdm(range(10)):
            sleep(random.choice([0.1, 0.2, 0.4]))
        self.clear_screen()
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


def main():
    task = Task()
    # name = input("Name? ")
    # deadline = input("deadline? ")
    # task.add_task(name, deadline)

    task.display()
    # id = int(input("Which task to delete: "))
    # task.del_task(id)

    id = int(input("from? "))
    to = int(input("to? "))
    task.swap_order(id, to)


if __name__ == "__main__":
    main()

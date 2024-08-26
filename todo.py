import subprocess
import argparse
import csv
from datetime import date

class Task:
    # Add Task
    def add_task(self, name, end):
        if len(name) > 16:
            raise ValueError("Length of name is <= 16")
        today = date.today()
        with open("taskfile0.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "start", "end", "status"])
            writer.writerow({"name": name, "start": self.getdate(), "end": end, "status": "0%"})

    # printing
    def clear_screen(self):
        _ = subprocess.run("clear")

    def display(self):
        self.clear_screen()
        id = 1
        with open("taskfile0.csv") as file:
            reader = csv.DictReader(file)
            print(self.format(-1, "Quest", "Start", "End", "Status"))
            for row in reader:
                print(self.format(id, row["name"], row["start"], row["end"], row["status"]))
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
        if i == -1: return "##"
        if i < 10: return f"0{i}"
        return f"{i}"


def main():
    task = Task()
    name = input("Give task name: ")
    end = input("Give end date: ")
    task.add_task(name, end)
    task.display()

if __name__ == "__main__":
    main()

import subprocess
import argparse


class Task:
    # Add Task

    # printing
    def clear_screen(self):
        _ = subprocess.run("clear")

    def display(self):
        self.ClearScreen()
        tmp = [
            "##",
            self.Space(2),
            "Quest",
            self.Space(16),
            "Start",
            self.Space(5),
            "End",
            self.Space(5),
            "Status",
        ]
        print("".join(tmp))

    def Space(self, cnt):
        return " " * cnt


def main():
    task = Task()
    task.display()


if __name__ == "__main__":
    main()

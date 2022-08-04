import sys
import threading
from queue import Queue


class ThreadBot(threading.Thread):
    def __init__(self):
        super().__init__(target=self.manage_table)
        self.cutlery = Cutlery(knives=0, forks=0)
        self.tasks = Queue()

    def manage_table(self):
        while True:
            task = self.tasks.get()
            if task == "prepare table":
                kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == "clear table":
                self.cutlery.give(
                    to=kitchen,
                    knives=self.cutlery.knives,
                    forks=self.cutlery.forks,
                )
            elif task == "shutdown":
                return


class Cutlery:
    def __init__(self, knives: int = 0, forks: int = 0):
        self.knives = knives
        self.forks = forks
        self.lock = threading.Lock()

    def __repr__(self):
        attributes = (
            ", ".join(f"{key}={value}" for key, value in vars(self).items()))
        return f"{self.__class__.__name__}({attributes})"

    def give(self, to: "Cutlery", knives: int = 0, forks: int = 0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives: int, forks: int):
        # this avoid to another thread read the state while other thread is
        # still reading it
        with self.lock:

            # the following sentences should cause a race condition
            self.knives += knives
            self.forks += forks


def main():
    global kitchen
    kitchen = Cutlery(knives=100, forks=100)
    bots = [ThreadBot() for _ in range(10)]

    for bot in bots:
        for i in range(int(sys.argv[1])):
            bot.tasks.put("prepare table")
            bot.tasks.put("clear table")
        bot.tasks.put("shutdown")

    print(f"Kitchen inventory before service: {kitchen}")

    for bot in bots:
        bot.start()

    for bot in bots:
        bot.join()

    print(f"Kitchen inventory after service: {kitchen}")

if __name__ == "__main__":
    main()

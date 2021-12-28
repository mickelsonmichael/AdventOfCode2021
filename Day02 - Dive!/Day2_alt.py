
class Command:
    def __init__(self, command):
        self.direction, xStr = command.split(" ")
        self.position = int(xStr)

class Sub:

    def __init__(self):
        self.depth = 0
        self.position = 0
        self.aim = 0

    def reportPosition(self):
        print("         |_")
        print("   _____|~ |____             Current position:")
        print("  (  --         ~~~~--_,       ", str(self.position * self.depth))
        print("   ~~~~~~~~~~~~~~~~~~~'`")

        return self

    def executeSingle(self, command: Command):
        if command.direction == "forward":
            self.position += command.position
            self.depth += self.aim * command.position
        elif command.direction == "up":
            self.aim -= command.position
        elif command.direction == "down":
            self.aim += command.position

    def execute(self, filename):
        with open(filename) as commands:
            for command in commands:
                cmd = Command(command)

                self.executeSingle(cmd)
        return self

Sub().execute("./Day2Input.txt").reportPosition()



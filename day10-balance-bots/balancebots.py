#!/usr/bin/python3
"""adventofcode.com/2016/day/10

Part One
--
Seems suited for an OO approach. Bot objects will hold state of each bots'
values and will activate when two values are held. Activation will set off
the first attached command or leave the bot in "activated" state in which
the next command will execute immediately. Commands can probably be in form
Command.low and Command.high, to give their low/high values to a bot or output.
Bots and outputs will have a separate registry which Bots all know how to access.

Part Two
--
Everything we did in part one was all we needed for part two. Just printed out
the output bins 0, 1, and 2 at the end of the process.
"""
from collections import defaultdict, namedtuple


FILENAME = "input.txt"
Instruction = namedtuple("Instruction", ["bot", "action", "payload"])
CommandTarget = namedtuple("CommandTarget", ["target", "id"])
Command = namedtuple("Command", ["low", "high"])


class Bot:
    """Bots store low and high values and activate when both are filled.

    Commands are given to bots which involve transfering their low and high
    values elsewhere. The bot only executes these commands after it has two
    values.

    Instance variables:
    key -- id of bot
    low -- the lower value or None
    high -- the higher value or None
    commands -- queue of commands, the first of which will execute when activated

    Instance methods:
    accept_value -- store value in low or high slot and activate if both are filled.
    accept_command -- execute command immediately if activated; queue otherwise.
    """

    def __init__(self, key, bot_registry=None, output_registry=None):
        self.key = key
        self.low = None
        self.high = None
        self.commands = []
        self.activated = False
        self.bot_registry = bot_registry
        self.output_registry = output_registry

    def accept_value(self, value):
        """Store value and self-activate if two values have been given."""
        if self.low is None:
            self.low = value
        else:
            if self.low > value:
                self.low, self.high = value, self.low
            else:
                self.high = value
            self.activate()

    def give_value(self, value, target, key):
        """Give value from robot to some target."""
        if value == "low":
            if target == "bot":
                self.bot_registry[key].accept_value(self.low)
            elif target == "output":
                self.output_registry[key].append(self.low)
            self.low = None
        elif value == "high":
            if target == "bot":
                self.bot_registry[key].accept_value(self.high)
            elif target == "output":
                self.output_registry[key].append(self.high)
            self.high = None

    def activate(self):
        """Execute the next pending command, or set self to activated status."""
        if len(self.commands) > 0:
            self.execute_command(self.commands.pop(0))
        else:
            self.activated = True

    def accept_command(self, command):
        """Execute command if activated. Queue command if not."""
        if self.activated:
            self.execute_command(command)
        else:
            self.commands.append(command)

    def execute_command(self, command):
        """Execute the command. This method should not be called publicly.

        Should only be called when the bot is activated.

        Possible refactor is to abstract out implementation of Bot and output registries
        and share interface for sending values. Probably an Output class with an accept_value
        method. Does python have interfaces?
        """
        if self.high == 61 and self.low == 17:
            print("PART ONE: BOT {}".format(self))
        for value, target, key in (("low", *command.low), ("high", *command.high)):
            self.give_value(value, target, key)

    def __str__(self):
        return "Bot {}: low - {}, high - {}".format(self.key, self.low, self.high)

    def __repr__(self):
        return str(self)


class BotRegistry(object):
    """Custom registry for bots.

    Creates a new bot if it hasn't been registered and assign it an id.
    """

    def __init__(self, output_registry):
        self.registry = {}
        self.output_registry = output_registry

    def __getitem__(self, key):
        if key not in self.registry:
            self.registry[key] = Bot(key, bot_registry=self, output_registry=self.output_registry)
        return self.registry[key]


def parse_instruction(raw_instruction):
    """Parse instruction and return an actionable tuple.

    e.g.
    value X goes to bot B
    bot B gives low to bot C and high to bot D
    bot B gives low to output Y and high to output Z
    """
    split = raw_instruction.split()
    if split[0] == "value":
        bot, action, value = split[5], "value", int(split[1])
        return Instruction(bot, action, value)
    else:
        bot, action = split[1], "command"
        low_target = split[5:7]
        high_target = split[10:]
        command = Command(low=CommandTarget._make(low_target),
                          high=CommandTarget._make(high_target))
        return Instruction(bot, action, command)


def control_bots(raw_instructions):
    """Parse instructions and send commands/values to bots."""
    output_registry = defaultdict(list)
    bot_registry = BotRegistry(output_registry)
    for raw_instruction in raw_instructions:
        instruction = parse_instruction(raw_instruction)
        if instruction.action == "value":
            print("sending value: {} to bot {}".format(instruction.payload, instruction.bot))
            bot_registry[instruction.bot].accept_value(instruction.payload)
        elif instruction.action == "command":
            print("sending command: {} to bot {}".format(instruction.payload, instruction.bot))
            bot_registry[instruction.bot].accept_command(instruction.payload)
        print("Bot after instruction: {}".format(bot_registry[instruction.bot]))
    print("output 0 - {}\noutput 1 - {}\noutput 2 - {}".format(output_registry["0"],
                                                               output_registry["1"],
                                                               output_registry["2"]))


if __name__ == "__main__":
    with open(FILENAME) as inputFile:
        control_bots(line.strip() for line in inputFile)

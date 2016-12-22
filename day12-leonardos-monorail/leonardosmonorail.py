#!/usr/bin/python3
'''adventofcode.com/2016/day/12

Part One
--
Instructions:
cpy x y copies x (either an integer or the value of a register) into register y.
inc x increases the value of register x by one.
dec x decreases the value of register x by one.
jnz x y jumps to an instruction y away (positive means forward; negative means backward),
but only if x is not zero.

Need to keep track of four registers that start at 0 and can hold any integer.
Output is value of a after reading in input instructions.
'''
from enum import Enum


FILENAME = 'input.txt'


class Command(Enum):
    '''Assembunny instruction.'''
    cpy = 1
    inc = 2
    dec = 3
    jnz = 4


class Register(Enum):
    '''Register available in computer.'''
    a = 1
    b = 2
    c = 3
    d = 4


class Instruction:
    '''Instructions are given to parser to determine program execution.

    Instance variables:
    command -- instruction command determines behavior
    arg_one -- first argument of Instruction
    arg_two -- second argument of Instruction
    '''

    def __init__(self, command, arg_one=None, arg_two=None):
        self.command = command
        self.arg_one = arg_one
        self.arg_two = arg_two

    @staticmethod
    def parse_sentence(sentence):
        '''Return an Instruction object built from raw sentence.'''
        split = sentence.split()
        command = Command[split[0]]
        args = [None, None]
        for index, arg in enumerate(split[1:]):
            try:
                args[index] = int(arg)
            except ValueError:
                args[index] = Register[arg]
        return Instruction(command, args[0], args[1])

    def __str__(self):
        return "{} {} {}".format(self.command, self.arg_one, self.arg_two)

    def __repr__(self):
        return str(self)


class Computer(object):
    '''A computer allows for execution of commands and keeps track of register states.

    Instance variables:
    registers -- map from registers to values
    instruction_pointer -- keeps track of which instruction program is on

    Instance methods:
    execute_program -- execute a given program on the computer
    '''

    def __init__(self, registers):
        self.registers = {register: 0 for register in registers}
        self.instruction_pointer = None

    def execute_program(self, instructions):
        '''Execute the given instruction on the computer.

        Possible instructions:
        cpy x y copies x (either an integer or the value of a register) into register y.
        inc x increases the value of register x by one.
        dec x decreases the value of register x by one.
        jnz x y jumps to an instruction y away (positive means forward; negative means backward),
            but only if x is not zero.
        '''
        self.instruction_pointer = 0
        while self.instruction_pointer < len(instructions):
            instruction = instructions[self.instruction_pointer]
            print('Executing instruction ({})'.format(instruction))
            if instruction.command == Command.jnz:
                self.instruction_pointer += self.jump(instruction.arg_one, instruction.arg_two)
            else:
                if instruction.command == Command.cpy:
                    self.copy(instruction.arg_two, instruction.arg_one)
                elif instruction.command == Command.inc:
                    self.increment(instruction.arg_one)
                elif instruction.command == Command.dec:
                    self.decrement(instruction.arg_one)
                self.instruction_pointer += 1
            print(self)
        print('end...')

    def copy(self, target_register, source):
        '''Copy integer or value of register from source into target_register.'''
        self.registers[target_register] = (source if isinstance(source, int)
                                           else self.registers[source])

    def increment(self, target_register):
        '''Increment value of target register by one.'''
        self.registers[target_register] += 1

    def decrement(self, target_register):
        '''Decrement value of target register by one.'''
        self.registers[target_register] -= 1

    def jump(self, check_target, steps):
        '''Return number of instruction steps to jump away from current.

        Caller will use this number to move instruction pointer. If {check_target}
        is zero, then return one so that program execution will continue as normal.
        '''
        check = check_target if isinstance(check_target, int) else self.registers[check_target]
        return 1 if check == 0 else steps

    def __str__(self):
        computer_string = '{}: Instruction pointer - {}'.format(self.__class__.__name__,
                                                                self.instruction_pointer)
        register_strings = ['{}: {}'.format(register, self.registers[register])
                            for register in self.registers]
        return '\n'.join([computer_string] + register_strings)


def execute_instructions(instructions):
    '''Return end result of Register A after running given instructions.'''
    registers = (Register.a, Register.b, Register.c, Register.d)
    computer = Computer(registers)
    computer.copy(Register.c, 1)
    computer.execute_program(instructions)


if __name__ == "__main__":
    with open(FILENAME) as inputFile:
        execute_instructions([Instruction.parse_sentence(sentence.strip()) for sentence in inputFile])

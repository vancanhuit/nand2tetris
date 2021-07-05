#!/usr/bin/env python3
import os
import sys
import re


JUMP_MNEMONIC_CODE = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

DEST_MNEMONIC_CODE = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}

COMP_MNEMONIC_CODE = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101',
}


symbol_table = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
}

allocated_address = 16


class Code:
    @staticmethod
    def dest(mnemonic: str) -> str:
        return DEST_MNEMONIC_CODE[mnemonic]

    @staticmethod
    def comp(mnemonic: str) -> str:
        return COMP_MNEMONIC_CODE[mnemonic]

    @staticmethod
    def jump(mnemonic: str) -> str:
        return JUMP_MNEMONIC_CODE[mnemonic]


class Command:
    def __init__(self, command: str):
        self._command = command

    def code(self) -> str:
        global allocated_address
        c = ''
        # A instruction pattern
        pattern = re.compile(r'^@(.*)$')
        m = pattern.match(self._command)
        if m is not None:
            v = m.group(1)
            if not v.isdigit():
                if symbol_table.get(v, '') == '':
                    symbol_table[v] = allocated_address
                    allocated_address += 1
                v = symbol_table[v]
            c = '0{0:015b}'.format(int(v))
            return c
        parts = self._command.split(';')
        jump = 'null'
        if len(parts) == 2:
            jump = parts[1]
        
        parts = parts[0].split('=')
        comp = ''
        dest = 'null'
        if len(parts) == 1:
            comp = parts[0]
        elif len(parts) == 2:
            dest = parts[0]
            comp = parts[1]
        
        c = '111{}{}{}'.format(
                Code.comp(comp), Code.dest(dest), Code.jump(jump))
        return c


def normalize(string: str) -> str:
    pattern = re.compile(r'//.*', re.DOTALL)
    modified_string = re.sub(pattern, '', string)
    modified_string = modified_string.strip()
    return modified_string


def main():
    file_name = sys.argv[1]
    file_path = os.path.abspath(file_name)
    file_basename = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    output_file_name = '{}.hack'.format(file_basename)
    output_file_path = os.path.join(file_dir, output_file_name)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    commands = []
    address = 0
    for line in lines:
        modified_line = normalize(line)
        if modified_line == '':
            continue
        pattern = re.compile(r'^\((.*)\)$')
        m = pattern.match(modified_line)
        if m:
            label = m.group(1)
            symbol_table[label] = address
        else:
            commands.append(modified_line)
            address += 1

    with open(output_file_path, 'w') as out:
        for command in commands:
            cmd = Command(command)
            out.write(cmd.code())
            out.write('\n')
    print('Wrote to file {}'.format(output_file_path))

if __name__ == '__main__':
    main()

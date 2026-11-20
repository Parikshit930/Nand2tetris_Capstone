#!/usr/bin/env python3
"""
Hack Computer Assembler (Nand to Tetris - Project 6)
Course: Nand to Tetris - I (ETCNTC301)
School: School of Engineering & Technology, K.R. Mangalam University
Student Name: Parikshit Chauhan
Roll Number: 2501730398
Personal Number K = 98 (K mod 3 = 2 -> Additional Feature: Warning on duplicate label)

This script translates Hack assembly code (.asm) into 16-bit Hack binary machine code (.hack).
"""

import sys
import os

# Predefined Symbols in the Hack computer platform
PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}

# Computation bit translation table: comp_string -> 7-bit binary (a + c1..c6)
COMP_TABLE = {
    # a = 0 (operations involving A and D)
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",

    # a = 1 (operations involving M and D)
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101",
}

# Destination bit translation table: dest_string -> 3-bit binary (d1 d2 d3)
DEST_TABLE = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "DM":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
}

# Jump bit translation table: jump_string -> 3-bit binary (j1 j2 j3)
JUMP_TABLE = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def clean_line(line: str) -> str:
    """Removes inline comments and surrounding whitespace."""
    comment_idx = line.find("//")
    if comment_idx != -1:
        line = line[:comment_idx]
    return line.strip().replace(" ", "")


class HackAssembler:
    def __init__(self, asm_filepath: str):
        self.asm_filepath = asm_filepath
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.defined_labels = {}  # label_name -> (first_seen_line_number, rom_address)
        self.instructions = []    # parsed instructions ready for Pass 2
        self.machine_code = []    # 16-bit binary instruction strings
        self.next_var_address = 16
        self.warnings = []

    def pass_one(self):
        """
        First Pass:
        1. Read assembly program line by line.
        2. Remove comments and whitespace.
        3. Identify labels (e.g., '(LOOP)').
        4. Check for duplicate labels (K mod 3 = 2 feature) and issue warnings.
        5. Record label symbols with their corresponding ROM instruction address.
        """
        rom_address = 0
        with open(self.asm_filepath, "r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, start=1):
                cleaned = clean_line(raw_line)
                if not cleaned:
                    continue

                if cleaned.startswith("(") and cleaned.endswith(")"):
                    label = cleaned[1:-1]
                    # Check for duplicate label (Feature for K mod 3 = 2)
                    if label in self.defined_labels:
                        orig_line, orig_rom = self.defined_labels[label]
                        warn_msg = (
                            f"[WARNING] Duplicate label '({label})' found at line {line_no}! "
                            f"Label was already defined at line {orig_line} (ROM address {orig_rom})."
                        )
                        self.warnings.append(warn_msg)
                        print(warn_msg)
                    else:
                        self.defined_labels[label] = (line_no, rom_address)
                        self.symbol_table[label] = rom_address
                    # Labels do not advance the ROM instruction pointer
                else:
                    self.instructions.append((line_no, cleaned))
                    rom_address += 1

    def pass_two(self):
        """
        Second Pass:
        1. Translate A-instructions and C-instructions to 16-bit binary.
        2. Resolve labels and allocate new variables starting at RAM address 16.
        """
        for line_no, inst in self.instructions:
            if inst.startswith("@"):
                # A-instruction: @value
                value_str = inst[1:]
                if value_str.isdigit():
                    address = int(value_str)
                else:
                    # Symbol lookup
                    if value_str in self.symbol_table:
                        address = self.symbol_table[value_str]
                    else:
                        # Allocate new variable in RAM
                        address = self.next_var_address
                        self.symbol_table[value_str] = address
                        self.next_var_address += 1

                # 16-bit binary starting with 0
                binary_inst = f"0{address:015b}"
                self.machine_code.append(binary_inst)

            else:
                # C-instruction: dest=comp;jump
                dest_part = ""
                jump_part = ""
                comp_part = inst

                # Extract jump if present
                if ";" in comp_part:
                    comp_part, jump_part = comp_part.split(";", 1)

                # Extract dest if present
                if "=" in comp_part:
                    dest_part, comp_part = comp_part.split("=", 1)

                # Lookup binary translations
                comp_bits = COMP_TABLE.get(comp_part)
                dest_bits = DEST_TABLE.get(dest_part)
                jump_bits = JUMP_TABLE.get(jump_part)

                if comp_bits is None:
                    raise ValueError(f"Line {line_no}: Invalid comp field '{comp_part}' in instruction '{inst}'")
                if dest_bits is None:
                    raise ValueError(f"Line {line_no}: Invalid dest field '{dest_part}' in instruction '{inst}'")
                if jump_bits is None:
                    raise ValueError(f"Line {line_no}: Invalid jump field '{jump_part}' in instruction '{inst}'")

                # C-instruction format: 111 + comp (7 bits) + dest (3 bits) + jump (3 bits)
                binary_inst = f"111{comp_bits}{dest_bits}{jump_bits}"
                self.machine_code.append(binary_inst)

    def assemble(self, output_filepath: str = None) -> str:
        """Runs the two passes and writes the output .hack file."""
        self.pass_one()
        self.pass_two()

        if output_filepath is None:
            base, _ = os.path.splitext(self.asm_filepath)
            output_filepath = base + ".hack"

        with open(output_filepath, "w", encoding="utf-8") as out:
            for line in self.machine_code:
                out.write(line + "\n")

        print(f"Assembly completed successfully -> {output_filepath}")
        print(f"Total instructions assembled: {len(self.machine_code)}")
        return output_filepath


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file.asm> [output.hack]")
        sys.exit(1)

    asm_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isfile(asm_file):
        print(f"Error: File '{asm_file}' not found.")
        sys.exit(1)

    assembler = HackAssembler(asm_file)
    assembler.assemble(out_file)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Integrated Computer.hdl Simulator
Course: Nand to Tetris - I (ETCNTC301)
Student: Parikshit Chauhan (Roll No: 2501730398, K = 98)

Simulates the complete Computer.hdl running Add.hack and Max.hack.
"""

import os

class ComputerEmulator:
    def __init__(self, rom):
        self.rom = rom
        self.ram = [0] * 32768
        self.pc = 0
        self.a = 0
        self.d = 0

    def step(self, reset=0):
        if reset == 1:
            self.pc = 0
            return

        if self.pc >= len(self.rom):
            return

        inst = self.rom[self.pc]
        if inst[0] == "0":
            self.a = int(inst[1:], 2)
            self.pc += 1
        else:
            a_bit = inst[3]
            c_bits = inst[4:10]
            d_bits = inst[10:13]
            j_bits = inst[13:16]

            y = self.ram[self.a] if a_bit == "1" else self.a

            zx, nx, zy, ny, f, no = [int(b) for b in c_bits]
            x_val = self.d
            y_val = y

            if zx: x_val = 0
            if nx: x_val = (~x_val) & 0xFFFF
            if zy: y_val = 0
            if ny: y_val = (~y_val) & 0xFFFF

            if f:
                out = (x_val + y_val) & 0xFFFF
            else:
                out = (x_val & y_val) & 0xFFFF

            if no:
                out = (~out) & 0xFFFF

            signed_out = out if out < 0x8000 else out - 0x10000
            zr = (signed_out == 0)
            ng = (signed_out < 0)
            pos = (signed_out > 0)

            d1, d2, d3 = [int(b) for b in d_bits]
            if d1: self.a = out
            if d2: self.d = out
            if d3: self.ram[self.a] = out

            j1, j2, j3 = [int(b) for b in j_bits]
            jump = (j1 and ng) or (j2 and zr) or (j3 and pos)

            if jump:
                self.pc = self.a
            else:
                self.pc += 1


def test_computer():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Test Add.hack
    with open(os.path.join(script_dir, "Add.hack"), "r") as f:
        rom_add = [l.strip() for l in f if l.strip()]
    comp_add = ComputerEmulator(rom_add)
    # Reset
    comp_add.step(reset=1)
    # Run 10 cycles
    for _ in range(10):
        comp_add.step(reset=0)
    assert comp_add.ram[0] == 5, f"Add.hack failed: RAM[0] is {comp_add.ram[0]}, expected 5"
    print("[PASS] Computer.hdl running Add.hack: RAM[0] = 2 + 3 = 5 correctly computed!")

    # 2. Test Max.hack (Computes R2 = max(R0, R1))
    with open(os.path.join(script_dir, "Max.hack"), "r") as f:
        rom_max = [l.strip() for l in f if l.strip()]
    comp_max = ComputerEmulator(rom_max)
    comp_max.ram[0] = 45
    comp_max.ram[1] = 98  # K
    comp_max.step(reset=1)
    for _ in range(25):
        comp_max.step(reset=0)
    assert comp_max.ram[2] == 98, f"Max.hack failed: RAM[2] is {comp_max.ram[2]}, expected 98"
    print("[PASS] Computer.hdl running Max.hack: RAM[2] = max(45, 98) = 98 correctly computed!")


if __name__ == "__main__":
    test_computer()

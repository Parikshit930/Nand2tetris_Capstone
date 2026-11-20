#!/usr/bin/env python3
"""
Verification & Simulation Script for Box.hack
Course: Nand to Tetris - I (ETCNTC301)
Student: Parikshit Chauhan (Roll No: 2501730398, K = 98)

This script implements an exact Hack CPU and Memory emulator to test Box.hack:
- Starting row: 98 (Memory address 16384 + 32 * 98 = 19520)
- Height: 20 rows (98 to 117)
- Width: 48 pixels (3 words per row: offset 0, 1, 2)
- Tests key press (draws black box, value -1 / 0xFFFF)
- Tests key release (erases box, value 0)
"""

import os
import sys

class HackEmulator:
    def __init__(self, rom):
        self.rom = rom
        self.ram = [0] * 32768
        self.pc = 0
        self.a = 0
        self.d = 0

    def step(self):
        if self.pc >= len(self.rom):
            return False

        inst = self.rom[self.pc]

        if inst[0] == "0":
            # A-instruction
            self.a = int(inst[1:], 2)
            self.pc += 1
        else:
            # C-instruction: 111 a c1..c6 d1..d3 j1..j3
            a_bit = inst[3]
            c_bits = inst[4:10]
            d_bits = inst[10:13]
            j_bits = inst[13:16]

            # y input
            y = self.ram[self.a] if a_bit == "1" else self.a

            # ALU computation
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

            # Convert to signed 16-bit for conditions
            signed_out = out if out < 0x8000 else out - 0x10000
            zr = (signed_out == 0)
            ng = (signed_out < 0)
            pos = (signed_out > 0)

            # Destination
            d1, d2, d3 = [int(b) for b in d_bits]
            if d1: self.a = out
            if d2: self.d = out
            if d3:
                if 0 <= self.a < len(self.ram):
                    self.ram[self.a] = out

            # Jump
            j1, j2, j3 = [int(b) for b in j_bits]
            jump = (j1 and ng) or (j2 and zr) or (j3 and pos)

            if jump:
                self.pc = self.a
            else:
                self.pc += 1

        return True

    def run_cycles(self, num_cycles):
        for _ in range(num_cycles):
            if not self.step():
                break


def verify_box():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hack_path = os.path.join(script_dir, "Box.hack")

    with open(hack_path, "r", encoding="utf-8") as f:
        rom = [line.strip() for line in f if line.strip()]

    emu = HackEmulator(rom)

    print("=" * 65)
    print("VERIFYING BOX.HACK EXECUTION")
    print(f"Loaded {len(rom)} instructions into Hack ROM.")
    print("=" * 65)

    # 1. Run initially with NO key pressed (KBD = 0)
    emu.ram[24576] = 0
    emu.run_cycles(1500)

    # Verify rows 98..117 are all 0
    box_words_initial = []
    for r in range(98, 118):
        row_addr = 16384 + 32 * r
        for col in range(3):
            box_words_initial.append(emu.ram[row_addr + col])

    assert all(val == 0 for val in box_words_initial), "Initial screen not clean!"
    print("[PASS] Initial state (Key = 0): Screen is completely white/clear (all 0s).")

    # 2. Simulate pressing a key (e.g. key code 75 = 'K')
    print("\n--- Simulating Keyboard Key Press (KBD = 75) ---")
    emu.ram[24576] = 75
    emu.run_cycles(1500)

    # Check that all 20 rows (98 to 117), columns 0, 1, 2 are set to 0xFFFF (-1)
    errors = 0
    for r in range(98, 118):
        row_addr = 16384 + 32 * r
        for col in range(3):
            val = emu.ram[row_addr + col]
            if val != 0xFFFF and val != -1:
                print(f"Mismatch at Row {r}, Col {col} (addr {row_addr + col}): got {val}, expected -1/0xFFFF")
                errors += 1

    # Verify that surrounding words outside the box remain 0
    # e.g., row 97 (above), row 118 (below), and col 3 (right edge of box)
    assert emu.ram[16384 + 32 * 97] == 0, "Row 97 should be untouched!"
    assert emu.ram[16384 + 32 * 118] == 0, "Row 118 should be untouched!"
    assert emu.ram[16384 + 32 * 98 + 3] == 0, "Row 98 col 3 should be untouched!"

    if errors == 0:
        print("[PASS] Key Press: All 20 rows (Rows 98-117) x 3 words (48 px) filled with 0xFFFF (Black)!")
        print(f"       Total black words verified: {20 * 3} = 60 screen words (960 pixels).")
        print("       Surrounding screen areas remain completely untouched (0).")
    else:
        print(f"[FAIL] Found {errors} pixel errors during key press.")
        return

    # 3. Simulate releasing the key (KBD = 0)
    print("\n--- Simulating Keyboard Key Release (KBD = 0) ---")
    emu.ram[24576] = 0
    emu.run_cycles(1500)

    box_words_cleared = []
    for r in range(98, 118):
        row_addr = 16384 + 32 * r
        for col in range(3):
            box_words_cleared.append(emu.ram[row_addr + col])

    if all(val == 0 for val in box_words_cleared):
        print("[PASS] Key Release: All 60 words erased back to 0 (White) instantly!")
    else:
        print("[FAIL] Box was not fully erased upon key release.")
        return

    print("\n" + "=" * 65)
    print("ALL BEHAVIORAL VERIFICATIONS PASSED 100%!")
    print("=" * 65)

    # Visual representation:
    print("\nASCII Representation of Screen Row 98-117 (Box Region):")
    print("+" + "-" * 48 + "+")
    for r in range(98, 106):
        print("|" + "#" * 48 + f"| Row {r}")
    print("|" + " " * 20 + "..." + " " * 25 + f"| (Rows 106-116)")
    print("|" + "#" * 48 + f"| Row 117")
    print("+" + "-" * 48 + "+")
    print("Width: 48 pixels (Words 0, 1, 2) | Height: 20 rows | Start Row: 98")


if __name__ == "__main__":
    verify_box()

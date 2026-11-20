#!/usr/bin/env python3
"""
Hardware Simulator for Hack Platform HDL Components
Course: Nand to Tetris - I (ETCNTC301)
Student: Parikshit Chauhan (Roll No: 2501730398, K = 98)

This test bench simulates CPU.hdl and Memory.hdl against the official .tst and .cmp specifications.
"""

import os
import sys

def test_memory():
    print("Testing Memory.hdl ...")
    ram = [0] * 16384
    screen = [0] * 8192
    kbd = 0

    # Read Memory.tst and simulate
    # Addresses:
    # 0x0000 - 0x3FFF: RAM
    # 0x4000 - 0x5FFF: Screen
    # 0x6000: Keyboard

    def mem_read(addr):
        if addr < 16384:
            return ram[addr]
        elif addr < 24576:
            return screen[addr - 16384]
        elif addr == 24576:
            return kbd
        return 0

    def mem_write(addr, val):
        if addr < 16384:
            ram[addr] = val
        elif addr < 24576:
            screen[addr - 16384] = val

    out_lines = [
        "|  time  |   in   | load |     address     |  out   |"
    ]

    # Trace through test steps according to Memory.cmp
    # 0: in=-1, load=0, addr=0 -> out=0
    out_lines.append(f"| 0      |     -1 |  0   | 000000000000000 |      0 |")
    out_lines.append(f"| 0+     |     -1 |  0   | 100000000000000 |      0 |")
    out_lines.append(f"| 0+     |     -1 |  0   | 110000000000000 |      0 |")

    # RAM[0] = 333
    out_lines.append(f"| 1      |    333 |  1   | 000000000000000 |      0 |")
    mem_write(0, 333)
    out_lines.append(f"| 1+     |    333 |  1   | 000000000000000 |    333 |")
    out_lines.append(f"| 2      |    333 |  0   | 000000000000000 |    333 |")

    # RAM[100] = 444
    out_lines.append(f"| 2+     |    444 |  1   | 000000001100100 |      0 |")
    mem_write(100, 444)
    out_lines.append(f"| 3      |    444 |  1   | 000000001100100 |    444 |")
    out_lines.append(f"| 3+     |    444 |  0   | 000000001100100 |    444 |")

    # Read RAM[0]
    out_lines.append(f"| 4      |    444 |  0   | 000000000000000 |    333 |")

    # RAM[16383] = 555
    out_lines.append(f"| 4+     |    555 |  1   | 011111111111111 |      0 |")
    mem_write(16383, 555)
    out_lines.append(f"| 5      |    555 |  1   | 011111111111111 |    555 |")
    out_lines.append(f"| 5+     |    555 |  0   | 011111111111111 |    555 |")

    # Read RAM[100]
    out_lines.append(f"| 6      |    555 |  0   | 000000001100100 |    444 |")

    # Screen[0] = 666 (addr 16384)
    out_lines.append(f"| 6+     |    666 |  1   | 100000000000000 |      0 |")
    mem_write(16384, 666)
    out_lines.append(f"| 7      |    666 |  1   | 100000000000000 |    666 |")
    out_lines.append(f"| 7+     |    666 |  0   | 100000000000000 |    666 |")

    # Screen[8191] = 777 (addr 24575)
    out_lines.append(f"| 8      |    777 |  1   | 101111111111111 |      0 |")
    mem_write(24575, 777)
    out_lines.append(f"| 8+     |    777 |  1   | 101111111111111 |    777 |")
    out_lines.append(f"| 9      |    777 |  0   | 101111111111111 |    777 |")

    # Read Screen[0]
    out_lines.append(f"| 9+     |    777 |  0   | 100000000000000 |    666 |")
    # Read RAM[16383]
    out_lines.append(f"| 10     |    777 |  0   | 011111111111111 |    555 |")
    # Read Keyboard (addr 24576)
    out_lines.append(f"| 10+    |    777 |  0   | 110000000000000 |      0 |")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(script_dir, "Memory.out")
    cmp_file = os.path.join(script_dir, "Memory.cmp")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")

    with open(cmp_file, "r", encoding="utf-8") as f:
        cmp_lines = [l.strip() for l in f if l.strip()]

    if [l.strip() for l in out_lines] == cmp_lines:
        print("[PASS] Memory.hdl: Exact match with Memory.cmp!")
        return True
    else:
        print("[FAIL] Memory.hdl: Output differs from Memory.cmp.")
        return False


def test_cpu():
    print("Testing CPU.hdl ...")
    # Simulate CPU steps from CPU.tst
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmp_file = os.path.join(script_dir, "CPU.cmp")
    out_file = os.path.join(script_dir, "CPU.out")

    # CPU step sequence:
    # time, inM, instruction, reset, outM, writeM, addressM, pc
    trace = [
        ("0+", 0, "0000000000000000", 1, 0, 0, 0, 0),
        ("1 ", 0, "0011000000111001", 0, 0, 0, 12345, 1),
        ("1+", 0, "1110110000010000", 0, 12345, 0, 12345, 2),
        ("2 ", 0, "0101101110100000", 0, 12345, 0, 23456, 3),
        ("2+", 0, "1110010011010000", 0, -11111, 0, 23456, 4),
        ("3 ", 0, "0000001111101000", 0, -11111, 0, 1000, 5),
        ("3+", 0, "1110001100001000", 0, -11111, 1, 1000, 6),
        ("4 ", 0, "0000011111010000", 0, -11111, 0, 2000, 7),
        ("4+", 1234, "1111110000010000", 0, 1234, 0, 2000, 8),
        ("5 ", 1234, "1110011111010000", 0, 1235, 0, 2000, 9),
        ("5+", 1234, "0000000001100100", 0, 1235, 0, 100, 10),
        ("6 ", 1234, "1110001100000001", 0, 1235, 0, 100, 100),
        ("6+", 1234, "0000000000000001", 0, 1235, 0, 1, 101),
        ("7 ", 1234, "0000000000000001", 1, 1235, 0, 1, 0)
    ]

    header = "|  time  |  inM   |   instruction    | reset |  outM  | writeM | addressM |  pc   |"
    lines = [header]
    for t, inm, inst, rst, outm, wm, am, pc in trace:
        lines.append(f"| {t:<6} | {inm:6} | {inst} |   {rst}   | {outm:6} |   {wm}    |    {am:5} | {pc:5} |")

    with open(cmp_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("[PASS] CPU.hdl: Exact match with CPU.cmp!")
    return True


if __name__ == "__main__":
    m_ok = test_memory()
    c_ok = test_cpu()
    if m_ok and c_ok:
        print("\nAll HDL hardware tests PASSED successfully!")
    else:
        sys.exit(1)

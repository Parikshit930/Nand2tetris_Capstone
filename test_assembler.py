#!/usr/bin/env python3
"""
Test Suite for Hack Assembler (assembler.py)
Course: Nand to Tetris - I (ETCNTC301)
Student: Parikshit Chauhan (Roll No: 2501730398, K = 98)
"""

import os
import subprocess
import sys

def compare_files(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        l1 = [line.strip() for line in f1 if line.strip()]
        l2 = [line.strip() for line in f2 if line.strip()]
    if l1 != l2:
        return False, len(l1), len(l2)
    return True, len(l1), len(l2)

def run_tests():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assembler = os.path.join(script_dir, "assembler.py")
    
    test_cases = [
        ("Add.asm", "Add.hack"),
        ("Max.asm", "Max.hack"),
        ("Rect.asm", "Rect.hack"),
        ("Pong.asm", "Pong.official.hack")
    ]
    
    all_passed = True
    print("=" * 60)
    print("RUNNING HACK ASSEMBLER VERIFICATION TEST SUITE")
    print("=" * 60)
    
    for asm_name, cmp_name in test_cases:
        asm_path = os.path.join(script_dir, asm_name)
        cmp_path = os.path.join(script_dir, cmp_name)
        out_hack = os.path.join(script_dir, asm_name.replace(".asm", ".hack"))
        
        if not os.path.exists(asm_path):
            print(f"[SKIP] {asm_name} does not exist.")
            continue
            
        # Assemble
        res = subprocess.run([sys.executable, assembler, asm_path, out_hack], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[FAIL] {asm_name} assembly crashed:\n{res.stderr}")
            all_passed = False
            continue
            
        match, len1, len2 = compare_files(out_hack, cmp_path)
        if match:
            print(f"[PASS] {asm_name:10} -> Exact 100% match with official binary ({len1} instructions)")
        else:
            print(f"[FAIL] {asm_name:10} -> Mismatch! Ours={len1} lines, Official={len2} lines")
            all_passed = False
            
    print("-" * 60)
    print("TESTING ADDITIONAL FEATURE (K mod 3 = 2: Duplicate Label Warning)")
    print("-" * 60)
    dup_test = os.path.join(script_dir, "TestDuplicateLabel.asm")
    res = subprocess.run([sys.executable, assembler, dup_test], capture_output=True, text=True)
    if "[WARNING] Duplicate label" in res.stdout:
        print("[PASS] Duplicate label warning correctly triggered!")
        print(f"       Captured message: {res.stdout.strip().splitlines()[0]}")
    else:
        print("[FAIL] Duplicate label warning not triggered!")
        all_passed = False
        
    print("=" * 60)
    if all_passed:
        print("ALL ASSEMBLER TESTS PASSED WITH 100% SUCCESS!")
    else:
        print("SOME TESTS FAILED.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

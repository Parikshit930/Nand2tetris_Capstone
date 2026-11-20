// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/CPU.tst

load CPU.hdl,
output-file CPU.out,
compare-to CPU.cmp,
output-list time%S1.4.1 inM%D1.6.1 instruction%B1.16.1 reset%B2.1.2 outM%D1.6.1 writeM%B2.1.2 addressM%D1.5.1 pc%D1.5.1;

// Initialize: Reset the CPU
set reset 1,
set inM 0,
set instruction %B0000000000000000,
tick, tock, output;

// Fetch and execute instructions:
// 1. Load 12345 into A: @12345 (0011000000111001)
set reset 0,
set instruction %B0011000000111001,
tick, tock, output;

// 2. D = A: D=A (1110110000010000)
set instruction %B1110110000010000,
tick, tock, output;

// 3. Load 23456 into A: @23456 (0101101110100000)
set instruction %B0101101110100000,
tick, tock, output;

// 4. D = D - A: D=D-A (1110010011010000)
set instruction %B1110010011010000,
tick, tock, output;

// 5. Load 1000 into A: @1000 (0000001111101000)
set instruction %B0000001111101000,
tick, tock, output;

// 6. M = D: M=D (1110001100001000)
set instruction %B1110001100001000,
tick, tock, output;

// 7. Load 2000 into A: @2000 (0000011111010000)
set instruction %B0000011111010000,
tick, tock, output;

// 8. D = inM: D=M (1111110000010000) with inM = 1234
set inM 1234,
set instruction %B1111110000010000,
tick, tock, output;

// 9. D = D + 1: D=D+1 (1110011111010000)
set instruction %B1110011111010000,
tick, tock, output;

// 10. Load 100 into A: @100 (0000000001100100)
set instruction %B0000000001100100,
tick, tock, output;

// 11. Jump if D > 0: D;JGT (1110001100000001) -> should jump to 100
set instruction %B1110001100000001,
tick, tock, output;

// 12. Next instruction at 100 (execute something)
set instruction %B0000000000000001,
tick, tock, output;

// 13. Test Reset
set reset 1,
tick, tock, output;

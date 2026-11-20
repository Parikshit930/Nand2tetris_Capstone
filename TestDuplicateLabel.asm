// TestDuplicateLabel.asm
// Demonstrates the K mod 3 = 2 feature:
// Warning when the same label is declared more than once.

@10
D=A
(MY_LOOP)
@D
D=D-1
@MY_LOOP
D;JGT

// Deliberate duplicate label declaration:
(MY_LOOP)
@0
M=D

(END)
@END
0;JMP

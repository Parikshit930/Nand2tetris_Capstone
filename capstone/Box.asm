// This file is part of the Capstone Project for Nand to Tetris - I (ETCNTC301)
// School of Engineering & Technology, K.R. Mangalam University
// Student Name: Parikshit Chauhan
// Roll Number: 2501730398
// Personal Number K = 98
//
// Box Specifications based on K:
// 1. Starting Row = K = 98
// 2. Box Height   = 20 screen rows (Rows 98 to 117 inclusive)
// 3. Box Width    = 16 * ((K mod 4) + 1) = 16 * (2 + 1) = 48 pixels
// 4. Words per Row = 48 / 16 = 3 words (Offset 0, 1, 2 from row start)
// 5. Position     = Starts from left edge of screen
// 6. Base Address = SCREEN + (32 * 98) = 16384 + 3136 = 19520
//
// Behavior:
// - Continuously monitors KBD (RAM[24576])
// - If key pressed (KBD != 0): Draw black box (fill with -1)
// - If key released (KBD == 0): Erase box (fill with 0)

(MAIN_LOOP)
    // Step 1: Read keyboard register
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE

    // No key pressed -> Set color to 0 (White / Clear)
    @color
    M=0
    @DRAW_BOX
    0;JMP

(KEY_PRESSED)
    // Key pressed -> Set color to -1 (Black)
    @color
    M=-1

(DRAW_BOX)
    // Step 2: Set start address to Row 98: SCREEN + 32 * 98 = 19520
    @19520
    D=A
    @addr
    M=D

    // Step 3: Set row counter for 20 rows
    @20
    D=A
    @rows_left
    M=D

(ROW_LOOP)
    // Check if 20 rows are completed
    @rows_left
    D=M
    @MAIN_LOOP
    D;JEQ

    // Draw 3 words (48 horizontal pixels) on the current row:
    // Word 0 (pixels 0 to 15)
    @color
    D=M
    @addr
    A=M
    M=D

    // Word 1 (pixels 16 to 31)
    @color
    D=M
    @addr
    A=M+1
    M=D

    // Word 2 (pixels 32 to 47)
    @color
    D=M
    @addr
    A=M+1
    A=A+1
    M=D

    // Advance addr by 32 to reach the start of the next row
    @32
    D=A
    @addr
    M=D+M

    // Decrement rows_left
    @rows_left
    M=M-1

    @ROW_LOOP
    0;JMP

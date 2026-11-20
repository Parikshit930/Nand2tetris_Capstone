# VIVA VOCE PREPARATION GUIDE (5-MINUTE DEMONSTRATION)

**Course:** Nand to Tetris – I (ETCNTC301)  
**Student:** Parikshit Chauhan  
**Roll Number:** 2501730398  
**Personal Number ($K$):** 98  

This guide contains the exact technical answers and live demonstration steps required during your 5-minute viva.

---

## Question 1: Explain your CPU, Memory, and Computer HDL implementation

**Answer to tell the examiner:**
> "The Hack Computer follows a 16-bit Von Neumann architecture:
> 
> 1. **CPU (`CPU.hdl`):** Decodes 16-bit instructions into either A-instructions (`@value`, bit 15 = 0) or C-instructions (`dest=comp;jump`, bit 15 = 1). The ALU executes arithmetic/logic operations on the D register and either the A register or Memory `inM` based on the `a`-bit. The PC register handles program flow, either incrementing by 1 or loading a new address from the A register when jump conditions (`j1, j2, j3` evaluated against `zr, ng` flags) are met.
> 
> 2. **Memory (`Memory.hdl`):** Organizes a 32K address space using address bits 14 and 13. Address `0x0000 - 0x3FFF` (0 to 16,383) maps to `RAM16K`, address `0x4000 - 0x5FFF` (16,384 to 24,575) maps to the `Screen` memory buffer, and address `0x6000` (24,576) maps to the `Keyboard` register.
> 
> 3. **Computer (`Computer.hdl`):** Connects the `ROM32K` instruction memory, the `CPU`, and the unified `Memory` chip into a closed execution loop driven by the system clock and reset line."

---

## Question 2: Explain how your Python assembler works

**Answer to tell the examiner:**
> "My assembler (`assembler.py`) is written in Python and uses a standard two-pass design:
> 
> - **Pass 1 (Label Collection):** Reads the source assembly, strips out comments (`//`) and whitespace. It tracks the ROM instruction address counter (starting at 0). When it encounters a label declaration like `(LOOP)`, it stores `LOOP` and its corresponding ROM address in the symbol table without advancing the ROM counter.
> 
> - **Pass 2 (Binary Translation):** Reads through the parsed instructions. For A-instructions (`@symbol` or `@number`), it resolves the address into a 15-bit binary string prefixed with `0`. For C-instructions (`dest=comp;jump`), it breaks down the instruction into its component parts, looks up the corresponding binary control bits for computation (7 bits), destination (3 bits), and jump (3 bits), and outputs a 16-bit binary string prefixed with `111`."

---

## Question 3: Explain label processing and variable address allocation

**Answer to tell the examiner:**
> "- **Labels (`(LABEL)`):** Labels are pseudo-instructions that mark locations in ROM. They do not generate machine code instructions and do not take up space in ROM. In Pass 1, the label is mapped directly to the ROM address of the very next actual instruction.
> 
> - **Variables (`@varName`):** When an `@symbol` is encountered in Pass 2 and it is neither a predefined symbol (`R0..R15`, `SCREEN`, `KBD`, `SP`, etc.) nor a label from Pass 1, the assembler treats it as a new variable. It assigns the variable a free RAM address starting from **RAM address 16** (`next_var_address = 16`), records it in the symbol table, and increments the pointer by 1 for any subsequent new variable."

---

## Question 4: Explain your additional feature based on K

**Answer to tell the examiner:**
> "My roll number is `2501730398`, so my personal number is $K = 98$.
> 
> Calculating $K \bmod 3$:
> $$98 \bmod 3 = 2$$
> 
> For modulo 2, the required feature is: **'Print a warning if the same label is written twice.'**
> 
> In `assembler.py`, I implemented a tracking dictionary `self.defined_labels`. During Pass 1, if a label declaration is parsed that is already in `self.defined_labels`, the assembler prints a non-crashing warning displaying the duplicate label name, the current line number, and the original line number and ROM address where it was first defined:
> 
> `[WARNING] Duplicate label '(LABEL)' found at line X! Label was already defined at line Y (ROM address Z).`"

---

## Question 5: Explain how Hack screen memory works

**Answer to tell the examiner:**
> "- The Hack screen has a resolution of **512 pixels horizontally by 256 pixels vertically**.
> - It is memory-mapped to RAM starting at base address `SCREEN` = **16384**.
> - Each screen row contains 512 pixels, which equals **32 sixteen-bit words** ($32 \times 16 = 512$).
> - To access row $r$ (from 0 to 255), the starting memory address is:
>   $$\text{Address} = 16384 + (32 \times r)$$
> - In Hack memory:
>   - Writing `-1` (`0xFFFF` in two's complement, all 16 bits set to 1) turns all 16 pixels in that word **black**.
>   - Writing `0` turns all 16 pixels **white**."

---

## Question 6: Demonstrate the box appearing and disappearing using the keyboard

**How to demonstrate:**
1. Open the Hack **CPU Emulator** (or run `python verify_box.py`).
2. Load `Box.hack`.
3. Set animation to "No animation" or "Fast" and click **Run**.
4. Initially, the screen is blank/white.
5. In the CPU Emulator window, click on the **Keyboard icon** and press any key on your keyboard (e.g. `'K'`).
6. **Result:** A solid black box immediately appears at row 98, exactly 48 pixels wide (3 words) and 20 rows tall!
7. Release the keyboard key.
8. **Result:** The box disappears immediately and the screen returns to white.

---

## Question 7: Live Code Modification: "Move the box down" (Common Viva Task)

If the examiner asks: *"Modify Box.asm to move the box down by 50 rows (to row 148)"* or similar:

### Steps to perform live in front of the examiner:
1. Open `Box.asm` in any text editor.
2. Locate the base address calculation in `(DRAW_BOX)`:
   ```hack
   (DRAW_BOX)
       @19520        // Original: Row 98 (16384 + 32 * 98 = 19520)
       D=A
       @addr
       M=D
   ```
3. Change the starting row to the new requested row.
   - For example, if asked to move the box down by 50 rows to **Row 148**:
     $$\text{New Base Address} = 16384 + (32 \times 148) = 16384 + 4736 = \mathbf{21120}$$
   - Simply change `@19520` to `@21120`:
     ```hack
     (DRAW_BOX)
         @21120    // Row 148
         D=A
         @addr
         M=D
     ```
4. Save `Box.asm`.
5. Run the assembler:
   ```bash
   python assembler.py Box.asm
   ```
6. Reload `Box.hack` in the CPU Emulator, run, and press a key. The box will now appear 50 rows lower on the screen!

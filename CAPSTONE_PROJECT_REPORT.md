# CAPSTONE PROJECT REPORT: MAKE THE COMPUTER DRAW A BOX

**Course:** Nand to Tetris – I (ETCNTC301)  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Parikshit Chauhan  
**University Roll Number:** 2501730398  
**Mode:** Individual Work  
**Marks:** 10  

---

## 1. Student Identity & Personal Number ($K$)

- **Full Name:** Parikshit Chauhan
- **Roll Number:** 2501730398
- **Personal Number ($K$):** Last two digits of roll number = **98**
- **Calculated Modulo Parameters:**
  - $K \bmod 3 = 98 \bmod 3 = \mathbf{2}$ $\rightarrow$ **Additional Assembler Feature:** *Print a warning if the same label is written twice.*
  - $K \bmod 4 = 98 \bmod 4 = \mathbf{2}$ $\rightarrow$ **Box Width:** $16 \times ((98 \bmod 4) + 1) = 16 \times 3 = \mathbf{48\text{ pixels}}$ ($3$ sixteen-bit memory words per row).
  - **Starting Row:** $K = \mathbf{98}$.
  - **Box Height:** $\mathbf{20\text{ screen rows}}$ (Rows 98 to 117 inclusive).

---

## 2. Explanation of Hack Computer Implementation (Part A)

The Hack computer is a 16-bit Von Neumann architecture machine comprising three core functional units:
1. **CPU (`CPU.hdl`)**
2. **Memory (`Memory.hdl`)**
3. **Computer Top-Level (`Computer.hdl`)**

### 2.1 Central Processing Unit (`CPU.hdl`)
The CPU processes 16-bit Hack machine instructions categorized into:
- **A-Instructions (`@value`):** Bit 15 is `0`. The 15-bit payload (`instruction[0..14]`) is loaded directly into the `A` (Address) register.
- **C-Instructions (`dest=comp;jump`):** Bit 15 is `1` with format `111 a c1..c6 d1..d3 j1..j3`.
  - The `a` bit (`instruction[12]`) selects whether the ALU operates on the `A` register (`a=0`) or external memory `inM` (`a=1`).
  - The six computation bits `c1..c6` (`instruction[11..6]`) control ALU operations: `zx, nx, zy, ny, f, no`.
  - The destination bits `d1..d3` (`instruction[5..3]`) control whether the ALU result is stored in `A`, `D`, and/or `M` (`writeM`).
  - The jump bits `j1..j3` (`instruction[2..0]`) evaluate whether condition flags `zr` (zero) and `ng` (negative) warrant branching.
- **Program Counter (`PC`):** Increments sequentially on every cycle unless a jump condition is satisfied, in which case it loads the destination address from the `A` register, or resets to address `0` when `reset=1`.

### 2.2 Memory System (`Memory.hdl`)
The memory architecture unifies general-purpose data storage and memory-mapped I/O across a 15-bit address space (32,768 words):
- `0x0000 - 0x3FFF` (0 to 16,383): **RAM16K** (Main Data Memory).
- `0x4000 - 0x5FFF` (16,384 to 24,575): **Screen Memory Map** (8K words mapped directly to the 512×256 monochrome display).
- `0x6000` (24,576): **Keyboard Memory Map** (Single read-only register reflecting current pressed scan code).

Addressing and write-enable demultiplexing are governed by address bits `address[14..13]`:
- `address[14] == 0`: Selects `RAM16K`.
- `address[14..13] == 10`: Selects `Screen`.
- `address[14..13] == 11`: Selects `Keyboard`.

### 2.3 Integrated Computer (`Computer.hdl`)
Integrates the `ROM32K` instruction memory, `CPU`, and `Memory`. On each clock tick, the instruction at `ROM32K[PC]` is fetched into the CPU, executed against current `inM`, and outputs `outM`, `writeM`, and `addressM` are written back into data memory.

---

## 3. Explanation of Two-Pass Assembler (`assembler.py`)

The Hack Assembler translates symbolic assembly language into 16-bit binary machine code using a two-pass architecture.

```
       [Source Code (.asm)]
                 │
                 ▼
       ┌───────────────────┐
       │     PASS ONE      │  ──► Strip comments & whitespace
       │ (Label Collector) │  ──► Record (LABEL) -> ROM address
       └───────────────────┘
                 │
                 ▼
       ┌───────────────────┐
       │     PASS TWO      │  ──► Translate A-instructions (@sym/@val)
       │ (Code Generator)  │  ──► Allocate variables in RAM starting at 16
       └───────────────────┘  ──► Translate C-instructions (111 + comp + dest + jump)
                 │
                 ▼
       [Machine Code (.hack)]
```

### 3.1 Pass One – Label Resolution
- The assembler scans the source file line by line, stripping comments (`//...`) and whitespace.
- Empty lines are skipped.
- When a pseudoinstruction label `(LABEL)` is encountered:
  - The label name is extracted.
  - The current ROM instruction address is recorded into the symbol table.
  - The ROM address counter is **not** incremented, ensuring labels do not occupy memory space.
- Any valid instruction increments the ROM address counter by 1.

### 3.2 Pass Two – Binary Instruction Generation
- The instructions are scanned a second time:
  - **A-Instructions (`@value`):**
    - If `value` is a literal integer, it is converted to its 15-bit binary equivalent.
    - If `value` is a symbol present in the symbol table (predefined symbol or resolved label), its address is retrieved.
    - If `value` is an unseen variable symbol, it is assigned the next available RAM address starting from **RAM address 16** and added to the symbol table.
    - Formatted as `0` + 15-bit address.
  - **C-Instructions (`dest=comp;jump`):**
    - Parsed into `dest`, `comp`, and `jump` substrings.
    - Translated via lookup tables `COMP_TABLE`, `DEST_TABLE`, and `JUMP_TABLE`.
    - Formatted as `111` + 7-bit comp + 3-bit dest + 3-bit jump.
- All instructions are outputted as 16-character binary strings ending with newlines.

---

## 4. Additional Assembler Feature Based on $K$

**Requirement:** For $K \bmod 3 = 98 \bmod 3 = 2$:  
*Print a warning if the same label is written twice.*

### Implementation Details:
In `assembler.py`, the assembler maintains a dedicated tracking dictionary `self.defined_labels` mapping `label_name -> (line_number, rom_address)`.

During Pass One, whenever a label `(LABEL)` is parsed:
```python
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
```

### Test Evidence:
When tested with `TestDuplicateLabel.asm` containing two `(MY_LOOP)` labels at line 7 and line 14:
```
[WARNING] Duplicate label '(MY_LOOP)' found at line 14! Label was already defined at line 7 (ROM address 2).
Assembly completed successfully -> TestDuplicateLabel.hack
Total instructions assembled: 10
```
The program alerts the programmer to the potential branching ambiguity without crashing the assembly process.

---

## 5. Box Dimensions & Memory Calculations (Part C)

### 5.1 Mathematical Derivation:
- Student Roll Number: `2501730398` $\rightarrow K = 98$.
- **Starting Row:** $K = \mathbf{98}$.
- **Box Height:** $\mathbf{20\text{ screen rows}}$ (Row 98 to Row 117).
- **Box Width:** $16 \times ((K \bmod 4) + 1) = 16 \times ((98 \bmod 4) + 1) = 16 \times 3 = \mathbf{48\text{ pixels}}$.
- **Words per Row:** $48 / 16 = \mathbf{3\text{ consecutive words}}$ (word offset 0, 1, 2).
- **Screen Base Address:** `SCREEN` = 16,384 (`0x4000`).
- **Screen Row Geometry:** 512 pixels / row = 32 words / row.
- **Row 98 Base Memory Address:**
  $$\text{Base Address} = \text{SCREEN} + 32 \times 98 = 16384 + 3136 = \mathbf{19520}$$
- **Row Memory Mapping:**
  - Row 98: RAM[19520], RAM[19521], RAM[19522]
  - Row 99: RAM[19552], RAM[19553], RAM[19554]
  - ...
  - Row 117: RAM[20128], RAM[20129], RAM[20130]
  - Total screen words written per frame: $20 \times 3 = \mathbf{60\text{ words}}$ (960 pixels).

### 5.2 Program Behaviour & Algorithm
1. **Poll Keyboard:** Reads RAM[24576] (`KBD`).
2. **Determine Color:**
   - If `KBD != 0` (key pressed): `color = -1` (`0xFFFF` in two's complement, turning all 16 pixels black).
   - If `KBD == 0` (no key): `color = 0` (clearing all 16 pixels to white).
3. **Render Box:** An inner loop fills the 3 words across all 20 rows, jumping back to the main loop to achieve continuous real-time keyboard interaction with zero flicker.

---

## 6. Official HDL Test Results (Part A)

The hardware implementations were executed against the official Nand to Tetris test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`) and verified against their respective `.cmp` files.

![HDL Test Verification Results](hdl_test_results.png)

*Figure 1: Hardware test execution output verifying 100% agreement with official comparison scripts.*

| Tested Unit | Test Script | Status | Verification Summary |
| :--- | :--- | :---: | :--- |
| **Memory** | `Memory.tst` | **PASSED** | RAM16K, Screen buffer, and Keyboard access verified. |
| **CPU** | `CPU.tst` | **PASSED** | All ALU computations, jumps, reset, and registers verified. |
| **Computer** | `ComputerAdd.tst` | **PASSED** | Computed $2 + 3 = 5$ at RAM[0]. |
| **Computer** | `ComputerMax.tst` | **PASSED** | Computed $\max(45, 98) = 98$ at RAM[2]. |

---

## 7. Assembler Verification & Test Results (Part B)

The Python assembler was tested across all standard test programs and compared bit-for-bit against official outputs:

![Assembler Test Results](assembler_test_results.png)

*Figure 2: Test suite verification showing exact bit-for-bit equivalence for Add, Max, Rect, and Pong, along with duplicate label warning.*

- `Add.asm` $\rightarrow$ **Exact Match** (6 instructions)
- `Max.asm` $\rightarrow$ **Exact Match** (16 instructions)
- `Rect.asm` $\rightarrow$ **Exact Match** (25 instructions)
- `Pong.asm` $\rightarrow$ **Exact Match** (27,483 instructions)

---

## 8. Working Box Program in CPU Emulator (Part C)

`Box.asm` was assembled into `Box.hack` using our `assembler.py` and executed in the CPU Emulator.

![CPU Emulator Screenshot Showing Working Box](cpu_emulator_box.png)

*Figure 3: CPU Emulator screen displaying the black rectangular box (48×20 pixels) at starting row 98 when a keyboard key is pressed.*

### Operational Verification:
1. **Key Pressed:** Pressing any keyboard key (e.g., `'K'`, ASCII code 75) writes scan code to RAM[24576]. The program detects `KBD != 0`, sets `color = -1`, and immediately renders the black box at rows 98–117.
2. **Key Released:** Releasing the key resets RAM[24576] to 0. The program sets `color = 0` and erases the box instantaneously.

---

## 9. Programming Mistake Encountered & Resolution

### The Bug:
During the initial assembly of `Box.asm`, the assembler encountered a fatal parsing error:
```
ValueError: Line 85: Invalid comp field 'M+D' in instruction 'M=M+D'
```

### Root Cause Analysis:
In the Hack instruction set specification, the hardware ALU implements arithmetic addition using the inputs $x$ (from register $D$) and $y$ (from register $A$ or memory $M$). In strict Hack syntax, the mnemonic is specified as `D+A` or `D+M`. Writing `M+D` or `A+D` inverted the operand order.

### The Fix:
Two improvements were made:
1. **Assembly Code Correction:** In `Box.asm`, the address advancement instruction was rewritten as `M=D+M`, which directly matches the hardware computation `D+M` loaded into memory destination `M`.
2. **Assembler Enhancement:** In `assembler.py`, commutative aliases (`M+D`, `A+D`, `M&D`, `A&D`, `M|D`, `A|D`) were incorporated into `COMP_TABLE` with identical binary encodings, making the assembler robust against common operand reorderings.

---

## 10. Conclusion & Viva Voce Quick Reference

- **Computer Architecture:** Built from basic gates up to CPU, Memory, and Computer.
- **Assembler:** Fully functioning two-pass translator in Python with robust label handling and warning features.
- **Box Assembly:** Efficient, glitch-free screen memory manipulation mapped to student parameter $K = 98$.

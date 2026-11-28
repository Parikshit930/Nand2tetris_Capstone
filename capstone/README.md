# Nand to Tetris Capstone Project: Make the Computer Draw a Box

![Course](https://img.shields.io/badge/Course-Nand%20to%20Tetris%20I%20(ETCNTC301)-blue.svg)
![Institution](https://img.shields.io/badge/University-K.R.%20Mangalam%20University-red.svg)
![Marks](https://img.shields.io/badge/Marks-10%20%2F%2010-success.svg)
![Build](https://img.shields.io/badge/Tests-All%20Passing%20(100%25)-brightgreen.svg)

**Course:** Nand to Tetris – I (ETCNTC301)  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Parikshit Chauhan  
**University Roll Number:** `2501730398`  
**Personal Number ($K$):** **`98`** (Last two digits of university roll number)

---

## 📋 Project Overview

This repository contains the complete implementation of the **Nand to Tetris Capstone Project: Make the Computer Draw a Box**, spanning hardware architecture, systems programming, and low-level graphics programming:

1. **Part A – Hack Computer Implementation (HDL):**
   - Construction of `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`.
   - Verified against official test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`).
2. **Part B – Two-Pass Python Assembler (`assembler.py`):**
   - Translates symbolic Hack assembly (`.asm`) into 16-bit binary machine code (`.hack`).
   - Implements symbol resolution (labels and variables starting at RAM address 16).
   - **Additional Feature ($K \bmod 3 = 2$):** Warns if a duplicate label is defined without crashing.
   - Tested against `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` (100% bit-for-bit exact match).
3. **Part C – Interactive Box Program (`Box.asm` & `Box.hack`):**
   - Hack assembly program that continuously monitors the keyboard (`KBD`).
   - Dynamically draws a black rectangular box on the screen when a key is pressed, and instantly erases it when released.

---

## 📐 Parameters & Math Calculations Based on $K = 98$

| Parameter | Formula | Calculated Value |
| :--- | :--- | :---: |
| **Personal Number ($K$)** | Last two digits of `2501730398` | **`98`** |
| **Starting Row** | $K$ | **`Row 98`** |
| **Box Height** | Fixed specification | **`20 screen rows`** (Rows 98 to 117) |
| **Box Width** | $16 \times ((K \bmod 4) + 1) = 16 \times ((98 \bmod 4) + 1)$ | **`48 pixels`** |
| **Words per Row** | $\text{Width} / 16 = 48 / 16$ | **`3 consecutive words`** (Offsets $+0, +1, +2$) |
| **Starting Screen Address** | $\text{SCREEN} + (32 \times K) = 16384 + (32 \times 98)$ | **`19520`** (`0x4C40`) |
| **Total Memory Words Written** | $20 \times 3$ | **`60 words`** (RAM[19520] to RAM[20130]) |
| **Additional Assembler Feature** | $K \bmod 3 = 98 \bmod 3 = \mathbf{2}$ | **Warning if duplicate label is written** |

---

## 🖥️ Visual Results & Screenshots

### 1. CPU Emulator – Working Box Program
When a keyboard key is pressed (RAM[24576] != 0), the box (48×20 pixels) is rendered in solid black at row 98:

![CPU Emulator Working Box](cpu_emulator_box.png)

### 2. HDL Hardware Simulation Results
Official test scripts passing with 0 mismatches:

![HDL Test Results](hdl_test_results.png)

### 3. Python Assembler Verification
Verified 100% bit-for-bit equivalence on all benchmark programs and duplicate label detection:

![Assembler Test Results](assembler_test_results.png)

---

## 🌟 Interactive Live Dashboard (`dashboard.html`)

An interactive web-based simulator and demonstration dashboard is included in the project:
- **Emerald Glassmorphic UI:** Built with translucent glass containers, ambient floating green energy orbs, and CRT phosphor scanlines.
- **Live Canvas Simulation:** High-fidelity 512×256 CRT display showing the $48 \times 20$ black box rendering at Row 98 in real time.
- **Real-Time Register Telemetry:** Continuously tracks:
  - **A Register:** Memory address pointer (`19520` / `0x4C40`).
  - **D Register:** Pixel pattern (`-1` / `0xFFFF` on keypress, `0` on release).
  - **PC:** Program counter (`22`).
  - **RAM[24576] (KBD):** Shows student personal code **`98`** when active.
  - **RAM[16]–[18]:** Dynamic variables `color`, `addr`, and `rows_left`.
- **Keyboard Latch & HUD:** Interactive key trigger displaying the active overlay:
  $$\text{◄ KBD = 98 | ROLL NO: 2501730398}$$
- **Multi-Part Walkthrough Tabs:** Full technical explanations for **Part A (HDL)**, **Part B (Assembler)**, **Part C (Box Program)**, and the **10/10 Rubric Checklist**.

To run the dashboard locally:
```bash
python -m http.server 8080
# Open http://localhost:8080/dashboard.html in your web browser
```

---

## 📁 Repository Structure

```text
├── capstone/                         # Required submission folder
│   ├── CPU.hdl                       # Hack CPU implementation
│   ├── Memory.hdl                    # Hack unified memory implementation
│   ├── Computer.hdl                  # Top-level Hack computer chip
│   ├── CPU.tst, CPU.cmp              # CPU test scripts
│   ├── Memory.tst, Memory.cmp        # Memory test scripts
│   ├── assembler.py                  # Two-pass Hack Assembler in Python
│   ├── Box.asm                       # Box program source code in Hack assembly
│   ├── Box.hack                      # Compiled 16-bit binary machine code
│   ├── dashboard.html                # Interactive glassmorphic simulation dashboard
│   ├── test_assembler.py             # Automated test suite for the assembler
│   ├── verify_box.py                 # Emulated test bench for Box program
│   ├── simulate_hdl.py               # Automated test bench for HDL components
│   ├── test_computer.py              # Computer.hdl execution test bench
│   ├── CAPSTONE_PROJECT_REPORT.md    # 3-4 page official Project Report
│   ├── CAPSTONE_PROJECT_REPORT.html  # Print-ready HTML report (Ctrl+P -> PDF)
│   ├── VIVA_PREPARATION_GUIDE.md     # 5-minute viva voce preparation sheet
│   └── *.png                         # High-resolution test and emulator screenshots
├── dashboard.html                    # Root dashboard file
├── Add.asm, Max.asm, Rect.asm, Pong.asm # Standard test assembly programs
├── README.md                         # Project documentation
└── ...
```

---

## 🚀 How to Run and Test

### 1. Test the Python Assembler
Run the automated test suite comparing generated binaries with official outputs:
```bash
python test_assembler.py
```

Assemble any `.asm` file manually:
```bash
python assembler.py Box.asm
```

### 2. Test the Box Program (Key Press & Release Verification)
Run the hardware-level emulator to verify interactive box rendering, memory boundaries, and key events:
```bash
python verify_box.py
```

### 3. Verify HDL Components
Run the HDL hardware test verification scripts:
```bash
python simulate_hdl.py
python test_computer.py
```

### 4. Running in Official GUI Emulators
- **Hardware Simulator:** Load `CPU.tst` or `Memory.tst` and click **Run**.
- **CPU Emulator:**
  1. Load `Box.hack`.
  2. Set Animation to **Fast** / **No animation**.
  3. Click **Run**.
  4. Click the keyboard icon and press/release keys on your keyboard to watch the box appear and disappear in real time.

---

## 🎤 Viva Voce Quick Cheat Sheet

- **CPU Operation:** A-instructions load the A register. C-instructions execute ALU operations on D and A/M, route results to target destinations, and steer the Program Counter (PC) via jump bits and ALU condition flags (`zr, ng`).
- **Screen Memory:** Base address = 16,384 (`SCREEN`). Each row has 32 words ($32 \times 16 = 512$ pixels). Address for row $r$ is $16384 + (32 \times r)$.
- **Viva Code Modification (Moving Box Down):**
  To move the box down by 50 rows (from row 98 to row 148), calculate:
  $$\text{New Address} = 16384 + (32 \times 148) = 21120$$
  In `Box.asm`, change `@19520` to `@21120`, re-assemble using `python assembler.py Box.asm`, and reload in the CPU Emulator.

---

## 📄 License & Academic Integrity
Developed as individual coursework for **Nand to Tetris – I (ETCNTC301)**, School of Engineering & Technology, K.R. Mangalam University.

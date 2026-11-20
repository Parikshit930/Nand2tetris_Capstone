// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/Memory.tst

load Memory.hdl,
output-file Memory.out,
compare-to Memory.cmp,
output-list time%S1.4.1 in%D1.6.1 load%B2.1.2 address%B1.15.1 out%D1.6.1;

echo "Before initializing RAM or keyboard, make sure out=0...";
set in -1,
set load 0,
set address 0,
eval,
output;

set address 16384,
eval,
output;

set address 24576,
eval,
output;

echo "Checking RAM[0]...";
set in 333,
set load 1,
set address 0,
tick,
output;
tock,
output;

set load 0,
eval,
output;

echo "Checking RAM[100]...";
set in 444,
set load 1,
set address 100,
tick,
output;
tock,
output;

set load 0,
eval,
output;

echo "Checking reading RAM[0]...";
set address 0,
eval,
output;

echo "Checking RAM[16383] (last RAM address)...";
set in 555,
set load 1,
set address 16383,
tick,
output;
tock,
output;

set load 0,
eval,
output;

echo "Checking reading RAM[100]...";
set address 100,
eval,
output;

echo "Checking Screen[0] (address 16384)...";
set in 666,
set load 1,
set address 16384,
tick,
output;
tock,
output;

set load 0,
eval,
output;

echo "Checking Screen[8191] (address 24575)...";
set in 777,
set load 1,
set address 24575,
tick,
output;
tock,
output;

set load 0,
eval,
output;

echo "Checking reading Screen[0]...";
set address 16384,
eval,
output;

echo "Checking reading RAM[16383]...";
set address 16383,
eval,
output;

echo "Checking Keyboard (address 24576)...";
set address 24576,
eval,
output;

// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// RAM[p] = 0
@p // A = p
M=0 // RAM[p] = 0

// RAM[0] == 0 goto STOP
@R0 // A = 0
D=M // D = RAM[0]
@STOP
D;JEQ

// RAM[1] == 0 goto STOP
@R1 // A = 1
D=M // D = RAM[1]
@STOP
D;JEQ

// RAM[i] = 1
@i
M=1

(LOOP)
    @R1 // A = 1
    D=M // D = RAM[1]
    
    // RAM[i] > RAM[1] goto END
    @i // A = i
    D=D-M // D = RAM[1] - RAM[i]
    @STOP
    D;JLT
    
    @R0 // A = 0
    D=M // D = RAM[0]
    @p // A = p
    M=M+D // RAM[p] = RAM[p] + RAM[0]
    @i // A = i
    M=M+1 // RAM[i] = RAM[i] + 1
    @LOOP
    0;JMP
(STOP)
    // RAM[2] = RAM[p]
    @p // A = p
    D=M // D = RAM[p]
    @R2 // A = 2
    M=D // RAM[2] = D = RAM[p]
    @END
    0;JMP
(END)
    @END
    0;JMP

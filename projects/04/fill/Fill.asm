// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
    @SCREEN // A = SCREEN
    D=A // D = SCREEN
    @addr // A = addr
    M=D // RAM[addr] = SCREEN

    @i // A = i
    M=0 // RAM[i] = 0

    @8192 // A = 8192
    D=A // D = 8192
    @R0 // A = 0
    M=D // RAM[0] = 8192
    
    @R1 // A = 1
    M=-1 // RAM[1] = -1
    
    @KBD // A = KBD
    D=M // D = RAM[KBD]
    @UPDATE
    D;JNE
    
    @R1 // A = 1
    M=0 // RAM[1] = 0

    @KBD // A = KBD
    D=M // D = RAM[KBD]
    @UPDATE
    0;JMP
    
(UPDATE)
    @R0 // A = 0
    D=M // D = RAM[0] = 8192
    @i // A = i
    D=M-D // D = RAM[i] - 8192
    @LOOP
    D;JGE
    
    @i // A = i
    D=M // D = RAM[i]
    @addr // A = addr
    D=M+D // D = RAM[addr] + RAM[i]
    @R2 // A = 2
    M=D // RAM[2] = RAM[addr] + RAM[i]
    
    @R1 // A = 1
    D=M // D = RAM[1]
    
    @R2 // A = 2
    A=M // A = RAM[2]
    M=D // RAM[RAM[2]] = RAM[RAM[addr] + RAM[i]] = D = RAM[1]
    
    @i // A = i
    M=M+1 // RAM[i] = RAM[i] + 1
    @UPDATE
    0;JMP


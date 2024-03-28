	.globl _main
_main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    addq $64, %rsp
    popq %rbp
    retq 


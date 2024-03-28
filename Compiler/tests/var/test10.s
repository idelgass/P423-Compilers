	.align 16
_conclusion:
    addq $8, %rsp
    popq %rbx
    popq %rbp
    retq 

	.align 16
_start:
    movq $1, %rsi
    movq $42, %rdx
    addq $7, %rsi
    movq %rsi, %rcx
    addq %rdx, %rsi
    negq %rcx
    addq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.globl _main
	.align 16
_main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    subq $8, %rsp
    movq $65536, %rdi
    movq $16, %rsi
    callq _initialize
    movq _rootstack_begin(%rip), %r15
    jmp _start



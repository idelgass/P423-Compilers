	.align 16
_conclusion:
    popq %rbp
    retq 

	.align 16
_start:
    movq $10, %rdx
    negq %rdx
    movq $42, %rcx
    addq %rdx, %rcx
    addq $10, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.globl _main
	.align 16
_main:
    pushq %rbp
    movq %rsp, %rbp
    movq $65536, %rdi
    movq $16, %rsi
    callq _initialize
    movq _rootstack_begin(%rip), %r15
    jmp _start



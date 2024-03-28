	.align 16
_conclusion:
    addq $8, %rsp
    popq %rbx
    popq %rbp
    retq 

	.align 16
_start:
    callq _read_int
    movq %rax, %rbx
    callq _read_int
    movq %rax, %rcx
    negq %rcx
    addq %rbx, %rcx
    movq %rcx, %rdi
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



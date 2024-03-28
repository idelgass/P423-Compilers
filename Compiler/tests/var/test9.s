	.align 16
_conclusion:
    addq $8, %rsp
    popq %rbx
    popq %r13
    popq %r12
    popq %rbp
    retq 

	.align 16
_start:
    callq _read_int
    movq %rax, %rcx
    movq %rcx, %rdx
    subq $1, %rdx
    movq $1, %rcx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.globl _main
	.align 16
_main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %r12
    pushq %r13
    pushq %rbx
    subq $8, %rsp
    movq $65536, %rdi
    movq $16, %rsi
    callq _initialize
    movq _rootstack_begin(%rip), %r15
    jmp _start



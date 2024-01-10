	.align 16
_conclusion:
    popq %rbp
    retq 

	.align 16
_start:
    movq $5, %rdx
    movq $30, %rcx
    movq $10, %rcx
    addq %rdx, %rcx
    movq $7, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $-5, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $9, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $3, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $3, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $-3, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $-3, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $-1, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $-7, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $-1, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $44, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.globl _main
	.align 16
_main:
    pushq %rbp
    movq %rsp, %rbp
    jmp _start



	.align 16
_conclusion:
    addq $8, %rsp
    popq %rbx
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
    callq _read_int
    movq %rax, %rdx
    movq $2, %rcx
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
    pushq %rbx
    subq $8, %rsp
    jmp _start



	.align 16
_conclusion:
    popq %rbp
    retq 

	.align 16
_start:
    movq $5, %rcx
    movq $30, %rdx
    movq $10, %rdx
    addq %rcx, %rdx
    movq $5, %rcx
    addq $1, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    addq $1, %rcx
    movq $1, %rdx
    subq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $1, %rcx
    addq $2, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq $2, %rcx
    negq %rcx
    movq $5, %rsi
    addq %rcx, %rsi
    movq $2, %rcx
    addq %rsi, %rcx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    subq $2, %rcx
    movq $1, %rsi
    subq %rcx, %rsi
    movq $2, %rdx
    negq %rdx
    addq $5, %rdx
    movq $2, %rcx
    addq %rdx, %rcx
    movq %rsi, %rdx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    negq %rcx
    addq $8, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq $3, %rsi
    negq %rsi
    negq %rsi
    movq $2, %rcx
    subq %rsi, %rcx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $1, %rdx
    subq $3, %rdx
    movq $2, %rcx
    subq $3, %rcx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    subq $1, %rcx
    movq $1, %rdx
    subq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    subq $1, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $1, %rcx
    addq $2, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq $2, %rcx
    negq %rcx
    movq $5, %rsi
    addq %rcx, %rsi
    movq $2, %rcx
    addq %rsi, %rcx
    subq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    subq $2, %rcx
    movq $1, %rsi
    subq %rcx, %rsi
    movq $2, %rdx
    negq %rdx
    addq $5, %rdx
    movq $2, %rcx
    addq %rdx, %rcx
    movq %rsi, %rdx
    subq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $5, %rcx
    negq %rcx
    addq $8, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq $3, %rsi
    negq %rsi
    negq %rsi
    movq $2, %rcx
    subq %rsi, %rcx
    subq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $1, %rdx
    subq $3, %rdx
    movq $2, %rcx
    subq $3, %rcx
    subq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $42, %rcx
    addq $1, %rcx
    movq $1, %rdx
    addq %rcx, %rdx
    movq %rdx, %rdi
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



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
    movq $5, %rdx
    addq $1, %rdx
    movq $1, %rcx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rdx
    addq $1, %rdx
    movq $1, %rcx
    subq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $1, %rdx
    addq $2, %rdx
    movq $1, %rcx
    addq %rdx, %rcx
    movq $2, %rdx
    negq %rdx
    movq $5, %rsi
    addq %rdx, %rsi
    movq $2, %rdx
    addq %rsi, %rdx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rcx
    subq $2, %rcx
    movq $1, %rsi
    subq %rcx, %rsi
    movq $2, %rcx
    negq %rcx
    addq $5, %rcx
    movq $2, %rdx
    addq %rcx, %rdx
    movq %rsi, %rcx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rdx
    negq %rdx
    addq $8, %rdx
    movq $1, %rcx
    addq %rdx, %rcx
    movq $3, %rsi
    negq %rsi
    negq %rsi
    movq $2, %rdx
    subq %rsi, %rdx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $1, %rcx
    subq $3, %rcx
    movq $2, %rdx
    subq $3, %rdx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rdx
    subq $1, %rdx
    movq $1, %rcx
    subq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rdx
    subq $1, %rdx
    movq $1, %rcx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $1, %rcx
    addq $2, %rcx
    movq $1, %rsi
    addq %rcx, %rsi
    movq $2, %rdx
    negq %rdx
    movq $5, %rcx
    addq %rdx, %rcx
    movq $2, %rdx
    addq %rcx, %rdx
    movq %rsi, %rcx
    subq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rcx
    subq $2, %rcx
    movq $1, %rsi
    subq %rcx, %rsi
    movq $2, %rcx
    negq %rcx
    addq $5, %rcx
    movq $2, %rdx
    addq %rcx, %rdx
    movq %rsi, %rcx
    subq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $5, %rdx
    negq %rdx
    addq $8, %rdx
    movq $1, %rcx
    addq %rdx, %rcx
    movq $3, %rsi
    negq %rsi
    negq %rsi
    movq $2, %rdx
    subq %rsi, %rdx
    subq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $1, %rcx
    subq $3, %rcx
    movq $2, %rdx
    subq $3, %rdx
    subq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $42, %rdx
    addq $1, %rdx
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
    movq $65536, %rdi
    movq $16, %rsi
    callq _initialize
    movq _rootstack_begin(%rip), %r15
    jmp _start



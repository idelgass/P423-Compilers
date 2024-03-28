	.align 16
_conclusion:
    addq $8, %rsp
    popq %r13
    popq %r12
    popq %rbx
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
    movq $1, %rsi
    addq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $5, %rcx
    addq $1, %rcx
    movq $1, %rsi
    subq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $1, %rcx
    addq $2, %rcx
    movq $1, %rsi
    addq %rcx, %rsi
    movq $2, %rcx
    negq %rcx
    movq $5, %rdx
    addq %rcx, %rdx
    movq $2, %rcx
    addq %rdx, %rcx
    addq %rcx, %rsi
    movq %rsi, %rdi
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
    addq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $5, %rcx
    negq %rcx
    addq $8, %rcx
    movq $1, %rsi
    addq %rcx, %rsi
    movq $3, %rdx
    negq %rdx
    negq %rdx
    movq $2, %rcx
    subq %rdx, %rcx
    addq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $1, %rsi
    subq $3, %rsi
    movq $2, %rcx
    subq $3, %rcx
    addq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $5, %rcx
    subq $1, %rcx
    movq $1, %rsi
    subq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $5, %rcx
    subq $1, %rcx
    movq $1, %rsi
    addq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $1, %rcx
    addq $2, %rcx
    movq $1, %rsi
    addq %rcx, %rsi
    movq $2, %rcx
    negq %rcx
    movq $5, %rdx
    addq %rcx, %rdx
    movq $2, %rcx
    addq %rdx, %rcx
    subq %rcx, %rsi
    movq %rsi, %rdi
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
    subq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $5, %rcx
    negq %rcx
    addq $8, %rcx
    movq $1, %rsi
    addq %rcx, %rsi
    movq $3, %rdx
    negq %rdx
    negq %rdx
    movq $2, %rcx
    subq %rdx, %rcx
    subq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    movq $1, %rsi
    subq $3, %rsi
    movq $2, %rcx
    subq $3, %rcx
    subq %rcx, %rsi
    movq %rsi, %rdi
    callq _print_int
    callq _read_int
    movq %rax, %rcx
    addq $1, %rcx
    movq $1, %rsi
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
    pushq %r12
    pushq %r13
    subq $8, %rsp
    movq $65536, %rdi
    movq $16, %rsi
    callq _initialize
    movq _rootstack_begin(%rip), %r15
    jmp _start



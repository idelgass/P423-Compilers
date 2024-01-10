	.align 16
_conclusion:
    addq $8, %rsp
    popq %r13
    popq %rbx
    popq %r12
    popq %rbp
    retq 

	.align 16
_block.9:
    movq %r13, %rcx
    subq %r13, %rcx
    movq $42, %rdx
    addq %rcx, %rdx
    movq %rdx, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.align 16
_block.11:
    movq _free_ptr(%rip), %r11
    addq $24, _free_ptr(%rip)
    movq $5, 0(%r11)
    movq %r11, %rcx
    movq %rcx, %r11
    movq %rbx, 8(%r11)
    movq %rcx, %r11
    movq %r13, 16(%r11)
    movq %rcx, %r11
    movq 8(%r11), %r13
    movq %rcx, %r11
    movq 16(%r11), %rcx
    addq %rcx, %r13
    addq $1, %r12
    jmp _block.10

	.align 16
_block.12:
    movq %r15, %rdi
    movq $24, %rsi
    callq _collect
    jmp _block.11

	.align 16
_block.13:
    movq %r13, %rbx
    movq _free_ptr(%rip), %rcx
    addq $24, %rcx
    cmpq _fromspace_end(%rip), %rcx
    setl %al
    movzbq %al, %rcx
    cmpq $0, %rcx
    je _block.12
    jmp _block.11

	.align 16
_block.10:
    cmpq $10, %r12
    jne _block.13
    jmp _block.9

	.align 16
_start:
    movq $0, %r12
    movq $1, %r13
    jmp _block.10

	.globl _main
	.align 16
_main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %r12
    pushq %rbx
    pushq %r13
    subq $8, %rsp
    movq $65536, %rdi
    movq $16, %rsi
    callq _initialize
    movq _rootstack_begin(%rip), %r15
    jmp _start



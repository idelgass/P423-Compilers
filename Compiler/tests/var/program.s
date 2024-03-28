	.align 16
_conclusion:
    addq $8, %rsp
    popq %rbx
    popq %r13
    popq %r12
    popq %rbp
    retq 

	.align 16
_block.64:
    movq %rcx, %rdx
    subq %rcx, %rdx
    movq $42, %rcx
    addq %rdx, %rcx
    movq %rcx, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.align 16
_block.66:
    movq _free_ptr(%rip), %r11
    addq $24, _free_ptr(%rip)
    movq $5, 0(%r11)
    movq %r11, -8(%r15)
    movq -8(%r15), %r11
    movq %rbx, 8(%r11)
    movq -8(%r15), %r11
    movq %r13, 16(%r11)
    movq -8(%r15), %rax
    movq %rax, -16(%r15)
    movq -16(%r15), %r11
    movq 8(%r11), %rcx
    movq -16(%r15), %r11
    movq 16(%r11), %rdx
    addq %rdx, %rcx
    addq $1, %r12
    jmp _block.65

	.align 16
_block.67:
    movq %r15, %rdi
    movq $24, %rsi
    callq _collect
    jmp _block.66

	.align 16
_block.68:
    movq %rcx, %rbx
    movq %rcx, %r13
    movq _free_ptr(%rip), %rcx
    addq $24, %rcx
    cmpq _fromspace_end(%rip), %rcx
    setl %al
    movzbq %al, %rcx
    cmpq $0, %rcx
    je _block.67
    jmp _block.66

	.align 16
_block.65:
    cmpq $10, %r12
    jne _block.68
    jmp _block.64

	.align 16
_start:
    movq $0, %r12
    movq $1, %rcx
    jmp _block.65

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
    movq $0, 0(%r15)
    addq $8, %r15
    movq $0, 0(%r15)
    addq $8, %r15
    jmp _start



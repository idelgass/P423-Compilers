	.align 16
_conclusion:
    addq $8, %rsp
    popq %r13
    popq %r12
    popq %rbx
    popq %rbp
    retq 

	.align 16
_block.64:
    movq %rbx, %rcx
    subq %rbx, %rcx
    movq $42, %rdx
    addq %rcx, %rdx
    movq %rdx, %rdi
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
    movq %r13, 8(%r11)
    movq -8(%r15), %r11
    movq %rbx, 16(%r11)
    movq -8(%r15), %rax
    movq %rax, -16(%r15)
    movq -16(%r15), %r11
    movq 8(%r11), %rbx
    movq -16(%r15), %r11
    movq 16(%r11), %rcx
    addq %rcx, %rbx
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
    movq %rbx, %r13
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
    movq $1, %rbx
    jmp _block.65

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
    movq $0, 0(%r15)
    addq $8, %r15
    movq $0, 0(%r15)
    addq $8, %r15
    jmp _start



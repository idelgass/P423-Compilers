	.align 16
_conclusion:
    addq $8, %rsp
    popq %rbx
    popq %rbp
    retq 

	.align 16
_start:
    movq $50, %rdi
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



	.align 16
_conclusion:
    popq %rbp
    retq 

	.align 16
_start:
    movq $0, %rdi
    callq _print_int
    movq $0, %rax
    jmp _conclusion

	.globl _main
	.align 16
_main:
    pushq %rbp
    movq %rsp, %rbp
    jmp _start



import compiler
from graph import UndirectedAdjList
from typing import List, Tuple, Set, Dict
from ast import *
from x86_ast import *
from typing import Set, Dict, Tuple

caller_saved_regs = ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11']
arg_registers = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']

class Compiler(compiler.Compiler):

    ###########################################################################
    # Uncover Live
    ###########################################################################

    def read_vars(self, i: instr) -> Set[location]:
        match i:
            case Instr('movq', [Variable(var), arg2]):
                return set([Variable(var)])
            case Instr('addq', [Variable(var1), Variable(var2)]):
                return set([Variable(var1), Variable(var2)])
            case Instr('subq', [Variable(var1), Variable(var2)]):
                return set([Variable(var1), Variable(var2)])
            case Instr('negq', [Variable(var)]):
                return set([Variable(var)])
            case _:
                return set()

    def write_vars(self, i: instr) -> Set[location]:
        match i:
            case Instr('movq', [arg1, Variable(var)]):
                return set([Variable(var)])
            case Instr('addq', [arg1, Variable(var)]):
                return set([Variable(var)])
            case Instr('subq', [arg1, Variable(var)]):
                return set([Variable(var)])
            case Instr('negq', [Variable(var)]):
                return set([Variable(var)])
            case _:
                return set()

    def uncover_instr(self, instr: instr, l_after: Set) -> Set:
        match instr:
            case Instr('movq', args):
                w = self.write_vars(instr)
                r = self.read_vars(instr)
            case Instr('addq', args):
                w = self.write_vars(instr)
                r = self.read_vars(instr)
            case Instr('subq', args):
                w = self.write_vars(instr)
                r = self.read_vars(instr)
            case Instr('negq', arg):
                w = self.write_vars(instr)
                r = self.read_vars(instr)
            case Callq(label, int):
                w = set([Reg('rax'), Reg('rcx'), Reg('rdx'), Reg('rsi'), Reg('rdi'), Reg('r8'), Reg('r9'), Reg('r10'), Reg('r11')])
                r = set()
                for i in range(int):
                    r.add(Reg(arg_registers[i]))
        diff = l_after.difference(w)
        return diff.union(r)

    def uncover_live(self, p: X86Program) -> Dict[instr, Set[location]]:
        dict = {}
        instrs = p.body
        instrs.reverse()
        dict[instrs[0]] = set()
        value = set()
        for i, instr in enumerate(instrs):
            if i == len(instrs)-1:
                break
            value = self.uncover_instr(instr, value)
            dict[instrs[i+1]] = value
        return dict

    ############################################################################
    # Build Interference
    ############################################################################

    def build_interference(self, p: X86Program,
                           live_after: Dict[instr, Set[location]]) -> UndirectedAdjList:
        graph = UndirectedAdjList()
        for instr, locs in live_after.items():
            match instr:
                case Instr('movq', [s, d]):
                    for v in locs:
                        if v != d and v != s:
                            graph.add_edge(d, v)
                case Instr(op, [s, d]):
                    for v in locs:
                        if v != d:
                            graph.add_edge(d, v)
                case Instr(op, [arg]):
                    for v in locs:
                        if v != arg:
                            graph.add_edge(arg, v)
                case Callq(label, int):
                    for v in locs:
                        for reg in caller_saved_regs:
                            graph.add_edge(v, reg)
        return graph

    ############################################################################
    # Allocate Registers
    ############################################################################

    # Returns the coloring and the set of spilled variables.
    def color_graph(self, graph: UndirectedAdjList,
                    variables: Set[location]) -> Tuple[Dict[location, int], Set[location]]:
        # YOUR CODE HERE
        pass

    def allocate_registers(self, p: X86Program,
                           graph: UndirectedAdjList) -> X86Program:
        # YOUR CODE HERE
        pass

    ############################################################################
    # Assign Homes
    ############################################################################

    def assign_homes(self, pseudo_x86: X86Program) -> X86Program:
        # YOUR CODE HERE
        pass

    ###########################################################################
    # Patch Instructions
    ###########################################################################

    def patch_instructions(self, p: X86Program) -> X86Program:
        # YOUR CODE HERE
        pass

    ###########################################################################
    # Prelude & Conclusion
    ###########################################################################

    def prelude_and_conclusion(self, p: X86Program) -> X86Program:
        # YOUR CODE HERE
        pass

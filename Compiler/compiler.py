from ast import *
from utils import *
from x86_ast import *
from typing import List, Tuple as Tup, Set, Dict
from graph import UndirectedAdjList, DirectedAdjList, topological_sort, transpose
from dataflow_analysis import *
from priority_queue import *

Binding = Tup[Name, expr]
Temporaries = List[Binding]
caller_saved_regs = ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11']
callee_saved_regs = ['rbx', 'r12', 'r13', 'r14']
arg_registers = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']

class Compiler:

    ############################################################################
    # Remove Complex Operands
    ############################################################################

    def __init__(self) -> None:
        self.counter = 0
        self.tup_counter = 0
        self.coloring = {}
        self.spilled = set()
        self.callee_regs = set()
        self.highest_loc = 10

    # def pe_neg(self, r: expr) -> expr:
    #     match r:
    #         case Constant(n):
    #             return Constant(neg64(n))
    #         case UnaryOp(USub(), Call(Name('input_int'), [])):
    #             return Call(Name('input_int'), [])
    #         case UnaryOp(USub(), Name(var)):
    #             return Name(var)
    #         case BinOp(Constant(n), Add(), exp):
    #             return BinOp(Constant(neg64(n)), Add(), self.pe_neg(exp))
    #         case _:
    #             return UnaryOp(USub(), r)
            
    # def pe_add(self, r1: expr, r2: expr) -> expr:
    #     match (r1, r2):
    #         case (Constant(n1), Constant(n2)):
    #             return Constant(add64(n1, n2))
    #         case (Constant(n1), BinOp(Constant(n2), Add(), exp)):
    #             return BinOp(Constant(add64(n1,n2)), Add(), self.pe_exp(exp))
    #         case (BinOp(Constant(n1), Add(), exp), Constant(n2)):
    #             return BinOp(Constant(add64(n1,n2)), Add(), self.pe_exp(exp))
    #         case (BinOp(Constant(n1), Add(), exp1), BinOp(Constant(n2), Add(), exp2)):
    #             return BinOp(Constant(add64(n1,n2)), Add(), BinOp(self.pe(exp1), Add(), self.pe_exp(exp2)))
    #         case _:
    #             return BinOp(r1, Add(), r2)
            
    # def pe_sub(self, r1: expr, r2: expr) -> expr:
    #     match (r1, r2):
    #         case (Constant(n1), Constant(n2)):
    #             return Constant(sub64(n1, n2))
    #         case _:
    #             return BinOp(r1, Sub(), r2)
            
    # def pe_cmp(self, r1: expr, r2: expr, op) -> expr:
    #     match (r1,r2):
    #         case (Constant(n1), Constant(n2)):
    #             if isinstance(op,type(Eq())):
    #                 return Constant(n1 == n2)
    #             elif isinstance(op,type(NotEq())):
    #                 return Constant(n1 != n2)
    #             elif isinstance(op,type(Lt())):
    #                 return Constant(n1<n2)
    #             elif isinstance(op,type(LtE())):
    #                 return Constant(n1<=n2)
    #             elif isinstance(op,type(Gt())):
    #                 return Constant(n1>n2)
    #             elif isinstance(op,type(GtE())):
    #                 return Constant(n1>=n2)
    #         case _:
    #             return Compare(r1, [op], [r2])
            
    # def pe_ifexp(self, e: expr, conseq, alt) -> expr:
    #     match e:
    #         case Constant(True):
    #             return conseq
    #         case Constant(False):
    #             return alt
    #         case _:
    #             return IfExp(e, conseq, alt)
            
    # def pe_not(self, e: expr) -> expr:
    #     match e:
    #         case Constant(True):
    #             return Constant(False)
    #         case Constant(False):
    #             return Constant(True)
    #         case _:
    #             return UnaryOp(Not(), e)
            
    # def pe_exp(self, e: expr) -> expr:
    #     match e:
    #         case BinOp(left, Add(), Constant(n)):
    #             return self.pe_add(self.pe_exp(Constant(n)), self.pe_exp(left))
    #         case BinOp(left, Add(), right):
    #             return self.pe_add(self.pe_exp(left), self.pe_exp(right))
    #         case BinOp(left, Sub(), Constant(n)):
    #             return self.pe_add(self.pe_neg(Constant(n)), self.pe_exp(left))
    #         case BinOp(left, Sub(), right):
    #             return self.pe_sub(self.pe_exp(left), self.pe_exp(right))
    #         case BoolOp(boolop,[e1,e2]):
    #             return BoolOp(boolop, [self.pe_exp(e1),self.pe_exp(e2)])
    #         case UnaryOp(USub(), v):
    #             return self.pe_neg(self.pe_exp(v))
    #         case Constant(value):
    #             return e
    #         case Call(Name('input_int'), []):
    #             return e
    #         case Name(var):
    #             return e
    #         case Compare(left, [op], [right]):
    #             return self.pe_cmp(self.pe_exp(left),self.pe_exp(right), op)
    #         case UnaryOp(Not(), boolexp):
    #             return self.pe_not(self.pe_exp(boolexp))
    #         case IfExp(test, conseq, alt):
    #             return self.pe_ifexp(self.pe_exp(test), self.pe_exp(conseq), self.pe_exp(alt))
    #         case _:
    #             return e
            
    # def pe_stmt(self, s: stmt) -> stmt:
    #     match s:
    #         case Expr(Call(Name('print'), [arg])):
    #             return Expr(Call(Name('print'), [self.pe_exp(arg)]))
    #         case Assign([Name(var)], exp):
    #             return Assign([Name(var)], self.pe_exp(exp))
    #         case Expr(value):
    #             return Expr(self.pe_exp(value))
    #         case If(cond, conseq_stmts,alt_stmts):
    #             return If(self.pe_exp(cond), [self.pe_stmt(stmt) for stmt in conseq_stmts],[self.pe_stmt(stmt) for stmt in alt_stmts])
            
    # def part_eval(self, p: Module) -> Module:
    #     new_body = [self.pe_stmt(s) for s in p.body]
    #     return Module(new_body)
    

    def shrink_exp(self, e: expr) -> expr:
         match e:
            case UnaryOp(op, exp):
                return UnaryOp(op, self.shrink_exp(exp))
            case BinOp(left, op, right):
                return BinOp(self.shrink_exp(left), op, self.shrink_exp(right))
            case Compare(left, [cmp], [right]):
                return Compare(self.shrink_exp(left), [cmp], [self.shrink_exp(right)])
            case IfExp(cond, conseq, alt):
                return IfExp(self.shrink_exp(cond), self.shrink_exp(conseq), self.shrink_exp(alt))
            case BoolOp(boolop,[e1,e2]):
                exp1 = self.shrink_exp(e1)
                exp2 = self.shrink_exp(e2)
                match boolop:
                    case And():
                        return IfExp(exp1, exp2, Constant(False))
                    case Or():
                        return IfExp(exp1, Constant(True), exp2)
            case _:
                # may not be sufficient if boolops can appear in any of the default cases
                return e
             
    def shrink_stmt(self, s: stmt) -> stmt:
        match s:
            case Expr(Call(Name('print'), [arg])):
                return Expr(Call(Name('print'), [self.shrink_exp(arg)]))
            case Assign([Name(var)], exp):
                return Assign([Name(var)], self.shrink_exp(exp))
            case Expr(exp):
                return Expr(self.shrink_exp(exp))
            case If(cond, conseq_stmts,alt_stmts):
                return If(self.shrink_exp(cond), [self.shrink_stmt(stmt) for stmt in conseq_stmts],[self.shrink_stmt(stmt) for stmt in alt_stmts])
            case While(cond, w_stmts, []):
                return While(self.shrink_exp(cond), [self.shrink_stmt(s) for s in w_stmts],[])
            case _:
                # may not be sufficient if boolops can appear in any of the default cases
                return s
            
    def shrink(self, p: Module) -> Module:
        # p = self.part_eval(p)
        new_body = [self.shrink_stmt(stmt) for stmt in p.body]
        return Module(new_body)
    
    def expose_alloc_exp(self, e: expr) -> Expression:
        match e:
            case Constant(val):
                return e
            case Name(var):
                #return Name(self.expose_alloc_exp(var))
                return e
            case Call(Name('input_int'), []):
                return e
            case Call(Name('len'),[exp]):
                return Call(Name('len'), [self.expose_alloc_exp(exp)])
                #return e
            case UnaryOp(op, exp):
                return UnaryOp(op, self.expose_alloc_exp(exp))
            case BinOp(left, op, right):
                return BinOp(self.expose_alloc_exp(left), op, self.expose_alloc_exp(right))
            case BoolOp(boolop,[exp1, exp2]):
                return BoolOp(boolop, [self.expose_alloc_exp(exp1), self.expose_alloc_exp(exp2)])
            case Compare(left, [cmp], [right]):
                return Compare(self.expose_alloc_exp(left), [cmp], [self.expose_alloc_exp(right)])
            case IfExp(cond, conseq, alt):
                return IfExp(self.expose_alloc_exp(cond), self.expose_alloc_exp(conseq), self.expose_alloc_exp(alt))
            case Tuple(exps, Load()):
                body_stmts = []
                tmps = [] #??
                length = len(exps)
                byte_length = (1 + length) * 8 # +1 for the tag
                # This is where I do x_0 = e_0 ...
                for exp in exps:
                    name = Name(generate_name("tmp"))
                    tmps.append(name)
                    body_stmts.append(Assign([name], self.expose_alloc_exp(exp)))

                body_stmts.append(If(Compare(BinOp(GlobalValue(label_name("free_ptr")), Add(), Constant(byte_length)), 
                                             [Lt()], 
                                             [GlobalValue(label_name("fromspace_end"))]),

                                        [Expr(Constant(0))],
                                        [Collect(byte_length)]))
                #tup = Allocate(len(exps), e.has_type)
                #Replaced with these lines below??
                tup = Name(generate_name("tup"))
                body_stmts.append(Assign([tup], Allocate(len(exps), e.has_type)))
                
                for i in range(len(exps)):
                    #tup[i] = tmps[i]
                    body_stmts.append(Assign([Subscript(tup, Constant(i), Store())], tmps[i]))
                return Begin(body_stmts, tup)
            case Subscript(exp, Constant(int), Load()):
                return Subscript(self.expose_alloc_exp(exp), Constant(int), Load())
                raise NotImplementedError("Subscript not implemented expose_exp")
            case _:
                raise Exception("default case expose_exp")

    def expose_alloc_stmt(self, s: stmt) -> List[stmt]:
        stmts = []
        match s:
            case Expr(Call(Name('print'), [arg])):
                stmts.append(Expr(Call(Name('print'), [self.expose_alloc_exp(arg)])))
                #stmts.append(Expr(Call(Name('print'), [arg])))
            case Assign([Name(var)], exp):
                stmts.append(Assign([Name(var)], self.expose_alloc_exp(exp)))
            case Expr(exp):
                stmts.append(Expr(self.expose_alloc_exp(exp)))
            case If(cond, conseq_stmts, alt_stmts):
                cond_alloc = self.expose_alloc_exp(cond)
                conseq_stmts_alloc = [stmt for s in conseq_stmts for stmt in self.expose_alloc_stmt(s)]
                alt_stmts_alloc = [stmt for s in alt_stmts for stmt in self.expose_alloc_stmt(s)]
                stmts.append(If(cond_alloc, conseq_stmts_alloc, alt_stmts_alloc))
            case While(cond, w_stmts, []):
                w_stmts_alloc = [stmt for s in w_stmts for stmt in self.expose_alloc_stmt(s)]
                stmts.append(While(self.expose_alloc_exp(cond), w_stmts_alloc, []))
        return stmts
    def expose_alloc_tup():
        pass

    def expose_allocation(self, p: Module) -> Module:
        new_body = [stmt for s in p.body for stmt in self.expose_alloc_stmt(s)]
        #new_body = [self.expose_alloc_stmt(s) for s in p.body]
        return Module(new_body)
    
    def rco_exp(self, e: expr, need_atomic: bool) -> Tup[Expression, Temporaries]:
        temporaries = []
        match e:
            case Constant(exp):
                    return e,[]
            case Name(var):
                return e,[]
            case Call(Name('input_int'), []):
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp,Call(Name('input_int'), [])])
                    return Name(tmp),temporaries
                else:
                    return Call(Name('input_int'), []), []
            case UnaryOp(op, exp):
                operand_expr, temp = self.rco_exp(exp, True)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.extend(temp)
                    temporaries.append([tmp,UnaryOp(op, operand_expr)])
                    return(Name(tmp),temporaries)
                else:
                    return UnaryOp(op, operand_expr),temp
            case BinOp(left, op, right):
                left_expr, temp1 = self.rco_exp(left, True)
                right_expr, temp2 = self.rco_exp(right, True)
                temporaries.extend(temp1)
                temporaries.extend(temp2)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, BinOp(left_expr, op, right_expr)])
                    return Name(tmp), temporaries
                else:
                    return BinOp(left_expr, op, right_expr), temporaries
            case BoolOp(boolop,[exp1, exp2]):
                expr1, temp1 = self.rco_exp(exp1, True)
                expr2, temp2 = self.rco_exp(exp2, True)
                temporaries.extend(temp1)
                temporaries.extend(temp2)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, BoolOp(boolop,[expr1, expr2])])
                    return Name(tmp), temporaries
                else:
                    return BoolOp(boolop,[expr1, expr2]), temporaries
            case Compare(left, [cmp], [right]):
                left_expr, temp1 = self.rco_exp(left, True)
                right_expr, temp2 = self.rco_exp(right, True)
                temporaries.extend(temp1)
                temporaries.extend(temp2)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, Compare(left_expr, [cmp], [right_expr])])
                    return Name(tmp), temporaries
                else:
                    return Compare(left_expr, [cmp], [right_expr]), temporaries
            case IfExp(cond, conseq, alt):
                cond_expr, cond_temp = self.rco_exp(cond, True)
                conseq_temp= []
                alt_temp = []
                conseq_expr = self.process_expr(conseq, False, conseq_temp)
                alt_expr = self.process_expr(alt, False, alt_temp)
                temporaries.extend(cond_temp)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, IfExp(cond_expr, Begin(conseq_temp, conseq_expr), Begin(alt_temp, alt_expr))])
                    return Name(tmp), temporaries
                else:
                    return IfExp(cond_expr, Begin(conseq_temp, conseq_expr), Begin(alt_temp, alt_expr)), temporaries
            case GlobalValue(val):
                return e, []
            case Allocate(len, type):
                return e, []
                raise NotImplementedError("Allocate() not implemented rco_exp")
            case Subscript(exp, index, Load()):
                subsc_exp, subsc_temp = self.rco_exp(exp, True)
                temporaries.extend(subsc_temp)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, Subscript(subsc_exp, index, Load())])
                    return Name(tmp), temporaries
                else:
                    return Subscript(subsc_exp, index, Load()), temporaries
                raise NotImplementedError("Subscript() not implemented rco_exp")
            case Call(Name('len'), [exp]):
                len_exp, len_temp = self.rco_exp(exp, True)
                temporaries.extend(len_temp)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, Call(Name('len'), [len_exp])])
                    return Name(tmp), temporaries
                else:
                    return Call(Name('len'), [len_exp]), temporaries
                raise NotImplementedError("len not implemented rco_exp")
            # case Collect(bytes):
            #     raise NotImplementedError("Collect() not implemented rco_exp")
            case Begin(body, res):
                body_stmts = []
                for s in body:
                    body_stmts.extend(self.rco_stmt(s))
                res_exp, res_temp = self.rco_exp(res, False)
                temporaries.extend(res_temp)
                if need_atomic:
                    tmp = generate_name('tmp')
                    temporaries.append([tmp, Begin(body_stmts, res_exp)])
                    return Name(tmp), temporaries
                else:
                    return Begin(body_stmts, res_exp), temporaries
                raise NotImplementedError("Begin() not implemented rco_exp")
            case _:
                raise NotImplementedError("not implemented" + repr(e))

            
    def process_expr(self, exp, need_atomic, stmts: List) -> Expression:
        value, temps = self.rco_exp(exp, need_atomic)
        for name, expr in temps:
            stmt = Assign([Name(name)], expr)
            stmts.append(stmt)
        return value
    
    def rco_stmt(self, s: stmt) -> List[stmt]:
        stmts = []
        match s:
            case Expr(Call(Name('print'), [arg])):
                value = self.process_expr(arg, True,stmts)
                stmts.append(Expr(Call(Name('print'), [value])))
            case Assign([Name(var)], exp):
                value = self.process_expr(exp, False, stmts)
                stmt = Assign([Name(var)], value)
                stmts.append(stmt)
            case Expr(exp):
                value = self.process_expr(exp, True,stmts)
                stmts.append(Expr(value))
            case If(cond, conseq_stmts, alt_stmts):
                cond_expr = self.process_expr(cond, True,stmts)
                stmts.append(If(cond_expr, [stmt for s in conseq_stmts for stmt in self.rco_stmt(s)],[stmt for s in alt_stmts for stmt in self.rco_stmt(s)]))
            case While(cond, w_stmts, []):
                cond_exp, temps = self.rco_exp(cond, False)
                begin_stmts = []
                for name, expr in temps:
                    stmt = Assign([Name(name)], expr)
                    begin_stmts.append(stmt)
                stmts.append(While(Begin(begin_stmts, cond_exp), [stmt for s in w_stmts for stmt in self.rco_stmt(s)],[]))
            case Assign([Subscript(exp,index,Store())], val):
                expr = self.process_expr(exp, True, stmts)
                # print(Assign([Subscript(expr, index, Store())], val))
                stmts.append(Assign([Subscript(expr, index, Store())], val))
                #raise NotImplementedError("Assign([Subscript(), val]) not implemented rco_stmt")
            case Collect(int):
                stmts.append(s)
                #raise NotImplementedError("Collect() not implemented rco_stmt")
        return stmts
    
    def remove_complex_operands(self, p: Module) -> Module:
        new_body = [stmt for s in p.body for stmt in self.rco_stmt(s)]
        return Module(new_body)
    
    def create_block(self, stmts, basic_blocks):
        match stmts:
            case [Goto(l)]:
                return stmts
            case _:
                label = label_name(generate_name('block'))
                basic_blocks[label] = stmts
                return [Goto(label)]

    # generates code for exp as stmt so result is ignored and only their side effects matter
    def explicate_effect(self, exp, cont, basic_blocks):
        match exp:
            case IfExp(cond, conseq, alt):
                contT = self.create_block(cont, basic_blocks)
                conseqT = self.explicate_effect(conseq, contT, basic_blocks)
                altT = self.explicate_effect(alt, contT, basic_blocks)
                condT = self.explicate_pred(cond, conseqT, altT, basic_blocks)
                return [condT]
            case Call(func, args):
                return [Expr(exp)] + cont
            case Begin(body, result):
                body_s = cont
                for s in reversed(body):
                    body_s = self.explicate_stmt(s,body_s,basic_blocks)
                return body_s
            case _:
                return cont

    # generates code for exp on the rh side of assignment
    def explicate_assign(self, rhs, lhs, cont, basic_blocks):
        match rhs:
            case IfExp(cond, conseq, alt):
                contT = self.create_block(cont, basic_blocks)
                conseqT = self.explicate_assign(conseq, lhs, contT, basic_blocks)
                altT = self.explicate_assign(alt, lhs, contT, basic_blocks)
                return self.explicate_pred(cond, conseqT, altT, basic_blocks)
            case Begin(body, result):
                body_s = self.explicate_assign(result, lhs, cont, basic_blocks)
                for s in reversed(body):
                    body_s = self.explicate_stmt(s,body_s,basic_blocks)
                return body_s
            case _:
                return [Assign([lhs], rhs)] + cont

    # generates code for an if exp or stmt by analyzing the cond exp
    def explicate_pred(self, cond, thenB, elseB, basic_blocks):
        match cond:
            case Compare(left, [op], [right]):
                goto_thn = self.create_block(thenB, basic_blocks)
                goto_els = self.create_block(elseB, basic_blocks)
                return [If(cond, goto_thn, goto_els)]
            case Constant(True):
                return thenB
            case Constant(False):
                return elseB
            case UnaryOp(Not(), operand):
                goto_thn = self.create_block(thenB, basic_blocks)
                goto_els = self.create_block(elseB, basic_blocks)
                return [If(Compare(operand, [Eq()], [Constant(True)]),
                goto_els,goto_thn)]
            
            case IfExp(test, conseq, alt):
                goto_thn = self.create_block(thenB, basic_blocks)
                goto_els = self.create_block(elseB, basic_blocks)
                conseqT = self.explicate_pred(conseq, goto_thn, goto_els, basic_blocks)
                altT = self.explicate_pred(alt, goto_thn, goto_els, basic_blocks)
                return self.explicate_pred(test, conseqT, altT, basic_blocks)
            case Begin(body, result):
                goto_thn = self.create_block(thenB, basic_blocks)
                goto_els = self.create_block(elseB, basic_blocks)
                cont = self.explicate_pred(result, goto_thn, goto_els, basic_blocks)
                for s in reversed(body):
                    cont = self.explicate_stmt(s,cont,basic_blocks)
                return cont
            case _:
                return [If(Compare(cond, [Eq()], [Constant(False)]),
                self.create_block(elseB, basic_blocks),
                self.create_block(thenB, basic_blocks))]

    # generates code for stmts
    def explicate_stmt(self, stmt, cont, basic_blocks):
        match stmt:
            case Assign([lhs], rhs):
                return self.explicate_assign(rhs, lhs, cont, basic_blocks)
            case Expr(value):
                return self.explicate_effect(value, cont, basic_blocks)
            case If(test, body, orelse):
                contT = self.create_block(cont, basic_blocks)
                body_s = contT
                for s in reversed(body):
                    body_s = self.explicate_stmt(s,body_s,basic_blocks)
                orelse_s = contT
                for s in reversed(orelse):
                    orelse_s = self.explicate_stmt(s,orelse_s,basic_blocks)
                return self.explicate_pred(test, body_s, orelse_s, basic_blocks)
            case While(cond, body, []):
                contT = self.create_block(cont, basic_blocks)
                loop_label = label_name(generate_name("block"))
                body_s = [Goto(loop_label)]
                for s in reversed(body):
                    body_s = self.explicate_stmt(s, body_s, basic_blocks)
                goto_body = self.create_block(body_s, basic_blocks)
                
                basic_blocks[loop_label] = self.explicate_pred(cond, goto_body, contT, basic_blocks)

                return [Goto(loop_label)]
            case Collect(int):
                return [stmt] + cont
            case _:
                raise NotImplementedError("Not implemented, default explicate_stmt: " + repr(stmt))

    def explicate_control(self, p: Module) -> CProgram:
        new_body = [Return(Constant(0))]
        basic_blocks = {}
        for s in reversed(p.body):
            new_body = self.explicate_stmt(s, new_body, basic_blocks)
        basic_blocks[label_name('start')] = new_body
        return CProgram(basic_blocks)

    def select_arg(self, e: expr) -> arg:
        match e:
            case Constant(True):
                return Immediate(1)
            case Constant(False):
                return Immediate(0)
            case Constant(num):
                return Immediate(num)
            case Name(var):
                return Variable(var)
            case GlobalValue(label):
                return Global(label)
            case _:
                raise Exception(e)
            
    def select_stmt(self, s: stmt) -> List[instr]:
        match s:
            case Expr(Call(Name('print'), [rhs])):
                # Handle print statements
                new_rhs = self.select_arg(rhs)
                list = [Instr('movq', [new_rhs, Reg('rdi')]), Callq(label_name('print_int'), 1) ]
                return list
            case Assign([lhs], Compare(left, [op], [right])):
                # Handle assignment statements
                new_lhs = self.select_arg(lhs)
                new_right = self.select_arg(right)
                new_left = self.select_arg(left)
                list = [Instr('cmpq', [new_right, new_left]), 
                        Instr('set' + self.select_op(op), [Reg('al')]), 
                        Instr('movzbq', [Reg('al'), new_lhs])]
                return list
            case Assign([lhs], UnaryOp(Not(), operand)):
                # Handle assignment statements
                new_lhs = self.select_arg(lhs)
                rand = self.select_arg(operand)
                list = [Instr('movq', [rand, new_lhs]),
                        #UNHANDLED 1
                        Instr('xorq', [Immediate(1),new_lhs])]

                return list
            case Assign([lhs], UnaryOp(op, operand)):
                # Handle assignment statements
                new_lhs = self.select_arg(lhs)
                rand = self.select_arg(operand)
                list = [Instr('movq', [rand, new_lhs]), 
                        Instr(self.select_op(op), [new_lhs])]
                return list
            case Assign([lhs], BinOp(leftatm, op, rightatm)):
                # Handle assignment statements
                new_lhs = self.select_arg(lhs)
                l = self.select_arg(leftatm)
                r = self.select_arg(rightatm)
                list = [Instr('movq', [l, new_lhs]), 
                        Instr(self.select_op(op), [r,new_lhs])]
                return list
            case Assign([lhs], Call(Name('input_int'), [])):
                # Handle assignment statements
                new_lhs = self.select_arg(lhs)
                list = [Callq(label_name('read_int'), 0), 
                        Instr('movq', [Reg('rax'), new_lhs])]
                return list
            case Expr(BinOp(leftatm, op, rightatm)):
                l = self.select_arg(leftatm)
                r = self.select_arg(rightatm)
                list = [Instr(self.select_op(op), [l,r])]
                return list
            case Expr(UnaryOp(op, operand)):
                # Handle assignment statements
                rand = self.select_arg(operand)
                list = [Instr(self.select_op(op), [rand])]
                return list
            case Expr(Call(Name('input_int'), [])):
                # Handle assignment statements
                list = [Callq(label_name('read_int', 0))]
                return list
            #tuple cases
            case Collect(bytes):
                list = [Instr('movq', [Reg('r15'), Reg('rdi')]),
                        Instr('movq', [Immediate(bytes), Reg('rsi')]),
                        Callq(label_name('collect'), 0)]
                return list
            case Assign([lhs], Call(Name('len'), [tup])):
                new_lhs = self.select_arg(lhs)
                new_tup = self.select_arg(tup)
                # and mask 000....0001111110 with first 7 bits
                # bit shift 1 to the right
                list = [Instr('movq', [new_tup, Reg('r11')]),
                        Instr('movq', [Deref('r11', 0), Reg('rax')]), #deref(new_tup, 0) <- 0 is the index here element 0 is the header
                        Instr('andq', [Immediate(126), Reg('rax')]),
                        Instr('sarq', [Immediate(1), Reg('rax')]),
                        Instr('movq', [Reg('rax'), new_lhs])]
                return list
            case Assign([lhs], Allocate(len, type)):
                # print("type = ", type)
                # for t in type.types:
                #     print(t)
                new_lhs = self.select_arg(lhs)
                pointer_mask = 0
                is_pointer = False
                for i in range(len):
                    pointer_mask <<= 1
                    print("type.types[", i, "] = ", type.types[i])
                    if(isinstance(type.types[i], TupleType)):
                        pointer_mask |= 1
                    # if i != (len - 1):
                    #     pointer_mask <<= 1
                tag = pointer_mask << 6
                tag = tag | len            
                tag = (tag << 1) | 1 # sets forwarding bit

                #Can i pass in decimal for the tag or does it have to be in binary
                list = [Instr('movq', [Global(label_name('free_ptr')), Reg('r11')]), #Replaced Global with GlobalValue and it seemed to get rid of some errors 
                        Instr('addq', [Immediate(8*(len + 1)), Global(label_name('free_ptr'))]),
                        Instr('movq', [Immediate(tag), Deref('r11', 0)]),
                        Instr('movq', [Reg('r11'), new_lhs])]
                return list
            case Assign([lhs], Subscript(tup, Constant(index), Load())): #I get a type error here if I dont wrap index in Constant(), but it feels weird
                #ERROR: Cannot concatenate Name to str
                new_lhs = self.select_arg(lhs)
                new_tup = self.select_arg(tup)
                list = [
                        Instr('movq', [new_tup, Reg('r11')]),
                        Instr('movq', [Deref('r11', 8*(index + 1)), new_lhs])]
                return list
            case Assign([Subscript(tup, Constant(index), Store())], rhs):
                #ERROR: Cannot concatenate Name to str
                new_rhs = self.select_arg(rhs)
                new_tup = self.select_arg(tup)
                list = [Instr('movq', [new_tup, Reg('r11')]),
                        Instr('movq', [new_rhs, Deref('r11', 8*(index + 1))])]
                return list
            #Can't have these above specific cases as they catch all forms
            case Assign([lhs], rhs):
                # Handle assignment statements
                new_lhs = self.select_arg(lhs)
                new_rhs = self.select_arg(rhs)
                list = [Instr('movq', [new_rhs, new_lhs])]
                return list
            case Expr(exp):
                return []
            case _:
                raise ValueError(f"Unsupported statement type: {type(s)}")
            
    def select_tail(self, s: stmt) -> List[instr]:
        match s:
            case Return(exp):
                return [Instr('movq',[self.select_arg(exp),Reg('rax')]), Jump(label_name('conclusion'))]
            case Goto(label): 
                return [Jump(label)]
            case If(Compare(left,[cmp],[right]), [Goto(label_thn)], [Goto(label_else)]):
                return [Instr('cmpq', [self.select_arg(right), self.select_arg(left)]), JumpIf(self.select_op(cmp), label_thn), Jump(label_else)]

    def select_op(self, op):
        match op:
            case USub():
                return 'negq'
            case Add():
                return 'addq'
            case Sub():
                return 'subq'
            case Eq():
                return 'e'
            case NotEq():
                return 'ne'
            case Lt():
                return 'l'
            case LtE():
                return 'le'
            case Gt():
                return 'g'
            case GtE():
                return 'ge'
            case Is():
                raise NotImplementedError("Is() not implemented select_op")
                return 'e'
            case _:
                raise ValueError(f"Unsupported operand type: {type(op)}")
            
    def select_instructions(self, p: Module) -> X86Program:
        selected_basic_blocks = {label_name('conclusion'):[]}
        for label, block in p.body.items():
            selected_basic_blocks[label] = [instructions for s in block[:-1] for instructions in self.select_stmt(s)]+ self.select_tail(block[-1])


        #selected_instructions = [instruction for s in p.body for instruction in self.select_stmt(s)]
        x86 = X86Program(selected_basic_blocks)
        x86.var_types = p.var_types
        return x86
    

    ###########################################################################
    # Uncover Live
    ###########################################################################
        
    def generate_cfg(self, basic_blocks: Dict[str,List]) -> DirectedAdjList: # control flow graph
        cfg = DirectedAdjList()
        for label, instrs in basic_blocks.items():
            for instr in instrs:
                match instr:
                    case JumpIf(cc,jmp_label):
                        cfg.add_edge(label, jmp_label)
                    case Jump(jmp_label):
                        cfg.add_edge(label, jmp_label)
        return cfg
    
    def write_vars(self, i: instr) -> Set[location]:
        types = (type(Variable(id)), type(Reg(id)))
        match i:
            case Instr('cmpq', [arg1, arg2]):
                return set()            
            case Instr(op, operands):
                loc = operands[len(operands)-1]
                if isinstance(loc, types):
                    return set([loc])
                return set()
            case _:
                raise Exception("error in write_vars") 
            
    def read_vars(self, i: instr) -> Set[location]:
        types = (type(Variable(id)), type(Reg(id)))
        match i:
            case Instr('movq', [arg1, arg2]) | Instr('movzbq', [arg1, arg2]):
                if isinstance(arg1, types):
                    return set([arg1])
                return set()
            case Instr(op, operands):
                return {arg for arg in operands if isinstance(arg, types)}
            case _:
                raise Exception("error in read_vars")
            
    def uncover_instr(self, i: instr, l_after: Set[location], live_before_block: Dict[str,Set[location]]) -> Set[location]:
        w, r = set(), set()
        if isinstance(i, Instr):
            w = self.write_vars(i)
            r = self.read_vars(i)
        elif isinstance(i, Callq):
            w = {Reg(reg) for reg in ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10']} #removed r11 as its now used by tuples
            r = set()
            for _ in range(i.num_args):
                r.add(Reg(arg_registers[_]))
        elif isinstance(i, JumpIf):
            return l_after.union(live_before_block[i.label])
        elif isinstance(i, Jump):
            return live_before_block[i.label]
        return l_after.difference(w).union(r)
    
    # liveness analysis with cycles (loops)

    def uncover_live(self, p: X86Program) -> Dict[instr, Set[location]]:
        basic_blocks = p.body
        cfg = self.generate_cfg(basic_blocks)
        live_after = {}
        live_before = {}
        live_before_block = {}
        def transfer(block_label, live_after_block):
            lives = live_after_block
            for b in reversed(basic_blocks[block_label]):
                live_after[b] = lives
                lives = self.uncover_instr(b, lives, live_before_block)
                live_before[b] = lives
            live_before_block[block_label] = lives
            return lives
        def join(A, B):
            return A.union(B)
        for block in basic_blocks.keys():
            live_before_block[block] = set()
        analyze_dataflow(transpose(cfg), transfer, set(), join)
        return live_after
            
    # def select_stmt(self, s: stmt) -> List[instr]:
    #     match s:
    #         case Expr(Call(Name('print'), [rhs])):
    #             # Handle print statements
    #             new_rhs = self.select_arg(rhs)
    #             list = [Instr('movq', [new_rhs, Reg('rdi')]), Callq(label_name('print_int'), 1) ]
    #             return list
    #         case Assign([lhs], Compare(left, [op], [right])):
    #             # Handle assignment statements
    #             new_lhs = self.select_arg(lhs)
    #             new_right = self.select_arg(right)
    #             new_left = self.select_arg(left)
    #             list = [Instr('cmpq', [new_right, new_left]), 
    #                     Instr('set' + self.select_op(op), [Reg('al')]), 
    #                     Instr('movzbq', [Reg('al'), new_lhs])]
    #             return list
    #         case Assign([lhs], UnaryOp(Not(), operand)):
    #             # Handle assignment statements
    #             new_lhs = self.select_arg(lhs)
    #             rand = self.select_arg(operand)
    #             list = [Instr('movq', [rand, new_lhs]), 
    #                     Instr('xorq', [1,new_lhs])]
    #             return list
    #         case Assign([lhs], UnaryOp(op, operand)):
    #             # Handle assignment statements
    #             new_lhs = self.select_arg(lhs)
    #             rand = self.select_arg(operand)
    #             list = [Instr('movq', [rand, new_lhs]), 
    #                     Instr(self.select_op(op), [new_lhs])]
    #             return list
    #         case Assign([lhs], BinOp(leftatm, op, rightatm)):
    #             # Handle assignment statements
    #             new_lhs = self.select_arg(lhs)
    #             l = self.select_arg(leftatm)
    #             r = self.select_arg(rightatm)
    #             list = [Instr('movq', [l, new_lhs]), 
    #                     Instr(self.select_op(op), [r,new_lhs])]
    #             return list
    #         case Assign([lhs], Call(Name('input_int'), [])):
    #             # Handle assignment statements
    #             new_lhs = self.select_arg(lhs)
    #             list = [Callq(label_name('read_int'), 0), 
    #                     Instr('movq', [Reg('rax'), new_lhs])]
    #             return list
    #         case Expr(BinOp(leftatm, op, rightatm)):
    #             l = self.select_arg(leftatm)
    #             r = self.select_arg(rightatm)
    #             list = [Instr(self.select_op(op), [l,r])]
    #             return list
    #         case Expr(UnaryOp(op, operand)):
    #             # Handle assignment statements
    #             rand = self.select_arg(operand)
    #             list = [Instr(self.select_op(op), [rand])]
    #             return list
    #         case Expr(Call(Name('input_int'), [])):
    #             # Handle assignment statements
    #             list = [Callq(label_name('read_int', 0))]
    #             return list
    #         #tuple cases
    #         case Collect(bytes):
    #             list = [Instr('movq', [Reg('r15'), Reg('rdi')]),
    #                     Instr('movq', [Immediate(bytes), Reg('rsi')]),
    #                     Callq(label_name('collect'), 0)]
    #             return list
    #         case Assign([lhs], Call(Name('len'), [tup])):
    #             new_lhs = self.select_arg(lhs)
    #             new_tup = self.select_arg(tup)
    #             # and mask 000....0001111110 with first 7 bits
    #             # bit shift 1 to the right
    #             list = [Instr('movq', [Deref(new_tup, 0), Reg('rax')]), #deref(new_tup, 0) <- 0 is the index here element 0 is the header
    #                     Instr('andq', [Immediate(126), Reg('rax')]),
    #                     Instr('sarq', [Immediate(1), Reg('rax')]),
    #                     Instr('movq', [Reg('rax'), new_lhs])]
    #         case Assign([lhs], Allocate(len, type)):
    #             new_lhs = self.select_arg(lhs)
    #             pointer_mask = 0
    #             is_pointer = False
    #             for i in range(len):
    #                 if(is_pointer):
    #                     pointer_mask &= 1
    #                 pointer_mask <<= 1
    #             tag = pointer_mask << 6
    #             #lenb = Bin(len)
    #             tag = tag & len #len or lenb            
    #             tag = (tag << 1) & 1 # sets forwarding bit

    #             #Can i pass in decimal for the tag or does it have to be in binary
    #             list = [Instr('movq', [Global(label_name('free_ptr')), Reg('r11')]), #Replaced Global with GlobalValue and it seemed to get rid of some errors 
    #                     Instr('addq', [Immediate(8*(len + 1)), Global(label_name('free_ptr'))]),
    #                     Instr('movq', [Immediate(tag), Deref('r11', 0)]),
    #                     Instr('movq', [Reg('r11'), new_lhs])]
    #             return list
    #         case Assign([lhs], Subscript(tup, Constant(index), Load())): #I get a type error here if I dont wrap index in Constant(), but it feels weird
    #             #ERROR: Cannot concatenate Name to str
    #             new_lhs = self.select_arg(lhs)
    #             new_tup = self.select_arg(tup)
    #             list = [Instr('movq', [Deref(tup, index), Reg('r11')]),
    #                     Instr('movq', [Deref('r11', 8*(index + 1)), new_lhs])]
    #             return list
    #         case Assign([Subscript(tup, Constant(index), Store())], rhs):
    #             #ERROR: Cannot concatenate Name to str
    #             new_rhs = self.select_arg(rhs)
    #             new_tup = self.select_arg(tup)
    #             list = [Instr('movq', [Deref(tup, index), Reg('r11')]),
    #                     Instr('movq', [new_rhs, Deref('r11', 8*(index + 1))])]
    #             return list
    #         #Can't have these above specific cases as they catch all forms
    #         case Assign([lhs], rhs):
    #             # Handle assignment statements
    #             new_lhs = self.select_arg(lhs)
    #             new_rhs = self.select_arg(rhs)
    #             list = [Instr('movq', [new_rhs, new_lhs])]
    #             return list
    #         case Expr(exp):
    #             return []
    #         case _:
    #             raise ValueError(f"Unsupported statement type: {type(s)}")
            
    # def select_tail(self, s: stmt) -> List[instr]:
    #     match s:
    #         case Return(exp):
    #             return [Instr('movq',[self.select_arg(exp),Reg('rax')]), Jump(label_name('conclusion'))]
    #         case Goto(label):
    #             return [Jump(label)]
    #         case If(Compare(left,[cmp],[right]), [Goto(label_thn)], [Goto(label_else)]):
    #             return [Instr('cmpq', [self.select_arg(right), self.select_arg(left)]), JumpIf(self.select_op(cmp), label_thn), Jump(label_else)]

    # def select_op(self, op):
    #     match op:
    #         case USub():
    #             return 'negq'
    #         case Add():
    #             return 'addq'
    #         case Sub():
    #             return 'subq'
    #         case Eq():
    #             return 'e'
    #         case NotEq():
    #             return 'ne'
    #         case Lt():
    #             return 'l'
    #         case LtE():
    #             return 'le'
    #         case Gt():
    #             return 'g'
    #         case GtE():
    #             return 'ge'
    #         case Is():
    #             raise NotImplementedError("Is() not implemented select_op")
    #             return 'e'
    #         case _:
    #             raise ValueError(f"Unsupported operand type: {type(op)}")
            
    # def select_instructions(self, p: Module) -> X86Program:
    #     selected_basic_blocks = {label_name('conclusion'):[]}
    #     for label, block in p.body.items():
    #         selected_basic_blocks[label] = [instructions for s in block[:-1] for instructions in self.select_stmt(s)]+ self.select_tail(block[-1])


    #     #selected_instructions = [instruction for s in p.body for instruction in self.select_stmt(s)]
    #     return X86Program(selected_basic_blocks)
    

    # ###########################################################################
    # # Uncover Live
    # ###########################################################################
        
    # def generate_cfg(self, basic_blocks: Dict[str,List]) -> DirectedAdjList: # control flow graph
    #     cfg = DirectedAdjList()
    #     for label, instrs in basic_blocks.items():
    #         for instr in instrs:
    #             match instr:
    #                 case JumpIf(cc,jmp_label):
    #                     cfg.add_edge(label, jmp_label)
    #                 case Jump(jmp_label):
    #                     cfg.add_edge(label, jmp_label)
    #     return cfg
    
    # def write_vars(self, i: instr) -> Set[location]:
    #     types = (type(Variable(id)), type(Reg(id)))
    #     match i:
    #         case Instr('cmpq', [arg1, arg2]):
    #             return set()            
    #         case Instr(op, operands):
    #             loc = operands[len(operands)-1]
    #             if isinstance(loc, types):
    #                 return set([loc])
    #             return set()
    #         case _:
    #             raise Exception("error in write_vars") 
            
    # def read_vars(self, i: instr) -> Set[location]:
    #     types = (type(Variable(id)), type(Reg(id)))
    #     match i:
    #         case Instr('movq', [arg1, arg2]) | Instr('movzbq', [arg1, arg2]):
    #             if isinstance(arg1, types):
    #                 return set([arg1])
    #             return set()
    #         case Instr(op, operands):
    #             return {arg for arg in operands if isinstance(arg, types)}
    #         case _:
    #             raise Exception("error in read_vars")
            
    # def uncover_instr(self, i: instr, l_after: Set[location], live_before_block: Dict[str,Set[location]]) -> Set[location]:
    #     w, r = set(), set()
    #     if isinstance(i, Instr):
    #         w = self.write_vars(i)
    #         r = self.read_vars(i)
    #     elif isinstance(i, Callq):
    #         w = {Reg(reg) for reg in ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10']} #removed r11 as its now used by tuples
    #         r = set()
    #         for _ in range(i.num_args):
    #             r.add(Reg(arg_registers[_]))
    #     elif isinstance(i, JumpIf):
    #         return l_after.union(live_before_block[i.label])
    #     elif isinstance(i, Jump):
    #         return live_before_block[i.label]
    #     return l_after.difference(w).union(r)
    
    # # liveness analysis with cycles (loops)

    # def uncover_live(self, p: X86Program) -> Dict[instr, Set[location]]:
    #     basic_blocks = p.body
    #     cfg = self.generate_cfg(basic_blocks)
    #     live_after = {}
    #     live_before = {}
    #     live_before_block = {}
    #     def transfer(block_label, live_after_block):
    #         lives = live_after_block
    #         for b in reversed(basic_blocks[block_label]):
    #             live_after[b] = lives
    #             lives = self.uncover_instr(b, lives, live_before_block)
    #             live_before[b] = lives
    #         live_before_block[block_label] = lives
    #         return lives
    #     def join(A, B):
    #         return A.union(B)
    #     for block in basic_blocks.keys():
    #         live_before_block[block] = set()
    #     analyze_dataflow(transpose(cfg), transfer, set(), join)
    #     return live_after
    

    ############################################################################
    # Build Interference
    ############################################################################

    def build_graphs(self, p: X86Program, live_after: Dict[instr, Set[location]]) -> Tup[UndirectedAdjList,UndirectedAdjList]:
        graph_inter = UndirectedAdjList()
        graph_move = UndirectedAdjList()
        for instr, locs in live_after.items():
            match instr:
                case Instr(inst, operands):
                    d = operands[len(operands)-1]
                    for v in locs:
                        if v != d:
                            graph_inter.add_edge(d,v)
                        if(v.id in p.var_types.keys() and isinstance(p.var_types[v.id], TupleType)):
                            [graph_inter.add_edge(v, Reg(reg)) for reg in callee_saved_regs]
                    #[graph_inter.add_edge(d, v) for v in locs if v != d]
                    if len(operands) > 1:
                        s = operands[0]
                        if inst == 'movq' and isinstance(s,type(Variable(id))) and isinstance(d,type(Variable(id))):
                            graph_move.add_edge(s,d)
                case Callq(_, _):
                    [graph_inter.add_edge(v, Reg(reg)) for v in locs for reg in caller_saved_regs]
        return graph_inter,graph_move
    

    ############################################################################
    # Allocate Registers
    ############################################################################
    # Returns the coloring and the set of spilled variables.
    
    def color_graph(self, var_types, inter_graph: UndirectedAdjList, move_graph: UndirectedAdjList,
                    variables: Set[location]) -> Tup[Dict[location, int], Set[location]]:
        self.root_spills = 0
        color = {Reg(reg): -index for index, reg in enumerate(['rax', 'rsp', 'rbp'])} #removed r15, r11 because as of tuples it is a dedicated reg
        color.update({Reg(reg): index for index, reg in enumerate(['rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'rbx', 'r12', 'r13', 'r14'])})
        saturation = {} # var, Set(int)
        spilled = set()
        def allocate_color(u):
            unavail_colors = saturation[u]
            mov_regs = {color[vert] for vert in move_graph.adjacent(u) if vert in color and color[vert] < 11}
            mov_stack = {color[vert] for vert in move_graph.adjacent(u) if vert in color and color[vert] >= 11}
            mov_regs, mov_stack = sorted(mov_regs), sorted(mov_stack)
            if(isinstance(var_types[u.id],TupleType)):
                color[u] = 1000
                self.root_spills += 1
                return
            for reg in mov_regs + list(range(11)):
                if reg not in unavail_colors:
                    color[u] = reg
                    if 7 <= reg <= 10:
                        self.callee_regs.add(callee_saved_regs[reg - 7])
                    if reg == self.highest_loc:
                        self.highest_loc += 1
                    return
            for num in mov_stack + list(range(11, self.highest_loc + 1)):
                if num not in unavail_colors:
                    color[u] = num
                    if num >= 11:
                        spilled.add(u)
                    if num == self.highest_loc:
                        self.highest_loc += 1
                    return
        def compare(u, v):
            if len(saturation[u.key]) == len(saturation[v.key]):
                for vert in move_graph.adjacent(u):
                    if vert in color:
                        if color[vert] not in saturation[u]:
                            return False     
                return True
            else:
                return len(saturation[u.key]) < len(saturation[v.key])
        Q = PriorityQueue(compare)
        for var in variables:
            saturation[var] = set(color[vert] for vert in inter_graph.adjacent(var) if vert in color)
            Q.push(var)
        while not Q.empty():
            u = Q.pop()
            if isinstance(u,Variable):
                allocate_color(u)
                for vert in inter_graph.adjacent(u):
                    saturation[vert].add(color[u]) 
                    Q.increase_key(vert)
        return color, spilled 
    

    ############################################################################
    # Assign Homes
    ############################################################################

    def assign_homes_arg(self, a: arg, home: Dict[Variable, arg]) -> arg:
        match a:
            case Variable(var):
                return home[a]
            case _:
                return a
            
    def gen_home(self):
        inst = Deref('rbp', -8* (self.counter+1 + len(self.callee_regs)))
        self.counter+=1
        return inst
    
    def gen_hometup(self):
        inst = Deref('r15', -8*(self.tup_counter+1))
        self.tup_counter+=1
        return inst
    
    def assign_homes_instr(self, i: instr, home: Dict[Variable, arg]) -> instr:
        match i:
            case Instr(inst, operands):
                new_operands = [self.assign_homes_arg(arg, home) for arg in operands]
                return Instr(inst, new_operands)
            case _:
                return i
            
    def assign_homes_instrs(self, block_dict: Dict[str,List[Instr]], home: Dict[Variable, arg]) -> List[instr]:
        correspondence = {i: Reg(reg) for i, reg in enumerate(['rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'rbx', 'r12', 'r13', 'r14'])}
        asnd_block_dict = {}
        def assign_home(arg):
            if arg not in home:
                mem_no = self.coloring[arg]
                if mem_no == 1000:
                    correspondence[mem_no] = self.gen_hometup()
                elif mem_no not in correspondence:
                    correspondence[mem_no] = self.gen_home()
                home[arg] = correspondence[mem_no]
        for label, block in block_dict.items():
            for i in block:
                match i:
                    case Instr(inst, operands):
                        [assign_home(arg) for arg in operands if isinstance(arg, type(Variable(id)))]
            asnd_block_dict[label] = [self.assign_homes_instr(i, home) for i in block]
        return asnd_block_dict
    
    def collect_vars(self, i: instr) -> Set:
        vars = set()
        match i:
            case Instr(op, operands):
                [vars.add(var) for var in operands if isinstance(var, type(Variable(id)))]
        return vars
    
    def assign_homes(self, p: X86Program) -> X86Program:
        # print(p.var_types)
        l_after = self.uncover_live(p)
        interference,move = self.build_graphs(p, l_after)
        vars = set()
        for v in interference.vertices():
            vars.add(v)
        for label,block in p.body.items():
            for instr in block:
                vars = vars.union(self.collect_vars(instr))
        self.coloring, self.spilled = self.color_graph(p.var_types, interference, move, vars)
        m =self.assign_homes_instrs(p.body,{})
        return X86Program(m)
    

    ############################################################################
    # Patch Instructions
    ############################################################################

    def patch_instr(self, i: instr) -> List[instr]:
        match i:
            case Instr('movq', [Deref(reg1, offset1) as arg1, Deref(reg2, offset2) as arg2]) if arg1 == arg2:
                return []
            case Instr('movq' | 'cmpq' as instr, [Deref(reg1, offset1) as arg1, Deref(reg2, offset2) as arg2]):
                return [Instr('movq', [arg1, Reg('rax')]), Instr(instr, [Reg('rax'), arg2])]
            case Instr('movq', [arg1, arg2]) if arg1 == arg2:
                return []
            case Instr('movq', [arg1, arg2]):
                return [i]
            case Instr(instr, [Immediate(num), Deref(reg, offset) as arg]) if num > 2**16:
                return [Instr('movq', [Immediate(num), Reg('rax')]), Instr(instr, [Reg('rax'), arg])]
            case _:
                return [i]
            
    def patch_instrs(self, ss: List[instr]) -> List[instr]:
        return [instruction for i in ss for instruction in self.patch_instr(i)]
    
    def patch_instructions(self, p: X86Program) -> X86Program:
        selected_basic_blocks = {}
        for label, block in p.body.items():
            selected_basic_blocks[label] = self.patch_instrs(block)
        return X86Program(selected_basic_blocks)   
      
    ############################################################################
    # Prelude & Conclusion
    ############################################################################

    def prelude_and_conclusion(self, p: X86Program) -> X86Program:
        blocks = p.body
        call_regs = list(self.callee_regs)
        prelude = [Instr('pushq', [Reg('rbp')]), Instr('movq', [Reg('rsp'), Reg('rbp')])]
        conclusion = [Instr('popq', [Reg('rbp')]),Instr('retq', [])]
        callee_push = [Instr('pushq', [Reg(reg)]) for reg in call_regs]
        callee_pop = [Instr('popq', [Reg(reg)]) for reg in reversed(call_regs)]
        stack_space = align(8 * (self.counter + len(call_regs)), 16) - (8 * len(call_regs))
        if stack_space != 0:
            stack_adjustment_sub = [Instr('subq', [Immediate(stack_space), Reg('rsp')])]
            stack_adjustment_add = [Instr('addq', [Immediate(stack_space), Reg('rsp')])]
        else:
            stack_adjustment_sub = []
            stack_adjustment_add = []

        initialize = [Instr('movq', [Immediate(65536), Reg('rdi')]), 
                      Instr('movq', [Immediate(16), Reg('rsi')]),
                      Callq(label_name('initialize'), 2)]
        
        root_handling = [Instr('movq', [Global(label_name('rootstack_begin')), Reg('r15')])]
        for i in range(self.root_spills):
            root_handling.append(Instr('movq', [Immediate(0), Deref('r15', 0)]))
            root_handling.append(Instr('addq', [Immediate(8), Reg('r15')]))

        blocks[label_name('main')] = prelude + callee_push + stack_adjustment_sub + initialize + root_handling+ [Jump(label_name('start'))]

        # blocks[label_name('main')] = prelude + callee_push + stack_adjustment_sub + [Jump(label_name('start'))]

        blocks[label_name('conclusion')] = stack_adjustment_add + callee_pop + conclusion
        return X86Program(blocks)

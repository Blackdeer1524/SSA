from collections import defaultdict
from dataclasses import dataclass, field
from typing import Literal, Optional
from src.cfg.instructions import Add, Cmp, Instruction, Jump, Mov, Phi, Return
from src.analysis.task_transitions import (
    BlockNode,
    CMPNode,
    ConditionNode,
    DeclarationNode,
    EOFNode,
    ElseBranchNode,
    ExpressionNode,
    ExpressionTailNode,
    FunctionNode,
    IdentNode,
    InitNode,
    KeywordBangEqualsNode,
    KeywordEqualsEqualsNode,
    KeywordEqualsNode,
    KeywordGreaterThanEqualsNode,
    KeywordGreaterThanNode,
    KeywordLeftBraceNode,
    KeywordLeftParenNode,
    KeywordLessThanEqualsNode,
    KeywordLessThanNode,
    KeywordPlusNode,
    KeywordRightBraceNode,
    KeywordRightParenNode,
    KeywordSemicolonNode,
    KeywordforNode,
    KeywordifNode,
    KeywordintNode,
    KeywordreturnNode,
    LogicalNode,
    Loop_1Node,
    Loop_2Node,
    Loop_3Node,
    LoopNode,
    NumberNode,
    ReassignmentNode,
    ReturnNode,
    StatementsNode,
)
from src.table_synthesis.stream import Stream


bb_count = 0


def generate_bb_name() -> str:
    global bb_count
    res = f"BB{bb_count}"
    bb_count += 1
    return res


@dataclass
class BasicBlock:
    name: str = field(init=False, default_factory=generate_bb_name)

    pred: list["BasicBlock"] = field(init=False, default_factory=list)
    succ: list["BasicBlock"] = field(init=False, default_factory=list)

    phi: dict[str, Phi] = field(init=False, default_factory=dict)
    instructions: list[Instruction] = field(init=False, default_factory=list)

    def traverse_preorder(self):
        q: list[BasicBlock] = [self]
        seen: set[str] = set()
        while len(q) > 0:
            top = q.pop()
            if top.name in seen:
                continue
            seen.add(top.name)
            yield top
            for s in top.succ:
                q.append(s)

    def push(self, i: Instruction):
        self.instructions.append(i)

    def add_child(self, c: "BasicBlock"):
        self.succ.append(c)
        c.pred.append(self)

    def to_IR(self) -> str:
        ss = Stream()
        with ss.push_line(f"{self.name}:").indent() as block:
            for phi in self.phi.values():
                block.push_line(phi.to_string())
                
            for instruction in self.instructions:
                block.push_line(instruction.to_string())
        return ss.emit()

    def to_graphviz(self, seen_nodes=set()) -> str:
        if self.name in seen_nodes:
            return ""
        seen_nodes.add(self.name)

        res = "\t" + self.name + f' [label="'
        res += self.to_IR().replace("\n", "\\l")

        res += '"]\n'
        for s in self.succ:
            res += f"\t{self.name} -> {s.name}\n"

        for s in self.succ:
            res += s.to_graphviz(seen_nodes)

        return res


def generate_IR(entry: BasicBlock) -> str:
    ss = Stream()
    for bb in entry.traverse_preorder():
        preds = ", ".join((p.name for p in bb.pred))
        succs = ", ".join((s.name for s in bb.succ))
        ss.push_line("; predecesors: " + preds)
        ss.push_line("; successors: " + succs)
        ss.push_line(bb.to_IR())
    return ss.emit()


class Builder:
    def __init__(self, cur: BasicBlock):
        self.cur = cur


# var_name_c = 0


def generate_var_name() -> str:
    # global var_name_c
    # res = f"%{var_name_c}"
    # var_name_c += 1
    return "%"


def codegen_expr_tail(
    tail: ExpressionTailNode, builder: Builder
) -> Optional[tuple[Literal["+"], str | int]]:
    match tail.value:
        case None:
            return None
        case tuple((KeywordPlusNode(), ExpressionNode() as expr)):
            res = codegen_expression(expr, builder)
            return ("+", res)


def codegen_expression(expr: ExpressionNode, builder: Builder) -> str | int:
    match expr.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (KeywordLeftParenNode(), ExpressionNode() as inner, KeywordRightParenNode())
        ):
            return codegen_expression(inner, builder)
        case tuple((IdentNode() as ident, ExpressionTailNode() as tail)):
            assert ident.value is not None
            match codegen_expr_tail(tail, builder):
                case None:
                    return ident.value.value
                case tuple(("+", int() as rhs)):
                    lhs = generate_var_name()
                    add = Add(lhs, ident.value.value, rhs)
                    builder.cur.push(add)
                    return lhs
                case tuple(("+", str() as rhs)):
                    lhs = generate_var_name()
                    add = Add(lhs, ident.value.value, rhs)
                    builder.cur.push(add)
                    return lhs
        case tuple((NumberNode() as number, ExpressionTailNode() as tail)):
            assert number.value is not None
            match codegen_expr_tail(tail, builder):
                case None:
                    return number.value.value
                case tuple(("+", int() as rhs)):
                    lhs = generate_var_name()
                    add = Add(lhs, number.value.value, rhs)
                    builder.cur.push(add)
                    return lhs
                case tuple(("+", str() as rhs)):
                    lhs = generate_var_name()
                    add = Add(lhs, number.value.value, rhs)
                    builder.cur.push(add)
                    return lhs
    raise RuntimeError("unreachable")


# TODO: check that the variable is not redeclared
def codegen_decl(decl: DeclarationNode, builder: Builder):
    match decl.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (
                KeywordintNode(),
                IdentNode() as ident,
                KeywordEqualsNode(),
                ExpressionNode() as rhs,
            )
        ):
            assert ident.value is not None

            res = codegen_expression(rhs, builder)
            builder.cur.push(Mov(ident.value.value, res))


# TODO: check that the variable actually exists
def codegen_reassign(reassign: ReassignmentNode, builder: Builder):
    match reassign.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (IdentNode() as ident, KeywordEqualsNode(), ExpressionNode() as rhs)
        ):
            assert ident.value is not None

            res = codegen_expression(rhs, builder)
            builder.cur.push(Mov(ident.value.value, res))


def codegen_return(reassign: ReturnNode, builder: Builder):
    match reassign.value:
        case None:
            raise NotImplementedError()
        case tuple((KeywordreturnNode(), ExpressionNode() as expr)):
            res = codegen_expression(expr, builder)
            builder.cur.push(Return(res))


def codegen_logic(node: LogicalNode, builder: Builder) -> CMPNode:
    match node.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (ExpressionNode() as lhs, CMPNode() as cmp, ExpressionNode() as rhs)
        ):
            lhs_res = codegen_expression(lhs, builder)
            rhs_res = codegen_expression(rhs, builder)
            builder.cur.push(Cmp(lhs_res, rhs_res))
            return cmp


def codegen_cond(cond: ConditionNode, builder: Builder):
    match cond.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (
                KeywordifNode(),
                KeywordLeftParenNode(),
                LogicalNode() as logic,
                KeywordRightParenNode(),
                BlockNode() as then_block_node,
                ElseBranchNode() as else_block_node,
            )
        ):
            then_block = BasicBlock()
            builder.cur.add_child(then_block)

            else_block: Optional[BasicBlock] = None
            if else_block_node.value is not None:
                else_block = BasicBlock()

            next_block = BasicBlock()
            if else_block is not None:
                condition_false_block = else_block
            else:
                condition_false_block = next_block

            builder.cur.add_child(condition_false_block)
            cmp = codegen_logic(logic, builder)
            match cmp.value:
                case None:
                    raise NotImplementedError()
                case KeywordLessThanNode():
                    builder.cur.push(Jump("jlt", then_block.name))
                case KeywordLessThanEqualsNode():
                    builder.cur.push(Jump("jle", then_block.name))
                case KeywordGreaterThanNode():
                    builder.cur.push(Jump("jgt", then_block.name))
                case KeywordGreaterThanEqualsNode():
                    builder.cur.push(Jump("jge", then_block.name))
                case KeywordEqualsEqualsNode():
                    builder.cur.push(Jump("je", then_block.name))
                case KeywordBangEqualsNode():
                    builder.cur.push(Jump("jne", then_block.name))

            builder.cur.push(Jump("jmp", condition_false_block.name))
            builder.cur = then_block
            codegen_block(then_block_node, builder)
            builder.cur.add_child(next_block)
            builder.cur.push(Jump("jmp", next_block.name))

            if else_block_node.value is not None:
                assert else_block is not None
                builder.cur = else_block
                codegen_block(else_block_node.value[1], builder)
                builder.cur.add_child(next_block)
                builder.cur.push(Jump("jmp", next_block.name))

            builder.cur = next_block


def codegen_loop(node: LoopNode, builder: Builder):
    match node.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (
                KeywordforNode(),
                KeywordLeftParenNode(),
                Loop_1Node() as init,
                KeywordSemicolonNode(),
                Loop_2Node() as cond,
                KeywordSemicolonNode(),
                Loop_3Node() as step,
                KeywordRightParenNode(),
                BlockNode() as loop_body,
            )
        ):
            match init.value:
                case None:
                    ...
                case DeclarationNode() as decl:
                    codegen_decl(decl, builder)
                case ReassignmentNode() as reassign:
                    codegen_reassign(reassign, builder)

            loop_header = BasicBlock()
            builder.cur.add_child(loop_header)
            builder.cur.push(Jump("jmp", loop_header.name))

            loop_block = BasicBlock()
            loop_header.add_child(loop_block)

            next_block = BasicBlock()
            loop_header.add_child(next_block)

            builder.cur = loop_header
            match cond.value:
                case None:
                    builder.cur.push(Jump("jmp", loop_block.name))
                case LogicalNode() as logic:
                    cmp = codegen_logic(logic, builder)
                    match cmp.value:
                        case None:
                            raise NotImplementedError()
                        case KeywordLessThanNode():
                            builder.cur.push(Jump("jlt", loop_block.name))
                        case KeywordLessThanEqualsNode():
                            builder.cur.push(Jump("jle", loop_block.name))
                        case KeywordGreaterThanNode():
                            builder.cur.push(Jump("jgt", loop_block.name))
                        case KeywordGreaterThanEqualsNode():
                            builder.cur.push(Jump("jge", loop_block.name))
                        case KeywordEqualsEqualsNode():
                            builder.cur.push(Jump("je", loop_block.name))
                        case KeywordBangEqualsNode():
                            builder.cur.push(Jump("jne", loop_block.name))

                    builder.cur.push(Jump("jmp", next_block.name))
                    builder.cur = loop_block
                    codegen_block(loop_body, builder)

                    match step.value:
                        case None:
                            ...  # OK here
                        case ReassignmentNode() as reassign:
                            codegen_reassign(reassign, builder)

                    builder.cur.push(Jump("jmp", loop_header.name))
                    builder.cur.add_child(loop_header)
                    builder.cur = next_block


def codegen_statements(node: StatementsNode, builder: Builder):
    match node.value:
        case None:
            ...  # OK here
        case tuple((DeclarationNode() as decl, _, StatementsNode() as tail)):
            codegen_decl(decl, builder)
            codegen_statements(tail, builder)
        case tuple((ReassignmentNode() as reassign, _, StatementsNode() as tail)):
            codegen_reassign(reassign, builder)
            codegen_statements(tail, builder)
        case tuple((ReturnNode() as ret, _, StatementsNode() as tail)):
            codegen_return(ret, builder)
            codegen_statements(tail, builder)
        case tuple((ConditionNode() as cond, StatementsNode() as tail)):
            codegen_cond(cond, builder)
            codegen_statements(tail, builder)
        case tuple((LoopNode() as loop, StatementsNode() as tail)):
            codegen_loop(loop, builder)
            codegen_statements(tail, builder)


def codegen_block(node: BlockNode, builder: Builder):
    match node.value:
        case None:
            raise NotImplementedError()
        case tuple(
            (KeywordLeftBraceNode(), StatementsNode() as stmts, KeywordRightBraceNode())
        ):
            codegen_statements(stmts, builder)


def codegen_function(node: FunctionNode, builder: Builder):
    match node.value:
        case None:
            raise NotImplementedError()
        case tuple((_, _, BlockNode() as block)):
            codegen_block(block, builder)


def build_cfg(node: InitNode) -> BasicBlock:
    entry = BasicBlock()
    builder = Builder(entry)

    match node.value:
        case tuple((FunctionNode() as func, EOFNode())):
            codegen_function(func, builder)
        case None:
            raise NotImplementedError()

    return entry


def get_graph(entry: BasicBlock) -> dict[str, BasicBlock]:
    vertices: dict[str, BasicBlock] = {}
    for bb in entry.traverse_preorder():
        vertices[bb.name] = bb
    return vertices

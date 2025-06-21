# ====================
# |   |!=|int|return|for|#EOF|}|fn|#Number|>=|=|==|)|+|;|#Ident|<=|<|else|if|main|>|{|(|
# |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# |Function|-|-|-|-|-|-|fn main Block|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# |Block|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|{ Statements }|-|
# |Statements|-|Declaration ; Statements|Return ; Statements|Loop Statements|-|𝓔|-|-|-|-|-|-|-|-|Reassignment ; Statements|-|-|-|Condition Statements|-|-|-|-|
# |Return|-|-|return Expression|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# |Declaration|-|int #Ident = Expression|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# |Reassignment|-|-|-|-|-|-|-|-|-|-|-|-|-|-|#Ident = Expression|-|-|-|-|-|-|-|-|
# |Expression|-|-|-|-|-|-|-|#Number ExpressionTail|-|-|-|-|-|-|#Ident ExpressionTail|-|-|-|-|-|-|-|( Expression )|
# |ExpressionTail|𝓔|-|-|-|-|-|-|-|𝓔|-|𝓔|𝓔|+ Expression|𝓔|-|𝓔|𝓔|-|-|-|𝓔|-|-|
# |Condition|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|if ( Logical ) Block ElseBranch|-|-|-|-|
# |ElseBranch|-|𝓔|𝓔|𝓔|-|𝓔|-|-|-|-|-|-|-|-|𝓔|-|-|else Block|𝓔|-|-|-|-|
# |Logical|-|-|-|-|-|-|-|Expression CMP Expression|-|-|-|-|-|-|Expression CMP Expression|-|-|-|-|-|-|-|Expression CMP Expression|
# |CMP|!=|-|-|-|-|-|-|-|>=|-|==|-|-|-|-|<=|<|-|-|-|>|-|-|
# |Loop|-|-|-|for ( Loop_1 ; Loop_2 ; Loop_3 ) Block|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# |Loop_1|-|Declaration|-|-|-|-|-|-|-|-|-|-|-|𝓔|Reassignment|-|-|-|-|-|-|-|-|
# |Loop_2|-|-|-|-|-|-|-|Logical|-|-|-|-|-|𝓔|Logical|-|-|-|-|-|-|-|Logical|
# |Loop_3|-|-|-|-|-|-|-|-|-|-|-|𝓔|-|-|Reassignment|-|-|-|-|-|-|-|-|
# |Init|-|-|-|-|-|-|Function #EOF|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# 
# ====================
from typing import Optional, Union
from dataclasses import dataclass, field

from src.common.abc import IGraphVizible
from src.common.pretty import wrap
from src.text.processors import Position

from src.scanning.task_scanner import Token

# every scanner has to provide
from src.scanning.task_scanner import Keyword

# Token types:
from src.scanning.task_scanner import EOF, Number, Ident

@dataclass
class IASTNode(IGraphVizible):
    pos: Optional[Position] = field(init=False, default=None)

    @property
    def node_label(self) -> str:
        return super().node_label + wrap(f"({str(self.pos)}))")


# ============== NONTERM NODES =============
@dataclass
class FunctionNode(IASTNode):
    value: Optional[tuple["KeywordfnNode", "KeywordmainNode", "BlockNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class BlockNode(IASTNode):
    value: Optional[tuple["KeywordLeftBraceNode", "StatementsNode", "KeywordRightBraceNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class StatementsNode(IASTNode):
    value: Optional[Union[tuple["DeclarationNode", "KeywordSemicolonNode", "StatementsNode"],tuple["ReassignmentNode", "KeywordSemicolonNode", "StatementsNode"],tuple["ReturnNode", "KeywordSemicolonNode", "StatementsNode"],tuple["ConditionNode", "StatementsNode"],tuple["LoopNode", "StatementsNode"]]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class ReturnNode(IASTNode):
    value: Optional[tuple["KeywordreturnNode", "ExpressionNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class DeclarationNode(IASTNode):
    value: Optional[tuple["KeywordintNode", "IdentNode", "KeywordEqualsNode", "ExpressionNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class ReassignmentNode(IASTNode):
    value: Optional[tuple["IdentNode", "KeywordEqualsNode", "ExpressionNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class ExpressionNode(IASTNode):
    value: Optional[Union[tuple["NumberNode", "ExpressionTailNode"],tuple["IdentNode", "ExpressionTailNode"],tuple["KeywordLeftParenNode", "ExpressionNode", "KeywordRightParenNode"]]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class ExpressionTailNode(IASTNode):
    value: Optional[tuple["KeywordPlusNode", "ExpressionNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class ConditionNode(IASTNode):
    value: Optional[tuple["KeywordifNode", "KeywordLeftParenNode", "LogicalNode", "KeywordRightParenNode", "BlockNode", "ElseBranchNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class ElseBranchNode(IASTNode):
    value: Optional[tuple["KeywordelseNode", "BlockNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class LogicalNode(IASTNode):
    value: Optional[tuple["ExpressionNode", "CMPNode", "ExpressionNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class CMPNode(IASTNode):
    value: Optional[Union["KeywordLessThanNode","KeywordLessThanEqualsNode","KeywordGreaterThanNode","KeywordGreaterThanEqualsNode","KeywordEqualsEqualsNode","KeywordBangEqualsNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
        return res

@dataclass
class LoopNode(IASTNode):
    value: Optional[tuple["KeywordforNode", "KeywordLeftParenNode", "Loop_1Node", "KeywordSemicolonNode", "Loop_2Node", "KeywordSemicolonNode", "Loop_3Node", "KeywordRightParenNode", "BlockNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

@dataclass
class Loop_1Node(IASTNode):
    value: Optional[Union["DeclarationNode","ReassignmentNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
        return res

@dataclass
class Loop_2Node(IASTNode):
    value: Optional["LogicalNode"] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
        return res

@dataclass
class Loop_3Node(IASTNode):
    value: Optional["ReassignmentNode"] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
        return res

@dataclass
class InitNode(IASTNode):
    value: Optional[tuple["FunctionNode", "EOFNode"]] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"\t{self.node_name} -> {epsilon_name}\n" 
            case tuple():
                res += "".join(child.to_graphviz() for child in self.value) 
                res += "".join( 
                    f"\t{self.node_name} -> {child.node_name}\n" for child in self.value 
                )
                assert len(self.value) > 1
                res += "\t{{rank=same; {} [style=invis]}}\n".format(
                    " -> ".join(child.node_name for child in self.value)
                )
        return res

NON_TERMINAL = FunctionNode | BlockNode | StatementsNode | ReturnNode | DeclarationNode | ReassignmentNode | ExpressionNode | ExpressionTailNode | ConditionNode | ElseBranchNode | LogicalNode | CMPNode | LoopNode | Loop_1Node | Loop_2Node | Loop_3Node | InitNode
# ============== TERM NODES =============
@dataclass
class EOFNode(IASTNode):
    value: Optional[EOF] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"{self.node_name} -> {epsilon_name}" 
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
                return res

@dataclass
class NumberNode(IASTNode):
    value: Optional[Number] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"{self.node_name} -> {epsilon_name}" 
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
                return res

@dataclass
class IdentNode(IASTNode):
    value: Optional[Ident] = None
    
    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}" 
                res += f'\t{epsilon_name} [label="𝓔"]\n' 
                res += f"{self.node_name} -> {epsilon_name}" 
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n" 
                return res

# ============== KEYWORD NODES =============
@dataclass
class KeywordBangEqualsNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordintNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordreturnNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordforNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordRightBraceNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordfnNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordGreaterThanEqualsNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordEqualsNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordEqualsEqualsNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordRightParenNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordPlusNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordSemicolonNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordLessThanEqualsNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordLessThanNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordelseNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordifNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordmainNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordGreaterThanNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordLeftBraceNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

@dataclass
class KeywordLeftParenNode(IASTNode):
    value: Optional["Keyword"] = None

    def to_graphviz(self) -> str:
        res = super().to_graphviz()
        match self.value:
            case None:
                epsilon_name = f"𝓔{id(self)}"
                res += f'\t{epsilon_name} [label="𝓔"]\n'
                res += f"{self.node_name} -> {epsilon_name}"
                return res
            case _:
                res += self.value.to_graphviz()
                res += f"\t{self.node_name} -> {self.value.node_name}\n"
        return res

TERMINAL = EOFNode | NumberNode | IdentNode | KeywordBangEqualsNode | KeywordintNode | KeywordreturnNode | KeywordforNode | KeywordRightBraceNode | KeywordfnNode | KeywordGreaterThanEqualsNode | KeywordEqualsNode | KeywordEqualsEqualsNode | KeywordRightParenNode | KeywordPlusNode | KeywordSemicolonNode | KeywordLessThanEqualsNode | KeywordLessThanNode | KeywordelseNode | KeywordifNode | KeywordmainNode | KeywordGreaterThanNode | KeywordLeftBraceNode | KeywordLeftParenNode
def transitions(
    current: NON_TERMINAL | TERMINAL, token: Token
) -> list[NON_TERMINAL | TERMINAL] | str | None:
    match current:
        case FunctionNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    res = (
                        KeywordfnNode(),
                        KeywordmainNode(),
                        BlockNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case BlockNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    res = (
                        KeywordLeftBraceNode(),
                        StatementsNode(),
                        KeywordRightBraceNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case StatementsNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    res = (
                        ReturnNode(),
                        KeywordSemicolonNode(),
                        StatementsNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="int"):
                    res = (
                        DeclarationNode(),
                        KeywordSemicolonNode(),
                        StatementsNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="for"):
                    res = (
                        LoopNode(),
                        StatementsNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    current.pos = token.start
                    return []
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    res = (
                        ReassignmentNode(),
                        KeywordSemicolonNode(),
                        StatementsNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    res = (
                        ConditionNode(),
                        StatementsNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case ReturnNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    res = (
                        KeywordreturnNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case DeclarationNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    res = (
                        KeywordintNode(),
                        IdentNode(),
                        KeywordEqualsNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case ReassignmentNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    res = (
                        IdentNode(),
                        KeywordEqualsNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case ExpressionNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    res = (
                        NumberNode(),
                        ExpressionTailNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    res = (
                        IdentNode(),
                        ExpressionTailNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    res = (
                        KeywordLeftParenNode(),
                        ExpressionNode(),
                        KeywordRightParenNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case ExpressionTailNode():
            match token:
                case Keyword(value="!="):
                    current.pos = token.start
                    return []
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    current.pos = token.start
                    return []
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    current.pos = token.start
                    return []
                case Keyword(value=")"):
                    current.pos = token.start
                    return []
                case Keyword(value="+"):
                    res = (
                        KeywordPlusNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value=";"):
                    current.pos = token.start
                    return []
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    current.pos = token.start
                    return []
                case Keyword(value="<"):
                    current.pos = token.start
                    return []
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    current.pos = token.start
                    return []
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case ConditionNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    res = (
                        KeywordifNode(),
                        KeywordLeftParenNode(),
                        LogicalNode(),
                        KeywordRightParenNode(),
                        BlockNode(),
                        ElseBranchNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case ElseBranchNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    current.pos = token.start
                    return []
                case Keyword(value="int"):
                    current.pos = token.start
                    return []
                case Keyword(value="for"):
                    current.pos = token.start
                    return []
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    current.pos = token.start
                    return []
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    current.pos = token.start
                    return []
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    res = (
                        KeywordelseNode(),
                        BlockNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="if"):
                    current.pos = token.start
                    return []
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case LogicalNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    res = (
                        ExpressionNode(),
                        CMPNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    res = (
                        ExpressionNode(),
                        CMPNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    res = (
                        ExpressionNode(),
                        CMPNode(),
                        ExpressionNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case CMPNode():
            match token:
                case Keyword(value="!="):
                    res = KeywordBangEqualsNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    res = KeywordGreaterThanEqualsNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    res = KeywordEqualsEqualsNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    res = KeywordLessThanEqualsNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="<"):
                    res = KeywordLessThanNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    res = KeywordGreaterThanNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case LoopNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    res = (
                        KeywordforNode(),
                        KeywordLeftParenNode(),
                        Loop_1Node(),
                        KeywordSemicolonNode(),
                        Loop_2Node(),
                        KeywordSemicolonNode(),
                        Loop_3Node(),
                        KeywordRightParenNode(),
                        BlockNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case Loop_1Node():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    res = DeclarationNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    current.pos = token.start
                    return []
                case Ident():
                    res = ReassignmentNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case Loop_2Node():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    res = LogicalNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    current.pos = token.start
                    return []
                case Ident():
                    res = LogicalNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    res = LogicalNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case Loop_3Node():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    return f"unexpected token: {token}" 
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    current.pos = token.start
                    return []
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    res = ReassignmentNode()
                    current.value = res
                    current.pos = token.start
                    return [res]
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case InitNode():
            match token:
                case Keyword(value="!="):
                    return f"unexpected token: {token}" 
                case Keyword(value="return"):
                    return f"unexpected token: {token}" 
                case Keyword(value="int"):
                    return f"unexpected token: {token}" 
                case Keyword(value="for"):
                    return f"unexpected token: {token}" 
                case EOF():
                    return f"unexpected token: {token}" 
                case Keyword(value="}"):
                    return f"unexpected token: {token}" 
                case Keyword(value="fn"):
                    res = (
                        FunctionNode(),
                        EOFNode(),
                    )

                    current.value = res
                    current.pos = token.start
                    return list(res)
                case Number():
                    return f"unexpected token: {token}" 
                case Keyword(value=">="):
                    return f"unexpected token: {token}" 
                case Keyword(value="="):
                    return f"unexpected token: {token}" 
                case Keyword(value="=="):
                    return f"unexpected token: {token}" 
                case Keyword(value=")"):
                    return f"unexpected token: {token}" 
                case Keyword(value="+"):
                    return f"unexpected token: {token}" 
                case Keyword(value=";"):
                    return f"unexpected token: {token}" 
                case Ident():
                    return f"unexpected token: {token}" 
                case Keyword(value="<="):
                    return f"unexpected token: {token}" 
                case Keyword(value="<"):
                    return f"unexpected token: {token}" 
                case Keyword(value="else"):
                    return f"unexpected token: {token}" 
                case Keyword(value="if"):
                    return f"unexpected token: {token}" 
                case Keyword(value="main"):
                    return f"unexpected token: {token}" 
                case Keyword(value=">"):
                    return f"unexpected token: {token}" 
                case Keyword(value="{"):
                    return f"unexpected token: {token}" 
                case Keyword(value="("):
                    return f"unexpected token: {token}" 
                case Keyword(value=unexpected):
                    return f"unknown keyword: {unexpected}" 
        case EOFNode():
            if type(token) != EOF:
                return f"expected EOF, but {type(token)} found" 
            current.value = token
            current.pos = token.start
            return None
        case NumberNode():
            if type(token) != Number:
                return f"expected Number, but {type(token)} found" 
            current.value = token
            current.pos = token.start
            return None
        case IdentNode():
            if type(token) != Ident:
                return f"expected Ident, but {type(token)} found" 
            current.value = token
            current.pos = token.start
            return None
        case KeywordBangEqualsNode():
            if type(token) != Keyword or token.value != "!=":
                return "expected !=, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordintNode():
            if type(token) != Keyword or token.value != "int":
                return "expected int, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordreturnNode():
            if type(token) != Keyword or token.value != "return":
                return "expected return, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordforNode():
            if type(token) != Keyword or token.value != "for":
                return "expected for, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordRightBraceNode():
            if type(token) != Keyword or token.value != "}":
                return "expected }, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordfnNode():
            if type(token) != Keyword or token.value != "fn":
                return "expected fn, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordGreaterThanEqualsNode():
            if type(token) != Keyword or token.value != ">=":
                return "expected >=, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordEqualsNode():
            if type(token) != Keyword or token.value != "=":
                return "expected =, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordEqualsEqualsNode():
            if type(token) != Keyword or token.value != "==":
                return "expected ==, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordRightParenNode():
            if type(token) != Keyword or token.value != ")":
                return "expected ), {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordPlusNode():
            if type(token) != Keyword or token.value != "+":
                return "expected +, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordSemicolonNode():
            if type(token) != Keyword or token.value != ";":
                return "expected ;, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordLessThanEqualsNode():
            if type(token) != Keyword or token.value != "<=":
                return "expected <=, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordLessThanNode():
            if type(token) != Keyword or token.value != "<":
                return "expected <, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordelseNode():
            if type(token) != Keyword or token.value != "else":
                return "expected else, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordifNode():
            if type(token) != Keyword or token.value != "if":
                return "expected if, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordmainNode():
            if type(token) != Keyword or token.value != "main":
                return "expected main, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordGreaterThanNode():
            if type(token) != Keyword or token.value != ">":
                return "expected >, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordLeftBraceNode():
            if type(token) != Keyword or token.value != "{":
                return "expected {, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None
        case KeywordLeftParenNode():
            if type(token) != Keyword or token.value != "(":
                return "expected (, {} found".format(token) 
            current.value = token
            current.pos = token.start
            return None


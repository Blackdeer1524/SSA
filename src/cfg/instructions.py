import abc
from dataclasses import dataclass, field
from typing import Literal, override


@dataclass
class Instruction(abc.ABC):
    @abc.abstractmethod
    def to_string(self) -> str: ...


@dataclass
class Phi(Instruction):
    lhs: str
    rhs: set[str] = field(init=False, default_factory=set)

    @override
    def to_string(self) -> str:
        return f"{self.lhs} = φ({', '.join([f'{var}' for var in self.rhs])})"


@dataclass
class Return(Instruction):
    data: str | int

    @override
    def to_string(self):
        return f"ret {self.data}"


@dataclass
class Mov(Instruction):
    lhs: str
    rhs: str | int

    @override
    def to_string(self):
        return f"{self.lhs} = {self.rhs}"


@dataclass
class Add(Instruction):
    lhs: str

    op1: str | int
    op2: str | int

    @override
    def to_string(self):
        return f"{self.lhs} = {self.op1} + {self.op2}"


@dataclass
class Cmp(Instruction):
    op1: str | int
    op2: str | int

    @override
    def to_string(self):
        return f"cmp {self.op1} {self.op2}"


@dataclass
class Jump(Instruction):
    kind: Literal["jlt", "jle", "je", "jne", "jgt", "jge", "jmp"]
    label: str

    @override
    def to_string(self):
        return f"{self.kind} {self.label}"
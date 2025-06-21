from collections import defaultdict
from src.cfg.dominators import DominatorComputer
from src.cfg.instructions import Add, Cmp, Mov, Phi, Return
from src.cfg.cfg import BasicBlock


def get_defining_blocks(entry: BasicBlock):
    res: dict[str, set[str]] = defaultdict(set)

    for bb in entry.traverse_preorder():
        for inst in bb.instructions:
            match inst:
                case Mov(lhs=lhs):
                    res[lhs].add(bb.name)
                case _:
                    ...
    return res


class SSAFormer:
    def __init__(
        self,
        entry: BasicBlock,
        dom_computer: DominatorComputer,
        name_to_bb: dict[str, BasicBlock],
        is_experiment: bool = False
    ):
        self.entry = entry
        self.inversed_dom_tree: dict[str, list[str]] = defaultdict(list)
        self.dom_computer = dom_computer

        dom_tree = self.dom_computer.get_dominator_tree()
        for child, parent in dom_tree.items():
            self.inversed_dom_tree[parent].append(child)

        self.name_to_bb = name_to_bb

        self.stacks: defaultdict[str, list[int]] = defaultdict(lambda: [])
        self.versions: defaultdict[str, int] = defaultdict(lambda: 0)
        
        self.visited_blocks : set[str] = set()
        self.EXPERIMENT = is_experiment

    def _new_version(self, s: str, local_stack: defaultdict[str, int]) -> str:
        v = self.versions[s]
        self.versions[s] += 1
        self.stacks[s].append(v)
        local_stack[s] += 1
        # if v == 0:
        #     return s
        return f"{s}{v}"

    def _stamp_version(self, s: str):
        v = self.stacks[s][-1]
        # if v == 0:
        #     return s
        return f"{s}{v}"

    def _rename_helper(self, bb: BasicBlock):
        if self.EXPERIMENT:
            if bb.name in self.visited_blocks:
                return
            self.visited_blocks.add(bb.name)

        local_stacks_len: defaultdict[str, int] = defaultdict(lambda: 0)
        for _, phi in bb.phi.items():
            phi.lhs = self._new_version(phi.lhs, local_stacks_len)

        for inst in bb.instructions:
            match inst:
                case Return() as ret:
                    if isinstance(ret.data, str):
                        ret.data = self._stamp_version(ret.data)
                case Mov() as mov:
                    if isinstance(mov.rhs, str):
                        mov.rhs = self._stamp_version(mov.rhs)

                    if isinstance(mov.lhs, str):
                        mov.lhs = self._new_version(mov.lhs, local_stacks_len)
                case Add() as add:
                    if isinstance(add.op1, str):
                        add.op1 = self._stamp_version(add.op1)
                    if isinstance(add.op2, str):
                        add.op2 = self._stamp_version(add.op2)
                    add.lhs = self._new_version(add.lhs, local_stacks_len)
                case Cmp() as cmp:
                    if isinstance(cmp.op1, str):
                        cmp.op1 = self._stamp_version(cmp.op1)
                    if isinstance(cmp.op2, str):
                        cmp.op2 = self._stamp_version(cmp.op2)
                case _:
                    pass

        for s in bb.succ:
            for var, phi in s.phi.items():
                if self.stacks.get(var) is None:
                    continue
                phi.rhs.add(self._stamp_version(var))

        if self.EXPERIMENT:
            for s in bb.succ:
                self._rename_helper(s)
        else:
            for dom_c in self.inversed_dom_tree[bb.name]:
                self._rename_helper(self.name_to_bb[dom_c])
            

        for var, stack_len in local_stacks_len.items():
            for _ in range(stack_len):
                self.stacks[var].pop()

    def insert_phi(self):
        DF = self.dom_computer.dominance_frontier()

        var_assigns = get_defining_blocks(self.entry)
        for var, var_blocks in var_assigns.items():
            for defining_block in var_blocks:
                q = [defining_block]
                while len(q) > 0:
                    top = q.pop()
                    var_front = DF[top]
                    for insertion_candidate in var_front:
                        block = self.name_to_bb[insertion_candidate]
                        if block.phi.get(var) is not None:
                            continue
                        block.phi[var] = Phi(var)
                        q.extend(DF[insertion_candidate])

    def transform(self):
        self.insert_phi()
        self._rename_helper(self.entry)

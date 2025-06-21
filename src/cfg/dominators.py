from collections import defaultdict
from copy import deepcopy
from typing import Optional
from src.cfg.cfg import BasicBlock
from src.table_synthesis.stream import Stream


class DominatorComputer:
    def __init__(self, entry: BasicBlock, name_to_block: dict[str, BasicBlock]):
        self.entry = entry

        self.vertices = name_to_block

        names = set(self.vertices.keys())
        self.dominators: dict[str, set[str]] = {}
        for name in names:
            self.dominators[name] = deepcopy(names)

        self.dominators[entry.name] = set((entry.name,))
        self.dom_tree: dict[str, str] = {}
        self.frontier: dict[str, set[str]] = defaultdict(set)

    def _compute_dominators_set_helper(self, cur: BasicBlock):
        old = deepcopy(self.dominators[cur.name])

        if len(cur.pred) == 0:
            return False

        first = self.dominators[cur.pred[0].name]
        self.dominators[cur.name] = set((cur.name,)).union(
            first.intersection(*(self.dominators[pred.name] for pred in cur.pred[1:]))
        )
        changed = len(old.symmetric_difference(self.dominators[cur.name])) > 0
        return changed

    def _compute_dominators_set(self):
        q: list[BasicBlock] = []

        while True:
            q.append(self.entry)
            changed = False
            seen: set[str] = set()
            while len(q) > 0:
                top = q.pop()
                if top.name in seen:
                    continue
                seen.add(top.name)

                changed = self._compute_dominators_set_helper(top) or changed
                for s in top.succ:
                    q.append(s)
            if not changed:
                break

        return self.dominators

    def get_dominator_tree(self) -> dict[str, str]:
        dominators = self._compute_dominators_set()

        res: dict[str, str] = {}
        for vertex, doms in dominators.items():
            max_depth = 0
            deepest_dom = vertex
            for dom in doms:
                if dom == vertex:
                    continue

                if len(dominators[dom]) > max_depth:
                    deepest_dom = dom
                    max_depth = len(dominators[dom])
            res[vertex] = deepest_dom
        res.pop(self.entry.name)
        self.dom_tree = res
        return res

    def dominance_frontier(self) -> dict[str, set[str]]:
        if self.frontier != {}:
            return self.frontier

        if self.dom_tree == {}:
            self.get_dominator_tree()

        self.frontier: dict[str, set[str]] = defaultdict(set)
        for cur, bb in self.vertices.items():
            for pred in (p.name for p in bb.pred):
                while pred != self.dom_tree[cur]:
                    self.frontier[pred].add(cur)
                    pred = self.dom_tree[pred]
        return self.frontier 


def draw_dom_tree_edges(tree: dict[str, str]) -> str:
    ss = Stream()
    for child, parent in tree.items():
        ss.push_line(f'\t{parent} -> {child} [color="blue"]')
    return ss.emit()


def draw_dom_frontier(frontier: dict[str, set[str]]) -> str:
    ss = Stream()
    for parent, children in frontier.items():
        for child in children:
            ss.push_line(f'\t{parent} -> {child} [color="red"]')
    return ss.emit()

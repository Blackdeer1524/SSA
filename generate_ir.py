import sys
from src.cfg.phi import SSAFormer
from src.cfg.dominators import DominatorComputer, draw_dom_tree_edges
from src.analysis.task_analyzer import SyntacticAnalyzer
from src.scanning.task_scanner import Scanner
from src.cfg.cfg import build_cfg, generate_IR, get_graph


def main():
    scanner = Scanner(open(sys.argv[1]))
    syn_an = SyntacticAnalyzer(scanner)

    res = syn_an.parse()
    entry = build_cfg(res)

    name_to_block = get_graph(entry)
    computer = DominatorComputer(entry, name_to_block)

    former = SSAFormer(entry, computer, name_to_block)
    former.transform()

    print(generate_IR(entry))


if __name__ == "__main__":
    main()

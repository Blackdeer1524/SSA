import sys
from src.scanning.task_scanner import Scanner
from src.analysis.task_analyzer import SyntacticAnalyzer


def main():
    scanner = Scanner(open(sys.argv[1]))
    syn_an = SyntacticAnalyzer(scanner)

    res = syn_an.parse()
    print("digraph {")
    print(res.to_graphviz().replace("\r", "\\n"))
    print("}")


if __name__ == "__main__":
    main()

.PHONY: transitions 
	
transitions:
	python3.12 generate_transitions.py language.gr > src/analysis/task_transitions.py

ast_graph: transitions
	python3.12 generate_graph.py input.txt > ast_graph.dot
	dot -Tsvg ast_graph.dot -o ast_graph.svg
	xdg-open ast_graph.svg
	
cfg: transitions
	python3.12 generate_cfg.py input.txt > cfg.dot
	dot -Tsvg cfg.dot -o cfg.svg
	xdg-open cfg.svg

ir: transitions
	python3.12 generate_ir.py input.txt > output.txt

main: cfg
	python3.12 main.py input.txt


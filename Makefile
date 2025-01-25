.PHONY: all plots readme test

all: plots readme

plots:
	python -m src.plotting.qubit_count_plot
	python -m src.plotting.entangled_error_plot
	python -m src.plotting.qec_time_plot
	python -m src.plotting.nkd_plot

readme:
	python -m src.markdown.generator

test:
	pytest tests/ 
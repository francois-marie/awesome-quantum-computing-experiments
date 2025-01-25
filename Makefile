.PHONY: test plots readme clean

test:
	pytest tests/

plots:
	python -m src.plotting.qubit_count_plot
	python -m src.plotting.entangled_error_plot
	python -m src.plotting.qec_time_plot
	python -m src.plotting.nkd_plot

readme:
	python -m src.markdown.generator

clean:
	rm -f out/plots/*

all: clean plots readme 
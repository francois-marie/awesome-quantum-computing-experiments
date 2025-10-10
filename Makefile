.PHONY: all plots readme test clean setup

all: setup plots readme

plots: setup
	python -m src.plotting.experiment_count_plot
	python -m src.plotting.experiment_count_yearly_plot
	python -m src.plotting.qec_platform_sunburst
	python -m src.plotting.qec_timeline_plot
	python -m src.plotting.entangled_error_plot
	python -m src.plotting.qubit_count_plot
	python -m src.plotting.coherence_times_plot
	python -m src.plotting.nkd_plot
	python -m src.plotting.qec_cumulative_plot
	python -m src.plotting.qec_qubit_count_plot
	python -m src.plotting.msd_plot
	python -m src.plotting.msd_error_evolution_plot

# Alternative way to generate all plots at once
generate_all: setup
	python -m src.plotting.generate_all_plots

# Export all plots to PDF
export_pdf: setup
	python -m src.plotting.export_all_to_pdf

readme:
	python -m src.markdown.generator

test:
	pytest tests/

clean:
	rm -rf out/js/*.js
	rm -rf out/pdf/*.pdf
	rm -rf out/png/*.png
	rm -rf out/plots/*.png
	mkdir -p out/js out/pdf out/png out/plots

# Ensure required directories exist
setup:
	mkdir -p out/js out/pdf out/png out/plots 
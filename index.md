---
layout: default
title: Home
nav_order: 1
---

# Awesome Quantum Computing Experiments

A comprehensive collection of notable quantum computing experiments, focusing on implementations of quantum error correction codes and other key metrics.

## Latest Highlights

{% include metrics_grid.html %}

## Visualizations

<!-- Include Plotly library -->
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>


### Cumulative Experiment Counts by Platform
<div id="experiment-counts" style="width:100%; height:800px;"></div>

### Yearly Experiment Counts by Platform
<div id="experiment-counts-yearly" style="width:100%; height:800px;"></div>

### QEC Platform Distribution
<div id="qec-platform-sunburst" style="width:100%; height:800px;"></div>


### Timeline of QEC Implementations
<div id="qec-timeline-scatter" style="width:100%; height:800px;"></div>

### [[n, k, d]] Distribution
<div id="nkd-plot" style="width:100%; height:800px;"></div>

### Entangled State Error Progress
<div id="entangled-error-plot" style="width:100%; height:800px;"></div>

### Qubit Count Evolution
<div id="qubit-count-plot" style="width:100%; height:800px;"></div>

### Physical Qubit Coherence Times
<div id="coherence-times-plot" style="width:100%; height:800px;"></div>

### Cumulative Experiment Counts by QEC Code
<div id="qec-cumulative-growth" style="width:100%; height:800px;"></div>

<!-- Load plot scripts -->
<script src="out/js/experiment_counts.js"></script>
<script src="out/js/experiment_counts_yearly.js"></script>
<script src="out/js/qec_platform_sunburst.js"></script>
<script src="out/js/qec_timeline.js"></script>
<script src="out/js/nkd_plot.js"></script>
<script src="out/js/entangled_error_plot.js"></script>
<script src="out/js/qubit_count_plot.js"></script>
<script src="out/js/coherence_times_plot.js"></script>
<script src="out/js/qec_cumulative_growth.js"></script>

## About

This database tracks:
- Quantum Error Correction (QEC) implementations
- Magic State Distillation (MSD) experiments
- Entangled State Error measurements
- Physical Qubit Count evolution


[View on GitHub <i class="fa-brands fa-github"></i>](https://github.com/francois-marie/awesome-quantum-computing-experiments){: .button} 

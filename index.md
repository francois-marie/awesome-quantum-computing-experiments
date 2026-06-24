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

<!-- Mobile-friendly plot sections -->
### Physical Qubit Coherence Times
<div class="plot-section">
    <div id="coherence-times-plot" class="plot-container"></div>
</div>

### Entangled State Error Progress
<div class="plot-section">
    <div id="entangled-error-plot" class="plot-container"></div>
</div>

### Qubit Count Evolution
<div class="plot-section">
    <div id="qubit-count-plot" class="plot-container"></div>
</div>

### Magic State Preparation: Error vs Acceptance Rate
<div class="plot-section">
    <div id="msd-plot" class="plot-container"></div>
</div>

### Magic State Error Evolution Over Time
<div class="plot-section">
    <div id="msd-error-evolution-plot" class="plot-container"></div>
</div>

<!-- High-level visualizations -->
### Cumulative Experiment Counts by Platform
<div class="plot-section">
    <div id="experiment-counts" class="plot-container"></div>
</div>

### [[n, k, d]] Distribution
<div class="plot-section">
    <div id="nkd-plot-aggregated" class="plot-container"></div>
</div>

### Yearly Experiment Counts by Platform
<div class="plot-section">
    <div id="experiment-counts-yearly" class="plot-container"></div>
</div>

### Cumulative Growth of QEC Implementations Over Time
<div class="plot-section">
    <div id="qec-cumulative-growth" class="plot-container"></div>
</div>

### Aggregated Timeline of Quantum Error Correction Implementations
<div class="plot-section">
    <div id="qec-timeline-aggregated-scatter" class="plot-container"></div>
</div>

### Distribution of QEC Implementations Across Platforms
<div class="plot-section">
    <div id="qec-platform-sunburst" class="plot-container"></div>
</div>



<!-- Load plot scripts from gh-pages-assets via jsDelivr (commit pinned in _data/plot_assets.yml) -->
{% include plot_scripts.html %}

<!-- Load responsive plot enhancement script -->
<script src="{{ '/assets/js/responsive-plots.js' | relative_url }}"></script>

## About

This database tracks:
- Quantum Error Correction (QEC) implementations
- Magic State Distillation (MSD) experiments
- Entangled State Error measurements
- Physical Qubit Count evolution


[View on GitHub <i class="fa-brands fa-github"></i>](https://github.com/francois-marie/awesome-quantum-computing-experiments){: .button} 

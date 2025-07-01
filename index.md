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
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('coherence-times-plot')">
            <h4>Coherence Times Evolution</h4>
            <p>📈 Tap to view interactive plot</p>
            <div class="preview-stats">
                <span>T1 & T2 evolution across platforms</span>
            </div>
        </div>
    </div>
    <div id="coherence-times-plot" class="plot-container desktop-only"></div>
</div>

### Entangled State Error Progress
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('entangled-error-plot')">
            <h4>Entanglement Error vs. Year</h4>
            <p>📈 Tap to view interactive plot</p>
            <div class="preview-stats">
                <span>Error reduction progress over time</span>
            </div>
        </div>
    </div>
    <div id="entangled-error-plot" class="plot-container desktop-only"></div>
</div>

### Qubit Count Evolution
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('qubit-count-plot')">
            <h4>Physical Qubit Count Evolution</h4>
            <p>📈 Tap to view interactive plot</p>
            <div class="preview-stats">
                <span>Qubit scaling across platforms</span>
            </div>
        </div>
    </div>
    <div id="qubit-count-plot" class="plot-container desktop-only"></div>
</div>

<!-- High-level visualizations -->
### Cumulative Experiment Counts by Platform
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('experiment-counts')">
            <h4>Experiment Counts by Platform</h4>
            <p>📊 Tap to view interactive plot</p>
        </div>
    </div>
    <div id="experiment-counts" class="plot-container desktop-only"></div>
</div>

### [[n, k, d]] Distribution
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('nkd-plot-aggregated')">
            <h4>QEC Code Parameters</h4>
            <p>📊 Tap to view 3D interactive plot</p>
        </div>
    </div>
    <div id="nkd-plot-aggregated" class="plot-container desktop-only"></div>
</div>

### Yearly Experiment Counts by Platform
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('experiment-counts-yearly')">
            <h4>Yearly Experiment Trends</h4>
            <p>📊 Tap to view interactive plot</p>
        </div>
    </div>
    <div id="experiment-counts-yearly" class="plot-container desktop-only"></div>
</div>

### Cumulative Growth of QEC Implementations Over Time
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('qec-cumulative-growth')">
            <h4>QEC Growth Over Time</h4>
            <p>📈 Tap to view interactive plot</p>
        </div>
    </div>
    <div id="qec-cumulative-growth" class="plot-container desktop-only"></div>
</div>

### Aggregated Timeline of Quantum Error Correction Implementations
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('qec-timeline-aggregated-scatter')">
            <h4>QEC Implementation Timeline</h4>
            <p>📊 Tap to view interactive plot</p>
        </div>
    </div>
    <div id="qec-timeline-aggregated-scatter" class="plot-container desktop-only"></div>
</div>

### Distribution of QEC Implementations Across Platforms
<div class="plot-section">
    <div class="plot-preview mobile-only">
        <div class="plot-thumbnail" onclick="openPlotModal('qec-platform-sunburst')">
            <h4>Platform Distribution</h4>
            <p>🌞 Tap to view sunburst chart</p>
        </div>
    </div>
    <div id="qec-platform-sunburst" class="plot-container desktop-only"></div>
</div>

<!-- Modal for mobile plot viewing -->
<div id="plot-modal" class="plot-modal mobile-only">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="modal-title">Interactive Plot</h3>
            <button class="close-btn" onclick="closePlotModal()">&times;</button>
        </div>
        <div id="modal-plot-container" class="modal-plot-container"></div>
        <div class="modal-instructions">
            <p>💡 Pinch to zoom the image, or tap the X to close</p>
        </div>
    </div>
</div>

<!-- Load plot scripts -->
<script src="{{ '/out/js/coherence_times_plot.js' | relative_url }}"></script>
<script src="{{ '/out/js/entangled_error_plot.js' | relative_url }}"></script>
<script src="{{ '/out/js/qubit_count_plot.js' | relative_url }}"></script>
<script src="{{ '/out/js/experiment_counts.js' | relative_url }}"></script>
<script src="{{ '/out/js/nkd_plot_aggregated.js' | relative_url }}"></script>
<script src="{{ '/out/js/experiment_counts_yearly.js' | relative_url }}"></script>
<script src="{{ '/out/js/qec_cumulative_growth.js' | relative_url }}"></script>
<script src="{{ '/out/js/qec_timeline_aggregated.js' | relative_url }}"></script>
<script src="{{ '/out/js/qec_platform_sunburst.js' | relative_url }}"></script>

## About

This database tracks:
- Quantum Error Correction (QEC) implementations
- Magic State Distillation (MSD) experiments
- Entangled State Error measurements
- Physical Qubit Count evolution


[View on GitHub <i class="fa-brands fa-github"></i>](https://github.com/francois-marie/awesome-quantum-computing-experiments){: .button} 

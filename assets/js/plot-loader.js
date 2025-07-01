function createQubitCountPlot(data) {
    const platforms = [...new Set(data.map(d => d.Platform))];
    const traces = platforms.map(platform => {
        const platformData = data.filter(d => d.Platform === platform);
        return {
            name: platform,
            type: 'scatter',
            mode: 'lines+markers',
            x: platformData.map(d => d.Year),
            y: platformData.map(d => d['Number of qubits']),
            text: platformData.map(d => d['Article Title']),
            customdata: platformData.map(d => d.Link || d.DOI || ''),
            hovertemplate: 
                '<b>%{text}</b><br>' +
                'Qubits: %{y}<br>' +
                'Year: %{x}<br>' +
                '%{customdata}<extra></extra>'
        };
    });

    const isMobile = window.innerWidth < 768;
    
    const layout = {
        title: {
            text: 'Number of Qubits vs. Year by Platform',
            font: { size: isMobile ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            titlefont: { size: isMobile ? 12 : 14 },
            tickfont: { size: isMobile ? 10 : 12 }
        },
        yaxis: { 
            title: 'Number of Qubits',
            type: 'log',
            titlefont: { size: isMobile ? 12 : 14 },
            tickfont: { size: isMobile ? 10 : 12 }
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            font: { size: isMobile ? 9 : 12 }
        },
        margin: {
            l: isMobile ? 60 : 80,
            r: isMobile ? 20 : 80,
            t: isMobile ? 60 : 80,
            b: isMobile ? 50 : 80
        },
        autosize: true
    };

    const config = {
        responsive: true,
        displayModeBar: !isMobile,
        modeBarButtons: [['zoom2d', 'pan2d', 'resetScale2d', 'toImage']]
    };

    Plotly.newPlot('qubit-count-plot', traces, layout, config);
}

function createQECTimelinePlot(data) {
    // Group data by platform
    const platforms = [...new Set(data.map(d => d.Platform))];
    const traces = platforms.map(platform => {
        const platformData = data.filter(d => d.Platform === platform);
        return {
            name: platform,
            type: 'scatter',
            mode: 'markers',
            x: platformData.map(d => d.Year),
            y: Array(platformData.length).fill(platform),
            text: platformData.map(d => `${d['Code Name']}<br>${d['Code Parameters']}`),
            hovertemplate: '%{text}<br>Year: %{x}<extra></extra>',
            marker: { size: 10 }
        };
    });

    const layout = {
        title: {
            text: 'Time Evolution of Quantum Error Correction Experiments',
            font: { size: window.innerWidth < 768 ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        yaxis: { 
            title: 'Platform',
            type: 'category',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        hovermode: 'closest',
        margin: {
            l: window.innerWidth < 768 ? 50 : 80,
            r: window.innerWidth < 768 ? 50 : 80,
            t: window.innerWidth < 768 ? 50 : 80,
            b: window.innerWidth < 768 ? 50 : 80
        }
    };

    const config = {
        responsive: true,
        displayModeBar: window.innerWidth >= 768,
        modeBarButtons: [['zoom2d', 'pan2d', 'resetScale2d', 'toImage']]
    };

    Plotly.newPlot('qec-timeline-plot', traces, layout, config);
}

function createNKDPlot(data) {
    const trace = {
        type: 'scatter3d',
        mode: 'markers',
        x: data.map(d => d.n),
        y: data.map(d => d.k),
        z: data.map(d => d.d),
        text: data.map(d => d.Platform),
        hovertemplate: 
            'n: %{x}<br>' +
            'k: %{y}<br>' +
            'd: %{z}<br>' +
            'Platform: %{text}<extra></extra>',
        marker: {
            size: 5,
            color: data.map(d => d.Year),
            colorscale: 'Viridis',
            colorbar: {title: 'Year'}
        }
    };

    const layout = {
        title: {
            text: '[[n,k,d]] Code Parameter Distribution',
            font: { size: window.innerWidth < 768 ? 14 : 18 }
        },
        scene: {
            xaxis: {
                title: 'n (physical qubits)',
                titlefont: { size: window.innerWidth < 768 ? 10 : 12 }
            },
            yaxis: {
                title: 'k (logical qubits)',
                titlefont: { size: window.innerWidth < 768 ? 10 : 12 }
            },
            zaxis: {
                title: 'd (distance)',
                titlefont: { size: window.innerWidth < 768 ? 10 : 12 }
            }
        },
        margin: {
            l: window.innerWidth < 768 ? 20 : 40,
            r: window.innerWidth < 768 ? 20 : 40,
            t: window.innerWidth < 768 ? 40 : 60,
            b: window.innerWidth < 768 ? 20 : 40
        }
    };

    const config = {
        responsive: true,
        displayModeBar: window.innerWidth >= 768,
        modeBarButtons: [['zoom3d', 'pan3d', 'resetCameraDefault3d', 'toImage']]
    };

    Plotly.newPlot('nkd-plot', [trace], layout, config);
}

function createEntangledErrorPlot(data) {
    const platforms = [...new Set(data.map(d => d.Platform))];
    const traces = platforms.map(platform => {
        const platformData = data.filter(d => d.Platform === platform);
        return {
            name: platform,
            type: 'scatter',
            mode: 'lines+markers',
            x: platformData.map(d => d.Year),
            y: platformData.map(d => d['Entangled State Error']),
            text: platformData.map(d => d['Article Title']),
            customdata: platformData.map(d => d.Link || d.DOI || ''),
            hovertemplate: 
                '<b>%{text}</b><br>' +
                'Error: %{y}<br>' +
                'Year: %{x}<br>' +
                '%{customdata}<extra></extra>'
        };
    });

    const isMobile = window.innerWidth < 768;

    const layout = {
        title: {
            text: 'Entangled State Error vs. Year',
            font: { size: isMobile ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            titlefont: { size: isMobile ? 12 : 14 },
            tickfont: { size: isMobile ? 10 : 12 }
        },
        yaxis: { 
            title: 'Entangled State Error',
            type: 'log',
            titlefont: { size: isMobile ? 12 : 14 },
            tickfont: { size: isMobile ? 10 : 12 }
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            font: { size: isMobile ? 9 : 12 }
        },
        margin: {
            l: isMobile ? 60 : 80,
            r: isMobile ? 20 : 80,
            t: isMobile ? 60 : 80,
            b: isMobile ? 50 : 80
        },
        autosize: true
    };

    const config = {
        responsive: true,
        displayModeBar: !isMobile,
        modeBarButtons: [['zoom2d', 'pan2d', 'resetScale2d', 'toImage']]
    };

    Plotly.newPlot('entangled-error-plot', traces, layout, config);
}

function createCoherenceTimesPlot(data) {
    const platforms = [...new Set(data.map(d => d.Platform))];
    const traces = [];
    
    platforms.forEach(platform => {
        const platformData = data.filter(d => d.Platform === platform);
        
        // T1 trace
        const t1Data = platformData.filter(d => d.T1 && d.T1 !== '');
        if (t1Data.length > 0) {
            traces.push({
                name: `${platform} (T1)`,
                type: 'scatter',
                mode: 'lines+markers',
                x: t1Data.map(d => d.Year),
                y: t1Data.map(d => d.T1),
                text: t1Data.map(d => d['Article Title'] || d['Code Name']),
                customdata: t1Data.map(d => d.Link || ''),
                hovertemplate: 
                    '<b>%{text}</b><br>' +
                    'T1: %{y}s<br>' +
                    'Year: %{x}<br>' +
                    '%{customdata}<extra></extra>',
                marker: { symbol: 'circle' }
            });
        }
        
        // T2 trace
        const t2Data = platformData.filter(d => d.T2 && d.T2 !== '');
        if (t2Data.length > 0) {
            traces.push({
                name: `${platform} (T2)`,
                type: 'scatter',
                mode: 'lines+markers',
                x: t2Data.map(d => d.Year),
                y: t2Data.map(d => d.T2),
                text: t2Data.map(d => d['Article Title'] || d['Code Name']),
                customdata: t2Data.map(d => d.Link || ''),
                hovertemplate: 
                    '<b>%{text}</b><br>' +
                    'T2: %{y}s<br>' +
                    'Year: %{x}<br>' +
                    '%{customdata}<extra></extra>',
                marker: { symbol: 'circle-open' }
            });
        }
    });

    const isMobile = window.innerWidth < 768;

    const layout = {
        title: {
            text: 'Evolution of Qubit Coherence Times',
            font: { size: isMobile ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            dtick: 1,
            titlefont: { size: isMobile ? 12 : 14 },
            tickfont: { size: isMobile ? 10 : 12 }
        },
        yaxis: { 
            title: 'Coherence Time (s)',
            type: 'log',
            titlefont: { size: isMobile ? 12 : 14 },
            tickfont: { size: isMobile ? 10 : 12 }
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            font: { size: isMobile ? 9 : 12 }
        },
        margin: {
            l: isMobile ? 60 : 80,
            r: isMobile ? 20 : 80,
            t: isMobile ? 60 : 80,
            b: isMobile ? 50 : 80
        },
        autosize: true
    };

    const config = {
        responsive: true,
        displayModeBar: !isMobile,
        modeBarButtons: [['zoom2d', 'pan2d', 'resetScale2d', 'toImage']]
    };

    Plotly.newPlot('coherence-times-plot', traces, layout, config);
}

// Window resize handler for mobile responsiveness
window.addEventListener('resize', function() {
    // Debounce resize events
    clearTimeout(window.resizeTimer);
    window.resizeTimer = setTimeout(function() {
        // List of all plot element IDs
        const plotIds = [
            'coherence-times-plot',
            'entangled-error-plot', 
            'qubit-count-plot',
            'experiment-counts',
            'nkd-plot-aggregated',
            'experiment-counts-yearly',
            'qec-cumulative-growth',
            'qec-timeline-aggregated-scatter',
            'qec-platform-sunburst',
            'qec-data-qubit-count-plot'
        ];
        
        // Properly resize all existing plots
        plotIds.forEach(plotId => {
            const plotDiv = document.getElementById(plotId);
            if (plotDiv && plotDiv.data && plotDiv.layout) {
                // Use Plotly's responsive resize which respects autosize
                Plotly.Plots.resize(plotId);
            }
        });
    }, 150); // Slightly longer debounce for better performance
});

// Make functions globally available immediately
window.openPlotModal = function(plotId) {
    console.log('Opening modal for plot:', plotId);
    
    const modal = document.getElementById('plot-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalPlotContainer = document.getElementById('modal-plot-container');
    
    if (!modal || !modalTitle || !modalPlotContainer) {
        console.error('Modal elements not found');
        alert('Modal elements not found. Please check the page setup.');
        return;
    }
    
    // Reset modal to clean state first
    resetModalState(modal, modalPlotContainer);
    
    // Set modal title based on plot
    const plotTitles = {
        'coherence-times-plot': 'Physical Qubit Coherence Times',
        'entangled-error-plot': 'Entangled State Error Progress',
        'qubit-count-plot': 'Qubit Count Evolution',
        'experiment-counts': 'Experiment Counts by Platform',
        'nkd-plot-aggregated': '[[n,k,d]] Distribution',
        'experiment-counts-yearly': 'Yearly Experiment Trends',
        'qec-cumulative-growth': 'QEC Growth Over Time',
        'qec-timeline-aggregated-scatter': 'QEC Implementation Timeline',
        'qec-platform-sunburst': 'Platform Distribution'
    };
    
    modalTitle.textContent = plotTitles[plotId] || 'Interactive Plot';
    
    // Map plot IDs to PNG file names
    const plotImageMap = {
        'coherence-times-plot': 'coherence_times_plot.png',
        'entangled-error-plot': 'entangled_error_plot.png',
        'qubit-count-plot': 'qubit_count_plot.png',
        'experiment-counts': 'experiment_counts.png',
        'nkd-plot-aggregated': 'nkd_plot_aggregated.png',
        'experiment-counts-yearly': 'experiment_counts_yearly.png',
        'qec-cumulative-growth': 'qec_cumulative_growth.png',
        'qec-timeline-aggregated-scatter': 'qec_timeline_aggregated.png',
        'qec-platform-sunburst': 'qec_platform_sunburst.png'
    };
    
    const imageName = plotImageMap[plotId];
    if (!imageName) {
        console.error('No image mapping found for plot:', plotId);
        modalPlotContainer.innerHTML = '<div style="padding: 2rem; text-align: center; color: #666;">Plot image not found.</div>';
        return;
    }
    
    // Show loading indicator immediately
    modalPlotContainer.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; height: 100%; flex-direction: column; color: #666;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">Loading plot...</div>
            <div style="font-size: 0.9rem;">Please wait a moment</div>
        </div>
    `;
    
    // Show modal using CSS classes
    modal.classList.remove('hidden');
    modal.classList.add('show');
    modal.style.display = 'flex';
    modal.style.visibility = 'visible';
    modal.style.opacity = '1';
    document.body.style.overflow = 'hidden';
    document.body.classList.add('modal-open');
    
    console.log('Modal should now be visible. Classes:', modal.className);
    
    // Create image element and load the PNG
    const baseUrl = window.location.pathname.includes('/awesome-quantum-computing-experiments') 
        ? '/awesome-quantum-computing-experiments' 
        : '';
    const imageUrl = `${baseUrl}/out/png/${imageName}`;
    console.log('Loading image:', imageUrl);
    
    const img = new Image();
    img.onload = function() {
        console.log('Image loaded successfully');
        modalPlotContainer.innerHTML = `
            <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 1rem; box-sizing: border-box;">
                <img src="${imageUrl}" 
                     alt="${plotTitles[plotId] || 'Plot'}" 
                     style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            </div>
        `;
    };
    
    img.onerror = function() {
        console.error('Failed to load image:', imageUrl);
        modalPlotContainer.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: #666;">
                <p>Failed to load plot image.</p>
                <p><small>Image path: ${imageUrl}</small></p>
                <button onclick="closePlotModal()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
            </div>
        `;
    };
    
    // Start loading the image
    img.src = imageUrl;
};

window.closePlotModal = function() {
    console.log('Attempting to close modal');
    
    const modal = document.getElementById('plot-modal');
    const modalPlotContainer = document.getElementById('modal-plot-container');
    
    if (!modal) {
        console.error('Modal not found for closing');
        return;
    }
    
    console.log('Modal before closing. Classes:', modal.className);
    
    // Reset modal to clean state
    resetModalState(modal, modalPlotContainer);
    
    // Hide modal using CSS class
    modal.classList.add('hidden');
    modal.style.display = 'none';
    
    console.log('Modal after closing. Classes:', modal.className);
    console.log('Modal closed successfully');
    
    // Force a reflow to ensure changes are applied
    modal.offsetHeight;
};

function resetModalState(modal, modalPlotContainer) {
    console.log('Resetting modal state');
    
    // Clear any existing content
    if (modalPlotContainer) {
        modalPlotContainer.innerHTML = '';
    }
    
    // Reset all CSS properties to initial state
    modal.classList.remove('show', 'hidden');
    modal.style.display = '';
    modal.style.visibility = '';
    modal.style.opacity = '';
    
    // Ensure body scroll is restored
    document.body.style.overflow = 'auto';
    document.body.classList.remove('modal-open');
    
    console.log('Modal state reset complete');
}

// Close modal when clicking outside content or pressing escape
document.addEventListener('DOMContentLoaded', function() {
    console.log('Setting up modal event listeners');
    
    const modal = document.getElementById('plot-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                console.log('Clicked outside modal, closing');
                closePlotModal();
            }
        });
        console.log('Modal click listener added');
    } else {
        console.error('Modal element not found during setup');
    }
    
    // Handle escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            console.log('Escape key pressed, closing modal');
            closePlotModal();
        }
    });
    
    console.log('Modal setup complete');
});

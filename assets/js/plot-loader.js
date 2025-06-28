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

    const layout = {
        title: {
            text: 'Number of Qubits vs. Year by Platform',
            font: { size: window.innerWidth < 768 ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        yaxis: { 
            title: 'Number of Qubits',
            type: 'log',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            font: { size: window.innerWidth < 768 ? 10 : 12 }
        },
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

    const layout = {
        title: {
            text: 'Entangled State Error vs. Year',
            font: { size: window.innerWidth < 768 ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        yaxis: { 
            title: 'Entangled State Error',
            type: 'log',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            font: { size: window.innerWidth < 768 ? 10 : 12 }
        },
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

    const layout = {
        title: {
            text: 'Evolution of Qubit Coherence Times',
            font: { size: window.innerWidth < 768 ? 14 : 18 }
        },
        xaxis: { 
            title: 'Year',
            dtick: 1,
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        yaxis: { 
            title: 'Coherence Time (s)',
            type: 'log',
            titlefont: { size: window.innerWidth < 768 ? 12 : 14 }
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            font: { size: window.innerWidth < 768 ? 10 : 12 }
        },
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
        
        // Resize all existing plots
        plotIds.forEach(plotId => {
            const plotDiv = document.getElementById(plotId);
            if (plotDiv && plotDiv.data) {
                Plotly.Plots.resize(plotId);
            }
        });
    }, 100);
});

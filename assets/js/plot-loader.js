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
        title: 'Number of Qubits vs. Year by Platform',
        xaxis: { title: 'Year' },
        yaxis: { 
            title: 'Number of Qubits',
            type: 'log'
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
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
        title: 'Time Evolution of Quantum Error Correction Experiments',
        xaxis: { title: 'Year' },
        yaxis: { 
            title: 'Platform',
            type: 'category'
        },
        hovermode: 'closest'
    };

    Plotly.newPlot('qec-timeline-plot', traces, layout);
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
        title: '[[n,k,d]] Code Parameter Distribution',
        scene: {
            xaxis: {title: 'n (physical qubits)'},
            yaxis: {title: 'k (logical qubits)'},
            zaxis: {title: 'd (distance)'}
        }
    };

    Plotly.newPlot('nkd-plot', [trace], layout);
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
        title: 'Entangled State Error vs. Year',
        xaxis: { title: 'Year' },
        yaxis: { 
            title: 'Entangled State Error',
            type: 'log'
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
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
        title: 'Evolution of Qubit Coherence Times',
        xaxis: { 
            title: 'Year',
            dtick: 1  // Force integer ticks
        },
        yaxis: { 
            title: 'Coherence Time (s)',
            type: 'log'
        },
        hovermode: 'closest',
        showlegend: true,
        legend: {
            x: 0,
            y: 1
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtons: [['zoom2d', 'pan2d', 'resetScale2d', 'toImage']]
    };

    Plotly.newPlot('coherence-times-plot', traces, layout, config);
}

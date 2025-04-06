function loadCSV(url, tableId) {
    Papa.parse(url, {
        download: true,
        header: true,
        complete: function(results) {
            console.log(`Loading table ${tableId}`);
            
            if (results.data.length === 0 || !results.data[0]) {
                console.warn(`No data found for ${tableId}`);
                $(`#${tableId}`).after(`<div class="info-message">No data available yet. Please contribute by adding entries!</div>`);
                return;
            }
            
            if (tableId === 'qubit-count-table') {
                results.data = results.data.filter(row => {
                    const qubitValue = row['Number of qubits'];
                    return qubitValue && qubitValue.toString().trim() !== '';
                });
            }
            
            function findColumn(headers, possibilities) {
                for (let possible of possibilities) {
                    let found = headers.find(h => 
                        h.toLowerCase().replace(/[^a-z0-9]/g, '') === 
                        possible.toLowerCase().replace(/[^a-z0-9]/g, '')
                    );
                    if (found) return found;
                }
                return null;
            }

            const headers = Object.keys(results.data[0] || {});
            let columnDefs;
            switch(tableId) {
                case 'qec-table':
                    // Filter out any empty rows
                    results.data = results.data.filter(row => 
                        row['Year'] && row['Year'].toString().trim() !== ''
                    );
                    
                    columnDefs = [
                        { 
                            title: "Year",
                            data: "Year",
                            type: "num"  // Specify that this is a numeric column
                        },
                        { 
                            title: "Platform",
                            data: "Platform"
                        },
                        {
                            title: "Code Name",
                            data: "Code Name"
                        },
                        {
                            title: "Code Parameters",
                            data: "Code Parameters"
                        },
                        { 
                            title: "Link",
                            data: "Link",
                            render: function(data) {
                                return data ? `<a href="${data}" target="_blank">Link</a>` : '';
                            }
                        }
                    ];
                    break;
                case 'qubit-count-table':
                    const yearCol = findColumn(headers, ["Year", "year", "Date", "date"]);
                    const platformCol = findColumn(headers, ["Platform", "platform", "Implementation", "Type", "type"]);
                    const qubitCol = findColumn(headers, ["Qubit Count", "qubit_count", "Qubits", "Number of Qubits", "qubits", "count"]);
                    const linkCol = findColumn(headers, ["Link", "URL", "DOI", "link", "doi", "url"]);
                    
                    console.log('Column matches for qubit-count-table:', {
                        yearCol,
                        platformCol,
                        qubitCol,
                        linkCol
                    });

                    columnDefs = [
                        { 
                            title: "Year",
                            data: yearCol || "date"
                        },
                        { 
                            title: "Platform",
                            data: platformCol || "type"
                        },
                        { 
                            title: "Qubit Count",
                            data: qubitCol || "qubits"
                        },
                        { 
                            title: "Link",
                            data: linkCol || "doi",
                            render: function(data) {
                                return data ? `<a href="${data}" target="_blank">Link</a>` : '';
                            }
                        }
                    ];
                    break;
                case 'entangled-table':
                    columnDefs = [
                        { 
                            title: "Year",
                            data: findColumn(headers, ["Year", "year", "Date", "date"]) || "Year"
                        },
                        { 
                            title: "Platform",
                            data: findColumn(headers, ["Platform", "platform", "Implementation"]) || "Platform"
                        },
                        {
                            title: "Entangled State Error",
                            data: findColumn(headers, ["Entangled State Error", "entangled_state_error", "State Error"]) || "Entangled State Error"
                        },
                        { 
                            title: "Link",
                            data: findColumn(headers, ["Link", "URL", "DOI", "link"]) || "Link",
                            render: function(data) {
                                return data ? `<a href="${data}" target="_blank">Link</a>` : '';
                            }
                        }
                    ];
                    break;
                case 'msd-table':
                    columnDefs = [
                        { 
                            title: "Year",
                            data: findColumn(headers, ["Year", "year", "Date", "date"]) || "Year"
                        },
                        { 
                            title: "Platform",
                            data: findColumn(headers, ["Platform", "platform", "Implementation"]) || "Platform"
                        },
                        {
                            title: "Code Name",
                            data: findColumn(headers, ["Code Name", "code_name", "Code", "code"]) || "Code Name"
                        },
                        { 
                            title: "Link",
                            data: findColumn(headers, ["Link", "URL", "DOI", "link"]) || "Link",
                            render: function(data) {
                                return data ? `<a href="${data}" target="_blank">Link</a>` : '';
                            }
                        }
                    ];
                    break;
                case 'physical-qubits-table':
                    columnDefs = [
                        { 
                            title: "Year",
                            data: findColumn(headers, ["Year", "year", "Date", "date"]) || "Year"
                        },
                        { 
                            title: "Platform",
                            data: findColumn(headers, ["Platform", "platform", "Implementation"]) || "Platform"
                        },
                        {
                            title: "Code Name",
                            data: findColumn(headers, ["Code Name", "code_name", "Code", "code"]) || "Code Name"
                        },
                        {
                            title: "T1",
                            data: findColumn(headers, ["T1", "t1", "T1 Time"]) || "T1"
                        },
                        {
                            title: "T2",
                            data: findColumn(headers, ["T2", "t2", "T2 Time"]) || "T2"
                        },
                        { 
                            title: "Link",
                            data: findColumn(headers, ["Link", "URL", "DOI", "link"]) || "Link",
                            render: function(data) {
                                return data ? `<a href="${data}" target="_blank">Link</a>` : '';
                            }
                        }
                    ];
                    break;
            }

            try {
                const table = $(`#${tableId}`).DataTable({
                    data: results.data,
                    columns: columnDefs,
                    responsive: true,
                    pageLength: 10,
                    order: [[0, 'desc']],
                    dom: 'Bfrtip',
                    buttons: ['copy', 'csv', 'excel'],
                    language: {
                        emptyTable: "No data available in table",
                        zeroRecords: "No matching records found"
                    }
                });
                
                updateMetricsGrid(tableId, results.data);
                
            } catch (error) {
                console.error('Error initializing DataTable:', error);
                $(`#${tableId}`).after(`<div class="error-message">Error loading table: ${error.message}</div>`);
            }
        },
        error: function(error) {
            console.error('Error loading CSV:', error);
            let message = "Data not available yet. ";
            message += error.status === 404 ? "Please contribute by adding entries!" : "There was an error loading the data.";
            $(`#${tableId}`).after(`<div class="info-message">${message}</div>`);
        }
    });
}

function updateMetricsGrid(tableId, data) {
    if (!data || data.length === 0) return;
    
    // Sort by year descending to get the latest
    const sortedData = [...data].sort((a, b) => {
        const yearA = parseInt(a.Year) || 0;
        const yearB = parseInt(b.Year) || 0;
        return yearB - yearA;
    });
    const latest = sortedData[0];
    
    console.log(`Updating metrics for ${tableId}:`, latest); // Debug log
    
    // Helper function to update link
    function updateLink(selector, url) {
        const link = $(selector + ' .link');
        if (url) {
            link.attr('href', url).show();
        } else {
            link.hide();
        }
    }
    
    switch(tableId) {
        case 'qec-table':
            $('#qec-metric .platform').text(latest.Platform || '');
            $('#qec-metric .code-name').text(latest['Code Name'] || '');
            $('#qec-metric .code-params').text(latest['Code Parameters'] || '');
            $('#qec-metric .year').text(latest.Year || '');
            updateLink('#qec-metric', latest.Link);
            break;
            
        case 'qubit-count-table':
            const qubitCount = latest['Number of qubits'] || latest['Qubit Count'] || '';
            $('#qubit-metric .count').text(qubitCount);
            $('#qubit-metric .platform').text(latest.Platform || latest.Type || '');
            $('#qubit-metric .year').text(latest.Year || '');
            updateLink('#qubit-metric', latest.Link || latest.DOI);
            break;
            
        case 'entangled-table':
            const errorRate = latest['Entangled State Error'] || '';
            $('#entangled-metric .error-rate').text(errorRate);
            $('#entangled-metric .platform').text(latest.Platform || '');
            $('#entangled-metric .year').text(latest.Year || '');
            updateLink('#entangled-metric', latest.Link);
            break;
            
        case 'msd-table':
            $('#msd-metric .msd-code-name').text(latest['Code Name'] || '');
            $('#msd-metric .platform').text(latest.Platform || '');
            $('#msd-metric .year').text(latest.Year || '');
            updateLink('#msd-metric', latest.Link);
            break;

        case 'physical-qubits-table':  // Update for coherence times
            const t1Value = latest['T1'] ? `${latest['T1']} s` : 'N/A';
            const t2Value = latest['T2'] ? `${latest['T2']} s` : 'N/A';
            $('#coherence-times-metric .t1-value').text(`T1: ${t1Value}`);
            $('#coherence-times-metric .t2-value').text(`T2: ${t2Value}`);
            $('#coherence-times-metric .platform').text(latest.Platform || '');
            $('#coherence-times-metric .physical-encoding').text(latest['Code Name'] || 'N/A');
            $('#coherence-times-metric .year').text(latest.Year || '');
            updateLink('#coherence-times-metric', latest.Link);
            break;
    }
}

$(document).ready(function() {
    // Load data for metrics grid and plots
    loadCSV('https://raw.githubusercontent.com/francois-marie/awesome-quantum-computing-experiments/main/data/qec_exp.csv', 'qec-table');
    loadCSV('https://raw.githubusercontent.com/francois-marie/awesome-quantum-computing-experiments/main/data/msd_exp.csv', 'msd-table');
    loadCSV('https://raw.githubusercontent.com/francois-marie/awesome-quantum-computing-experiments/main/data/entangled_state_error_exp.csv', 'entangled-table');
    loadCSV('https://raw.githubusercontent.com/francois-marie/awesome-quantum-computing-experiments/main/data/qubit_count.csv', 'qubit-count-table');
    loadCSV('https://raw.githubusercontent.com/francois-marie/awesome-quantum-computing-experiments/main/data/physical_qubits.csv', 'physical-qubits-table');
}); 
// Responsive Plot Enhancement Script
// This script enhances existing plots with mobile-responsive configurations

(function() {
    'use strict';

    // Mobile detection
    function isMobile() {
        return window.innerWidth <= 768;
    }

    // Function to get responsive layout configuration
    function getResponsiveLayout(originalLayout, plotType = 'default') {
        const mobile = isMobile();
        
        const responsiveLayout = {
            ...originalLayout,
            autosize: true,
            responsive: true,
            
            // Mobile-specific title adjustments
            title: {
                ...originalLayout.title,
                font: {
                    ...originalLayout.title?.font,
                    size: mobile ? 14 : (originalLayout.title?.font?.size || 18)
                },
                x: mobile ? 0.5 : (originalLayout.title?.x || 0.05),
                xanchor: mobile ? 'center' : 'left',
                pad: {
                    t: mobile ? 10 : 20,
                    b: mobile ? 10 : 20
                }
            },
            
            // Mobile-specific axis adjustments
            xaxis: {
                ...originalLayout.xaxis,
                title: {
                    ...originalLayout.xaxis?.title,
                    font: {
                        ...originalLayout.xaxis?.title?.font,
                        size: mobile ? 12 : (originalLayout.xaxis?.title?.font?.size || 14)
                    }
                },
                tickfont: {
                    ...originalLayout.xaxis?.tickfont,
                    size: mobile ? 10 : (originalLayout.xaxis?.tickfont?.size || 12)
                },
                tickangle: mobile ? -45 : (originalLayout.xaxis?.tickangle || 0)
            },
            
            yaxis: {
                ...originalLayout.yaxis,
                title: {
                    ...originalLayout.yaxis?.title,
                    font: {
                        ...originalLayout.yaxis?.title?.font,
                        size: mobile ? 12 : (originalLayout.yaxis?.title?.font?.size || 14)
                    }
                },
                tickfont: {
                    ...originalLayout.yaxis?.tickfont,
                    size: mobile ? 10 : (originalLayout.yaxis?.tickfont?.size || 12)
                }
            },
            
            // Mobile-specific legend adjustments
            legend: {
                ...originalLayout.legend,
                font: {
                    ...originalLayout.legend?.font,
                    size: mobile ? 10 : (originalLayout.legend?.font?.size || 12)
                },
                x: mobile ? 0.5 : (originalLayout.legend?.x !== undefined ? originalLayout.legend.x : 1.02),
                y: mobile ? -0.1 : (originalLayout.legend?.y !== undefined ? originalLayout.legend.y : 1),
                xanchor: mobile ? 'center' : 'left',
                yanchor: mobile ? 'top' : 'top',
                orientation: mobile ? 'h' : 'v',
                // Ensure legend is visible
                bgcolor: mobile ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0)',
                bordercolor: mobile ? 'rgba(0,0,0,0.1)' : 'rgba(0,0,0,0)',
                borderwidth: mobile ? 1 : 0
            },
            
            // Mobile-specific margin adjustments
            margin: {
                l: mobile ? 50 : 80,
                r: mobile ? 20 : 120, // More space for desktop legends
                t: mobile ? 50 : 80,
                b: mobile ? (originalLayout.legend && mobile ? 100 : 50) : 80
            },
            
            // Force responsive sizing
            width: undefined, // Let plot auto-size to container
            height: undefined // Let plot auto-size to container
        };

        // Special handling for 3D plots
        if (originalLayout.scene) {
            responsiveLayout.scene = {
                ...originalLayout.scene,
                camera: {
                    ...originalLayout.scene.camera,
                    eye: mobile ? 
                        { x: 1.5, y: 1.5, z: 1.5 } : 
                        (originalLayout.scene.camera?.eye || { x: 1.25, y: 1.25, z: 1.25 })
                },
                xaxis: {
                    ...originalLayout.scene.xaxis,
                    title: {
                        ...originalLayout.scene.xaxis?.title,
                        font: {
                            ...originalLayout.scene.xaxis?.title?.font,
                            size: mobile ? 10 : 12
                        }
                    },
                    tickfont: {
                        ...originalLayout.scene.xaxis?.tickfont,
                        size: mobile ? 8 : 10
                    }
                },
                yaxis: {
                    ...originalLayout.scene.yaxis,
                    title: {
                        ...originalLayout.scene.yaxis?.title,
                        font: {
                            ...originalLayout.scene.yaxis?.title?.font,
                            size: mobile ? 10 : 12
                        }
                    },
                    tickfont: {
                        ...originalLayout.scene.yaxis?.tickfont,
                        size: mobile ? 8 : 10
                    }
                },
                zaxis: {
                    ...originalLayout.scene.zaxis,
                    title: {
                        ...originalLayout.scene.zaxis?.title,
                        font: {
                            ...originalLayout.scene.zaxis?.title?.font,
                            size: mobile ? 10 : 12
                        }
                    },
                    tickfont: {
                        ...originalLayout.scene.zaxis?.tickfont,
                        size: mobile ? 8 : 10
                    }
                }
            };
        }

        return responsiveLayout;
    }

    // Function to get responsive config
    function getResponsiveConfig(originalConfig = {}) {
        const mobile = isMobile();
        
        return {
            ...originalConfig,
            responsive: true,
            displayModeBar: !mobile,
            modeBarButtonsToRemove: mobile ? [] : ['toImage', 'sendDataToCloud'],
            modeBarButtons: mobile ? [] : undefined,
            scrollZoom: !mobile,
            doubleClick: 'reset',
            showTips: !mobile,
            displaylogo: false,
            // Force autosizing on mobile for full width
            autosizable: mobile,
            // Touch-friendly configuration for mobile
            touchstart: mobile ? 'auto' : undefined,
            touchmove: mobile ? 'auto' : undefined,
            touchend: mobile ? 'auto' : undefined
        };
    }

    // Function to enhance existing plot
    function enhancePlot(plotId) {
        const plotDiv = document.getElementById(plotId);
        if (!plotDiv || !plotDiv.data || !plotDiv.layout) {
            console.log(`Plot ${plotId} not found or not initialized`);
            return false;
        }

        try {
            // Get current plot data
            const currentData = plotDiv.data;
            const currentLayout = plotDiv.layout;
            
            // Apply responsive enhancements
            const responsiveLayout = getResponsiveLayout(currentLayout);
            const responsiveConfig = getResponsiveConfig();
            
            // Update the plot with responsive configuration
            Plotly.react(plotId, currentData, responsiveLayout, responsiveConfig);
            
            // Force resize to ensure proper mobile width
            if (isMobile()) {
                setTimeout(() => {
                    Plotly.Plots.resize(plotId);
                }, 100);
            }
            
            console.log(`Enhanced plot ${plotId} with responsive configuration`);
            return true;
        } catch (error) {
            console.error(`Failed to enhance plot ${plotId}:`, error);
            return false;
        }
    }

    // Function to enhance all plots on the page
    function enhanceAllPlots() {
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
        
        let enhancedCount = 0;
        plotIds.forEach(plotId => {
            if (enhancePlot(plotId)) {
                enhancedCount++;
            }
        });
        
        console.log(`Enhanced ${enhancedCount} plots with responsive configuration`);
    }

    // Debounced resize handler
    let resizeTimeout;
    function handleResize() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            console.log('Window resized, re-enhancing plots...');
            enhanceAllPlots();
            
            // Additional mobile-specific resize handling
            if (isMobile()) {
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
                
                // Force resize for each plot on mobile
                plotIds.forEach(plotId => {
                    const plotDiv = document.getElementById(plotId);
                    if (plotDiv && plotDiv.data) {
                        try {
                            Plotly.Plots.resize(plotId);
                        } catch (e) {
                            console.warn(`Failed to resize plot ${plotId}:`, e);
                        }
                    }
                });
            }
        }, 250);
    }

    // Initialize when DOM is ready
    function initialize() {
        console.log('Initializing responsive plot enhancements...');
        
        // Enhance plots after a short delay to ensure they're loaded
        setTimeout(() => {
            enhanceAllPlots();
        }, 500);
        
        // Add resize listener
        window.addEventListener('resize', handleResize);
        
        // Re-enhance when orientation changes (mobile)
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                handleResize();
            }, 500);
        });
    }

    // Public API
    window.ResponsivePlots = {
        enhance: enhancePlot,
        enhanceAll: enhanceAllPlots,
        isMobile: isMobile
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

})(); 
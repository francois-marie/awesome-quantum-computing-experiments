// Coherence Times Plot Plot
const coherence_times_plotData = [
  {
    "customdata": [
      "https://arxiv.org/abs/1809.05215"
    ],
    "hovertemplate": "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#867BFA",
      "width": 3
    },
    "marker": {
      "color": "#867BFA",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "Graphene (T1)",
    "text": [
      "Quantum coherent control of a hybrid superconducting circuit made with graphene-based van der Waals heterostructures"
    ],
    "x": [
      2018
    ],
    "y": [
      5e-08
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://doi.org/10.1103/PhysRevLett.95.060502",
      "https://doi.org/10.1103/PhysRevLett.113.220501",
      "https://doi.org/10.1038/s41566-017-0007-1",
      "https://doi.org/10.1038/s41467-020-20330-w"
    ],
    "hovertemplate": "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#FFC107",
      "dash": "dash",
      "width": 3
    },
    "marker": {
      "color": "#FFC107",
      "line": {
        "color": "#FFC107",
        "width": 2
      },
      "size": 12,
      "symbol": "circle-open"
    },
    "mode": "markers",
    "name": "Ion traps (T2)",
    "text": [
      "Long-Lived Qubit Memory Using Atomic Ions",
      "High-Fidelity Preparation, Gates, Memory, and Readout of a Trapped-Ion Quantum Bit",
      "Single-qubit quantum memory exceeding ten-minute coherence time",
      "Single ion qubit with estimated coherence time exceeding one hour"
    ],
    "x": [
      2005,
      2014,
      2017,
      2021
    ],
    "y": [
      14.7,
      50.0,
      667.0,
      5500.0
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "line": {
      "color": "#FFC107",
      "dash": "dashdot",
      "width": 2
    },
    "mode": "lines",
    "name": "Ion traps T2 fit (\u00d72 every 1.9y)",
    "showlegend": true,
    "x": [
      2005,
      2021
    ],
    "y": [
      8.034081054958786,
      2617.064887994298
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://doi.org/10.1038/s41467-018-04916-z"
    ],
    "hovertemplate": "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#E74C3C",
      "width": 3
    },
    "marker": {
      "color": "#E74C3C",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "NV centers (T1)",
    "text": [
      "One-second coherence for a single electron spin coupled to a multi-qubit nuclear-spin environment"
    ],
    "x": [
      2018
    ],
    "y": [
      3600.0
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://doi.org/10.1038/s41467-018-04916-z"
    ],
    "hovertemplate": "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#E74C3C",
      "dash": "dash",
      "width": 3
    },
    "marker": {
      "color": "#E74C3C",
      "line": {
        "color": "#E74C3C",
        "width": 2
      },
      "size": 12,
      "symbol": "circle-open"
    },
    "mode": "markers",
    "name": "NV centers (T2)",
    "text": [
      "One-second coherence for a single electron spin coupled to a multi-qubit nuclear-spin environment"
    ],
    "x": [
      2018
    ],
    "y": [
      1.58
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://doi.org/10.1103/PhysRevA.75.040301",
      "https://doi.org/10.1103/PhysRevLett.122.173201",
      "https://doi.org/10.1038/s41586-022-04603-6",
      "https://doi.org/10.1038/s41586-022-04592-6",
      "https://doi.org/10.48550/arXiv.2403.12021"
    ],
    "hovertemplate": "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#95A5A6",
      "width": 3
    },
    "marker": {
      "color": "#95A5A6",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "Neutral atoms (T1)",
    "text": [
      "Fast Quantum State Control of a Single Trapped Neutral Atom",
      "2000-times repeated imaging of strontium atoms in clock-magic tweezer arrays",
      "Multi-qubit entanglement and algorithms on a neutral-atom quantum computer",
      "A quantum processor based on coherent transport of entangled atom arrays",
      "A tweezer array with 6100 highly coherent atomic qubits"
    ],
    "x": [
      2007,
      2019,
      2022,
      2022,
      2024
    ],
    "y": [
      3.0,
      420.0,
      4.0,
      4.0,
      119.0
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "line": {
      "color": "#95A5A6",
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "Neutral atoms T1 fit (\u00d72 every 5.9y)",
    "showlegend": true,
    "x": [
      2007,
      2024
    ],
    "y": [
      4.713383552745039,
      34.80109955052615
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://doi.org/10.1103/PhysRevA.75.040301",
      "https://doi.org/10.1038/s41586-022-04603-6",
      "https://doi.org/10.1038/s41586-022-04592-6",
      "https://doi.org/10.48550/arXiv.2403.12021"
    ],
    "hovertemplate": "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#95A5A6",
      "dash": "dash",
      "width": 3
    },
    "marker": {
      "color": "#95A5A6",
      "line": {
        "color": "#95A5A6",
        "width": 2
      },
      "size": 12,
      "symbol": "circle-open"
    },
    "mode": "markers",
    "name": "Neutral atoms (T2)",
    "text": [
      "Fast Quantum State Control of a Single Trapped Neutral Atom",
      "Multi-qubit entanglement and algorithms on a neutral-atom quantum computer",
      "A quantum processor based on coherent transport of entangled atom arrays",
      "A tweezer array with 6100 highly coherent atomic qubits"
    ],
    "x": [
      2007,
      2022,
      2022,
      2024
    ],
    "y": [
      0.034,
      1.0,
      1.5,
      12.6
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "line": {
      "color": "#95A5A6",
      "dash": "dashdot",
      "width": 2
    },
    "mode": "lines",
    "name": "Neutral atoms T2 fit (\u00d72 every 2.4y)",
    "showlegend": true,
    "x": [
      2007,
      2024
    ],
    "y": [
      0.02929798398979105,
      4.12630852714783
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://arxiv.org/abs/1503.08339",
      "https://arxiv.org/abs/1512.09195",
      "https://arxiv.org/abs/1711.07961"
    ],
    "hovertemplate": "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#92DCE5",
      "width": 3
    },
    "marker": {
      "color": "#92DCE5",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "Semiconductor (T1)",
    "text": [
      "A Semiconductor Nanowire-Based Superconducting Qubit",
      "Gatemon Benchmarking and Two-Qubit Operation",
      "Evolution of Nanowire Transmons and Their Quantum Coherence in Magnetic Field"
    ],
    "x": [
      2015,
      2016,
      2018
    ],
    "y": [
      8e-07,
      3e-06,
      1e-05
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "line": {
      "color": "#92DCE5",
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "Semiconductor T1 fit (\u00d72 every 0.9y)",
    "showlegend": true,
    "x": [
      2015,
      2018
    ],
    "y": [
      9.826570108668322e-07,
      1.1082965594026632e-05
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://arxiv.org/abs/1503.08339"
    ],
    "hovertemplate": "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#92DCE5",
      "dash": "dash",
      "width": 3
    },
    "marker": {
      "color": "#92DCE5",
      "line": {
        "color": "#92DCE5",
        "width": 2
      },
      "size": 12,
      "symbol": "circle-open"
    },
    "mode": "markers",
    "name": "Semiconductor (T2)",
    "text": [
      "A Semiconductor Nanowire-Based Superconducting Qubit"
    ],
    "x": [
      2015
    ],
    "y": [
      1e-06
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://arxiv.org/abs/cond-mat/9904003v1",
      "https://arxiv.org/abs/cond-mat/0111402",
      "https://arxiv.org/abs/cond-mat/0205343",
      "https://arxiv.org/abs/cond-mat/0305461",
      "https://arxiv.org/abs/cond-mat/0512428",
      "https://arxiv.org/abs/0803.4490",
      "https://arxiv.org/abs/0808.3279",
      "https://arxiv.org/abs/1101.4707",
      "https://arxiv.org/abs/1105.4652",
      "https://arxiv.org/abs/1202.5533",
      "https://arxiv.org/abs/1303.4071",
      "https://www.nature.com/articles/nature13017",
      "https://arxiv.org/abs/1412.2772",
      "https://arxiv.org/abs/1508.06299",
      "https://arxiv.org/abs/1601.05505",
      "https://arxiv.org/abs/1602.04768v1",
      "https://arxiv.org/abs/1803.00102",
      "https://arxiv.org/abs/1810.11006",
      "https://arxiv.org/abs/1805.09072",
      "https://doi.org/10.1038/s41567-020-0824-x",
      "https://doi.org/10.48550/arXiv.1901.08042",
      "https://doi.org/10.1103/PRXQuantum.4.020350",
      "https://doi.org/10.1038/s41586-024-07294-3",
      "https://doi.org/10.1103/PhysRevX.14.021019"
    ],
    "hovertemplate": "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#2ECC71",
      "width": 3
    },
    "marker": {
      "color": "#2ECC71",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "Superconducting circuit (T1)",
    "text": [
      "Coherent control of macroscopic quantum states in a single-Cooper-pair box",
      "Charge echo in a Cooper-pair box",
      "Manipulating the Quantum State of an Electrical Circuit",
      "Coherent Quantum Dynamics of a Superconducting Flux Qubit",
      "Dephasing of a superconducting qubit induced by photon noise",
      "Controlling the spontaneous emission of a superconducting transmon qubit",
      "Measurement of the decay of Fock states in a superconducting quantum circuit",
      "Dynamical decoupling and noise spectroscopy with a superconducting flux qubit",
      "Observation of high coherence in Josephson junction qubits measured in a three-dimensional circuit QED architecture",
      "Superconducting qubit in waveguide cavity with coherence time approaching 0.1ms",
      "Improved superconducting qubit coherence using titanium nitride",
      "Coherent suppression of electromagnetic dissipation due to superconducting quasiparticles",
      "Thermal and Residual Excited-State Population in a 3D Transmon Qubit",
      "The Flux Qubit Revisited to Enhance Coherence and Reproducibility",
      "A Schrodinger Cat Living in Two Boxes",
      "Demonstrating Quantum Error Correction that Extends the Lifetime of Quantum Information",
      "Fault-tolerant detection of a quantum error",
      "The high-coherence fluxonium qubit",
      "Demonstration of quantum error correction and universal gate set on a binomial bosonic logical qubit",
      "Exponential suppression of bit-flips in a qubit encoded in an oscillator",
      "Manufacturing low dissipation superconducting quantum processors",
      "One Hundred Second Bit-Flip Time in a Two-Photon Dissipative Oscillator",
      "Quantum control of a cat-qubit with bit-flip times exceeding ten seconds",
      "Autoparametric resonance extending the bit-flip time of a cat qubit up to 0.3 s"
    ],
    "x": [
      1999,
      2001,
      2002,
      2003,
      2005,
      2007,
      2008,
      2010,
      2011,
      2012,
      2013,
      2014,
      2014,
      2015,
      2015,
      2016,
      2018,
      2018,
      2019,
      2019,
      2019,
      2023,
      2024,
      2024
    ],
    "y": [
      2e-09,
      9e-09,
      1e-06,
      1e-06,
      5e-06,
      4e-06,
      3e-06,
      1.2e-05,
      7e-05,
      7e-05,
      7e-05,
      0.001,
      0.0001,
      4e-05,
      0.004,
      0.00015,
      0.0011,
      0.0002,
      0.0001,
      0.001,
      7.6e-05,
      127.0,
      15.0,
      0.3
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "line": {
      "color": "#2ECC71",
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "Superconducting circuit T1 fit (\u00d72 every 1.0y)",
    "showlegend": true,
    "x": [
      1999,
      2024
    ],
    "y": [
      9.183346664879572e-09,
      0.2053884451636374
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "customdata": [
      "https://arxiv.org/abs/cond-mat/0111402",
      "https://arxiv.org/abs/cond-mat/0205343",
      "https://arxiv.org/abs/cond-mat/0305461",
      "https://arxiv.org/abs/cond-mat/0512428",
      "https://arxiv.org/abs/0803.4490",
      "https://arxiv.org/abs/0808.3279",
      "https://arxiv.org/abs/0906.0831",
      "https://arxiv.org/abs/1101.4707",
      "https://arxiv.org/abs/1105.4652",
      "https://arxiv.org/abs/1202.5533",
      "https://arxiv.org/abs/1303.4071",
      "https://www.nature.com/articles/nature13017",
      "https://arxiv.org/abs/1412.2772",
      "https://arxiv.org/abs/1508.06299",
      "https://arxiv.org/abs/1601.05505",
      "https://arxiv.org/abs/1803.00102",
      "https://arxiv.org/abs/1810.11006",
      "https://arxiv.org/abs/1805.09072",
      "https://doi.org/10.1038/s41586-024-07294-3"
    ],
    "hovertemplate": "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#2ECC71",
      "dash": "dash",
      "width": 3
    },
    "marker": {
      "color": "#2ECC71",
      "line": {
        "color": "#2ECC71",
        "width": 2
      },
      "size": 12,
      "symbol": "circle-open"
    },
    "mode": "markers",
    "name": "Superconducting circuit (T2)",
    "text": [
      "Charge echo in a Cooper-pair box",
      "Manipulating the Quantum State of an Electrical Circuit",
      "Coherent Quantum Dynamics of a Superconducting Flux Qubit",
      "Dephasing of a superconducting qubit induced by photon noise",
      "Controlling the spontaneous emission of a superconducting transmon qubit",
      "Measurement of the decay of Fock states in a superconducting quantum circuit",
      "Fluxonium: single Cooper pair circuit free of charge offsets",
      "Dynamical decoupling and noise spectroscopy with a superconducting flux qubit",
      "Observation of high coherence in Josephson junction qubits measured in a three-dimensional circuit QED architecture",
      "Superconducting qubit in waveguide cavity with coherence time approaching 0.1ms",
      "Improved superconducting qubit coherence using titanium nitride",
      "Coherent suppression of electromagnetic dissipation due to superconducting quasiparticles",
      "Thermal and Residual Excited-State Population in a 3D Transmon Qubit",
      "The Flux Qubit Revisited to Enhance Coherence and Reproducibility",
      "A Schrodinger Cat Living in Two Boxes",
      "Fault-tolerant detection of a quantum error",
      "The high-coherence fluxonium qubit",
      "Demonstration of quantum error correction and universal gate set on a binomial bosonic logical qubit",
      "Quantum control of a cat-qubit with bit-flip times exceeding ten seconds"
    ],
    "x": [
      2001,
      2002,
      2003,
      2005,
      2007,
      2008,
      2009,
      2010,
      2011,
      2012,
      2013,
      2014,
      2014,
      2015,
      2015,
      2018,
      2018,
      2019,
      2024
    ],
    "y": [
      5e-09,
      8e-07,
      2e-08,
      5e-06,
      2e-06,
      6e-06,
      3.5e-07,
      2.3e-05,
      1.5e-05,
      9.5e-05,
      7e-05,
      2e-05,
      0.0002,
      8.5e-05,
      0.001,
      0.0014,
      0.0003,
      0.0001,
      5e-07
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  },
  {
    "line": {
      "color": "#2ECC71",
      "dash": "dashdot",
      "width": 2
    },
    "mode": "lines",
    "name": "Superconducting circuit T2 fit (\u00d72 every 1.9y)",
    "showlegend": true,
    "x": [
      2001,
      2024
    ],
    "y": [
      2.4797998637960684e-07,
      0.000935532868334199
    ],
    "type": "scatter",
    "textfont": {
      "family": "Arial"
    },
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  }
];

const coherence_times_plotLayout = {
  "font": {
    "color": "#2F3136",
    "family": "Arial",
    "size": 14
  },
  "height": 800,
  "hovermode": "closest",
  "legend": {
    "bgcolor": "rgba(255, 255, 255, 0.8)",
    "bordercolor": "#E5E5E5",
    "font": {
      "size": 12
    },
    "x": 1.02,
    "y": 1
  },
  "margin": {
    "b": 80,
    "l": 80,
    "pad": 10,
    "r": 40,
    "t": 80
  },
  "paper_bgcolor": "white",
  "plot_bgcolor": "#F5F6F7",
  "showlegend": true,
  "title": {
    "font": {
      "color": "#2F3136",
      "size": 16,
      "family": "Arial"
    },
    "text": "Physical Qubit Coherence Times Evolution"
  },
  "width": 1000,
  "xaxis": {
    "gridcolor": "#E5E5E5",
    "gridwidth": 1,
    "linecolor": "#2F3136",
    "linewidth": 1,
    "minor": {
      "tickcolor": "#2F3136",
      "ticklen": 3,
      "ticks": "outside",
      "tickwidth": 1
    },
    "showgrid": true,
    "tickcolor": "#2F3136",
    "ticklen": 5,
    "ticks": "outside",
    "tickwidth": 1,
    "title": {
      "text": "Year"
    }
  },
  "yaxis": {
    "gridcolor": "#E5E5E5",
    "gridwidth": 1,
    "linecolor": "#2F3136",
    "linewidth": 1,
    "minor": {
      "tickcolor": "#2F3136",
      "ticklen": 3,
      "ticks": "outside",
      "tickwidth": 1
    },
    "showgrid": true,
    "tickcolor": "#2F3136",
    "ticklen": 5,
    "ticks": "outside",
    "tickwidth": 1,
    "title": {
      "text": "Coherence Time (s)"
    },
    "type": "log"
  },
  "template": {
    "data": {
      "histogram2dcontour": [
        {
          "type": "histogram2dcontour",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          },
          "colorscale": [
            [
              0.0,
              "#0d0887"
            ],
            [
              0.1111111111111111,
              "#46039f"
            ],
            [
              0.2222222222222222,
              "#7201a8"
            ],
            [
              0.3333333333333333,
              "#9c179e"
            ],
            [
              0.4444444444444444,
              "#bd3786"
            ],
            [
              0.5555555555555556,
              "#d8576b"
            ],
            [
              0.6666666666666666,
              "#ed7953"
            ],
            [
              0.7777777777777778,
              "#fb9f3a"
            ],
            [
              0.8888888888888888,
              "#fdca26"
            ],
            [
              1.0,
              "#f0f921"
            ]
          ]
        }
      ],
      "choropleth": [
        {
          "type": "choropleth",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          }
        }
      ],
      "histogram2d": [
        {
          "type": "histogram2d",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          },
          "colorscale": [
            [
              0.0,
              "#0d0887"
            ],
            [
              0.1111111111111111,
              "#46039f"
            ],
            [
              0.2222222222222222,
              "#7201a8"
            ],
            [
              0.3333333333333333,
              "#9c179e"
            ],
            [
              0.4444444444444444,
              "#bd3786"
            ],
            [
              0.5555555555555556,
              "#d8576b"
            ],
            [
              0.6666666666666666,
              "#ed7953"
            ],
            [
              0.7777777777777778,
              "#fb9f3a"
            ],
            [
              0.8888888888888888,
              "#fdca26"
            ],
            [
              1.0,
              "#f0f921"
            ]
          ]
        }
      ],
      "heatmap": [
        {
          "type": "heatmap",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          },
          "colorscale": [
            [
              0.0,
              "#0d0887"
            ],
            [
              0.1111111111111111,
              "#46039f"
            ],
            [
              0.2222222222222222,
              "#7201a8"
            ],
            [
              0.3333333333333333,
              "#9c179e"
            ],
            [
              0.4444444444444444,
              "#bd3786"
            ],
            [
              0.5555555555555556,
              "#d8576b"
            ],
            [
              0.6666666666666666,
              "#ed7953"
            ],
            [
              0.7777777777777778,
              "#fb9f3a"
            ],
            [
              0.8888888888888888,
              "#fdca26"
            ],
            [
              1.0,
              "#f0f921"
            ]
          ]
        }
      ],
      "contourcarpet": [
        {
          "type": "contourcarpet",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          }
        }
      ],
      "contour": [
        {
          "type": "contour",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          },
          "colorscale": [
            [
              0.0,
              "#0d0887"
            ],
            [
              0.1111111111111111,
              "#46039f"
            ],
            [
              0.2222222222222222,
              "#7201a8"
            ],
            [
              0.3333333333333333,
              "#9c179e"
            ],
            [
              0.4444444444444444,
              "#bd3786"
            ],
            [
              0.5555555555555556,
              "#d8576b"
            ],
            [
              0.6666666666666666,
              "#ed7953"
            ],
            [
              0.7777777777777778,
              "#fb9f3a"
            ],
            [
              0.8888888888888888,
              "#fdca26"
            ],
            [
              1.0,
              "#f0f921"
            ]
          ]
        }
      ],
      "surface": [
        {
          "type": "surface",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          },
          "colorscale": [
            [
              0.0,
              "#0d0887"
            ],
            [
              0.1111111111111111,
              "#46039f"
            ],
            [
              0.2222222222222222,
              "#7201a8"
            ],
            [
              0.3333333333333333,
              "#9c179e"
            ],
            [
              0.4444444444444444,
              "#bd3786"
            ],
            [
              0.5555555555555556,
              "#d8576b"
            ],
            [
              0.6666666666666666,
              "#ed7953"
            ],
            [
              0.7777777777777778,
              "#fb9f3a"
            ],
            [
              0.8888888888888888,
              "#fdca26"
            ],
            [
              1.0,
              "#f0f921"
            ]
          ]
        }
      ],
      "mesh3d": [
        {
          "type": "mesh3d",
          "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
          }
        }
      ],
      "scatter": [
        {
          "fillpattern": {
            "fillmode": "overlay",
            "size": 10,
            "solidity": 0.2
          },
          "type": "scatter"
        }
      ],
      "parcoords": [
        {
          "type": "parcoords",
          "line": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scatterpolargl": [
        {
          "type": "scatterpolargl",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "bar": [
        {
          "error_x": {
            "color": "#2a3f5f"
          },
          "error_y": {
            "color": "#2a3f5f"
          },
          "marker": {
            "line": {
              "color": "#E5ECF6",
              "width": 0.5
            },
            "pattern": {
              "fillmode": "overlay",
              "size": 10,
              "solidity": 0.2
            }
          },
          "type": "bar"
        }
      ],
      "scattergeo": [
        {
          "type": "scattergeo",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scatterpolar": [
        {
          "type": "scatterpolar",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "histogram": [
        {
          "marker": {
            "pattern": {
              "fillmode": "overlay",
              "size": 10,
              "solidity": 0.2
            }
          },
          "type": "histogram"
        }
      ],
      "scattergl": [
        {
          "type": "scattergl",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scatter3d": [
        {
          "type": "scatter3d",
          "line": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          },
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scattermap": [
        {
          "type": "scattermap",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scattermapbox": [
        {
          "type": "scattermapbox",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scatterternary": [
        {
          "type": "scatterternary",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "scattercarpet": [
        {
          "type": "scattercarpet",
          "marker": {
            "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
            }
          }
        }
      ],
      "carpet": [
        {
          "aaxis": {
            "endlinecolor": "#2a3f5f",
            "gridcolor": "white",
            "linecolor": "white",
            "minorgridcolor": "white",
            "startlinecolor": "#2a3f5f"
          },
          "baxis": {
            "endlinecolor": "#2a3f5f",
            "gridcolor": "white",
            "linecolor": "white",
            "minorgridcolor": "white",
            "startlinecolor": "#2a3f5f"
          },
          "type": "carpet"
        }
      ],
      "table": [
        {
          "cells": {
            "fill": {
              "color": "#EBF0F8"
            },
            "line": {
              "color": "white"
            }
          },
          "header": {
            "fill": {
              "color": "#C8D4E3"
            },
            "line": {
              "color": "white"
            }
          },
          "type": "table"
        }
      ],
      "barpolar": [
        {
          "marker": {
            "line": {
              "color": "#E5ECF6",
              "width": 0.5
            },
            "pattern": {
              "fillmode": "overlay",
              "size": 10,
              "solidity": 0.2
            }
          },
          "type": "barpolar"
        }
      ],
      "pie": [
        {
          "automargin": true,
          "type": "pie"
        }
      ]
    },
    "layout": {
      "autotypenumbers": "strict",
      "colorway": [
        "#636efa",
        "#EF553B",
        "#00cc96",
        "#ab63fa",
        "#FFA15A",
        "#19d3f3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52"
      ],
      "font": {
        "color": "#2a3f5f"
      },
      "hovermode": "closest",
      "hoverlabel": {
        "align": "left"
      },
      "paper_bgcolor": "white",
      "plot_bgcolor": "#E5ECF6",
      "polar": {
        "bgcolor": "#E5ECF6",
        "angularaxis": {
          "gridcolor": "white",
          "linecolor": "white",
          "ticks": ""
        },
        "radialaxis": {
          "gridcolor": "white",
          "linecolor": "white",
          "ticks": ""
        }
      },
      "ternary": {
        "bgcolor": "#E5ECF6",
        "aaxis": {
          "gridcolor": "white",
          "linecolor": "white",
          "ticks": ""
        },
        "baxis": {
          "gridcolor": "white",
          "linecolor": "white",
          "ticks": ""
        },
        "caxis": {
          "gridcolor": "white",
          "linecolor": "white",
          "ticks": ""
        }
      },
      "coloraxis": {
        "colorbar": {
          "outlinewidth": 0,
          "ticks": ""
        }
      },
      "colorscale": {
        "sequential": [
          [
            0.0,
            "#0d0887"
          ],
          [
            0.1111111111111111,
            "#46039f"
          ],
          [
            0.2222222222222222,
            "#7201a8"
          ],
          [
            0.3333333333333333,
            "#9c179e"
          ],
          [
            0.4444444444444444,
            "#bd3786"
          ],
          [
            0.5555555555555556,
            "#d8576b"
          ],
          [
            0.6666666666666666,
            "#ed7953"
          ],
          [
            0.7777777777777778,
            "#fb9f3a"
          ],
          [
            0.8888888888888888,
            "#fdca26"
          ],
          [
            1.0,
            "#f0f921"
          ]
        ],
        "sequentialminus": [
          [
            0.0,
            "#0d0887"
          ],
          [
            0.1111111111111111,
            "#46039f"
          ],
          [
            0.2222222222222222,
            "#7201a8"
          ],
          [
            0.3333333333333333,
            "#9c179e"
          ],
          [
            0.4444444444444444,
            "#bd3786"
          ],
          [
            0.5555555555555556,
            "#d8576b"
          ],
          [
            0.6666666666666666,
            "#ed7953"
          ],
          [
            0.7777777777777778,
            "#fb9f3a"
          ],
          [
            0.8888888888888888,
            "#fdca26"
          ],
          [
            1.0,
            "#f0f921"
          ]
        ],
        "diverging": [
          [
            0,
            "#8e0152"
          ],
          [
            0.1,
            "#c51b7d"
          ],
          [
            0.2,
            "#de77ae"
          ],
          [
            0.3,
            "#f1b6da"
          ],
          [
            0.4,
            "#fde0ef"
          ],
          [
            0.5,
            "#f7f7f7"
          ],
          [
            0.6,
            "#e6f5d0"
          ],
          [
            0.7,
            "#b8e186"
          ],
          [
            0.8,
            "#7fbc41"
          ],
          [
            0.9,
            "#4d9221"
          ],
          [
            1,
            "#276419"
          ]
        ]
      },
      "xaxis": {
        "gridcolor": "white",
        "linecolor": "white",
        "ticks": "",
        "title": {
          "standoff": 15
        },
        "zerolinecolor": "white",
        "automargin": true,
        "zerolinewidth": 2
      },
      "yaxis": {
        "gridcolor": "white",
        "linecolor": "white",
        "ticks": "",
        "title": {
          "standoff": 15
        },
        "zerolinecolor": "white",
        "automargin": true,
        "zerolinewidth": 2
      },
      "scene": {
        "xaxis": {
          "backgroundcolor": "#E5ECF6",
          "gridcolor": "white",
          "linecolor": "white",
          "showbackground": true,
          "ticks": "",
          "zerolinecolor": "white",
          "gridwidth": 2
        },
        "yaxis": {
          "backgroundcolor": "#E5ECF6",
          "gridcolor": "white",
          "linecolor": "white",
          "showbackground": true,
          "ticks": "",
          "zerolinecolor": "white",
          "gridwidth": 2
        },
        "zaxis": {
          "backgroundcolor": "#E5ECF6",
          "gridcolor": "white",
          "linecolor": "white",
          "showbackground": true,
          "ticks": "",
          "zerolinecolor": "white",
          "gridwidth": 2
        }
      },
      "shapedefaults": {
        "line": {
          "color": "#2a3f5f"
        }
      },
      "annotationdefaults": {
        "arrowcolor": "#2a3f5f",
        "arrowhead": 0,
        "arrowwidth": 1
      },
      "geo": {
        "bgcolor": "white",
        "landcolor": "#E5ECF6",
        "subunitcolor": "white",
        "showland": true,
        "showlakes": true,
        "lakecolor": "white"
      },
      "title": {
        "x": 0.05
      },
      "mapbox": {
        "style": "light"
      }
    }
  },
  "uniformtext": {
    "mode": "hide",
    "minsize": 8
  },
  "modebar": {
    "remove": [
      "toImage",
      "sendDataToCloud"
    ]
  },
  "separators": ". "
};

Plotly.newPlot('coherence-times-plot', coherence_times_plotData, coherence_times_plotLayout);

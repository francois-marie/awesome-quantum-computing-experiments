// Qec Platform Sunburst Plot
const qec_platform_sunburstData = [
  {
    "branchvalues": "total",
    "customdata": [
      "<b>All QEC Codes</b><br>57 experiments",
      "<b>Bacon-Shor Code</b><br>3 experiments<br>5.3% of total",
      "<b>Bell State</b><br>3 experiments<br>5.3% of total",
      "<b>Cluster State</b><br>1 experiments<br>1.8% of total",
      "<b>Color Code</b><br>7 experiments<br>12.3% of total",
      "<b>Four-qubit Code</b><br>16 experiments<br>28.1% of total",
      "<b>Repetition Code</b><br>16 experiments<br>28.1% of total",
      "<b>Surface Code</b><br>8 experiments<br>14.0% of total",
      "<b>[[5,1,3]] Perfect Code</b><br>3 experiments<br>5.3% of total",
      "<b>Ion traps</b> - Bacon-Shor Code<br>1 experiments<br>33.3% of Bacon-Shor Code<br>1.8% of total<br>\u2022 Fault-Tolerant Operation of a Quantum Error-Correction Code (<a href='https://arxiv.org/abs/2009.11482' target='_blank'>link</a>)",
      "<b>Neutral atoms</b> - Bacon-Shor Code<br>1 experiments<br>33.3% of Bacon-Shor Code<br>1.8% of total<br>\u2022 Logical computation demonstrated with a neutral atom quantum processor (<a href='https://arxiv.org/abs/2411.11822' target='_blank'>link</a>)",
      "<b>Photons</b> - Bacon-Shor Code<br>1 experiments<br>33.3% of Bacon-Shor Code<br>1.8% of total<br>\u2022 Quantum teleportation of physical qubits into logical code-spaces (<a href='https://arxiv.org/abs/2009.06242' target='_blank'>link</a>)",
      "<b>Superconducting circuit</b> - Bell State<br>3 experiments<br>100.0% of Bell State<br>5.3% of total<br>\u2022 Demonstration of a quantum error detection code using a square lattice of four superconducting qubits (<a href='https://www.nature.com/articles/ncomms7979' target='_blank'>link</a>)<br>\u2022 Entanglement stabilization using ancilla-based parity detection and real-time feedback in superconducting circuits (<a href='https://www.nature.com/articles/s41534-019-0185-4' target='_blank'>link</a>)<br>\u2022 Protecting quantum entanglement from leakage and qubit errors via repetitive parity measurements (<a href='https://arxiv.org/abs/1905.12731' target='_blank'>link</a>)",
      "<b>Neutral atoms</b> - Cluster State<br>1 experiments<br>100.0% of Cluster State<br>1.8% of total<br>\u2022 A quantum processor based on coherent transport of entangled atom arrays (<a href='https://arxiv.org/abs/2112.03923' target='_blank'>link</a>)",
      "<b>Ion traps</b> - Color Code<br>2 experiments<br>28.6% of Color Code<br>3.5% of total<br>\u2022 Experimental Quantum Computations on a Topologically Encoded Qubit (<a href='https://arxiv.org/abs/1403.5426' target='_blank'>link</a>)<br>\u2022 Fault-tolerant quantum error detection (<a href='https://arxiv.org/abs/1611.06946' target='_blank'>link</a>)",
      "<b>Neutral atoms</b> - Color Code<br>3 experiments<br>42.9% of Color Code<br>5.3% of total<br>\u2022 A quantum processor based on coherent transport of entangled atom arrays (<a href='https://arxiv.org/abs/2112.03923' target='_blank'>link</a>)<br>\u2022 Logical quantum processor based on reconfigurable atom arrays (<a href='https://arxiv.org/abs/2312.03982' target='_blank'>link</a>)<br>\u2022 Experimental Demonstration of Logical Magic State Distillation (<a href='https://arxiv.org/abs/2412.15165' target='_blank'>link</a>)",
      "<b>Superconducting circuit</b> - Color Code<br>2 experiments<br>28.6% of Color Code<br>3.5% of total<br>\u2022 Experimental demonstration of fault-tolerant state preparation with superconducting qubits (<a href='https://arxiv.org/abs/1705.09259' target='_blank'>link</a>)<br>\u2022 Scaling and logic in the color code on a superconducting quantum processor (<a href='https://arxiv.org/abs/2412.14256' target='_blank'>link</a>)",
      "<b>Ion traps</b> - Four-qubit Code<br>2 experiments<br>12.5% of Four-qubit Code<br>3.5% of total<br>\u2022 Fault-tolerant quantum error detection (<a href='https://arxiv.org/abs/1611.06946' target='_blank'>link</a>)<br>\u2022 End-to-End Quantum Simulation of a Chemical System (<a href='https://arxiv.org/abs/2409.05835' target='_blank'>link</a>)",
      "<b>Neutral atoms</b> - Four-qubit Code<br>2 experiments<br>12.5% of Four-qubit Code<br>3.5% of total<br>\u2022 Logical computation demonstrated with a neutral atom quantum processor (<a href='https://arxiv.org/abs/2411.11822' target='_blank'>link</a>)<br>\u2022 Fault-Tolerant Operation and Materials Science with Neutral Atom Logical Qubits (<a href='https://arxiv.org/abs/2412.07670' target='_blank'>link</a>)",
      "<b>Photons</b> - Four-qubit Code<br>1 experiments<br>6.2% of Four-qubit Code<br>1.8% of total<br>\u2022 Optical demonstration of quantum fault-tolerant threshold (<a href='https://arxiv.org/abs/2012.08927' target='_blank'>link</a>)",
      "<b>Superconducting circuit</b> - Four-qubit Code<br>11 experiments<br>68.8% of Four-qubit Code<br>19.3% of total<br>\u2022 Exponential suppression of bit or phase flip errors with repetitive error correction (<a href='https://arxiv.org/abs/2102.06132' target='_blank'>link</a>)<br>\u2022 Experimental demonstration of fault-tolerant state preparation with superconducting qubits (<a href='https://arxiv.org/abs/1705.09259' target='_blank'>link</a>)<br>\u2022 Protecting quantum memories using coherent parity check codes (<a href='https://arxiv.org/abs/1709.01866' target='_blank'>link</a>)<br>\u2022 Is error detection helpful on IBM 5Q chips ? (<a href='https://arxiv.org/abs/1705.08957' target='_blank'>link</a>)<br>\u2022 Testing quantum fault tolerance on small systems (<a href='https://arxiv.org/abs/1805.05227' target='_blank'>link</a>)<br>\u2022 Fault-Tolerant Logical Gates in the IBM Quantum Experience (<a href='https://arxiv.org/abs/1806.02359' target='_blank'>link</a>)<br>\u2022 Resource Optimal Realization of Fault-Tolerant Quantum Circuit (<a href='https://ieeexplore.ieee.org/document/9171796' target='_blank'>link</a>)<br>\u2022 Error detection on quantum computers improves accuracy of chemical calculations (<a href='https://arxiv.org/abs/1910.00129' target='_blank'>link</a>)<br>\u2022 Experimental Characterization of Fault-Tolerant Circuits in Small-Scale Quantum Processors (<a href='https://arxiv.org/abs/2112.04076' target='_blank'>link</a>)<br>\u2022 Comparative analysis of error mitigation techniques for variational quantum eigensolver implementations on IBM quantum system (<a href='https://arxiv.org/abs/2206.07907' target='_blank'>link</a>)<br>\u2022 Encoding a magic state with beyond break-even fidelity (<a href='https://arxiv.org/abs/2305.13581' target='_blank'>link</a>)",
      "<b>Ion traps</b> - Repetition Code<br>2 experiments<br>12.5% of Repetition Code<br>3.5% of total<br>\u2022 Experimental Repetitive Quantum Error Correction (<a href='https://jubarreiro.physics.ucsd.edu/files/Schindler-Science-332-1059-1061.pdf' target='_blank'>link</a>)<br>\u2022 Realization of quantum error correction (<a href='https://doi.org/10.1038/nature03074' target='_blank'>link</a>)",
      "<b>NMR</b> - Repetition Code<br>3 experiments<br>18.8% of Repetition Code<br>5.3% of total<br>\u2022 Experimental Quantum Error Correction (<a href='https://arxiv.org/abs/quant-ph/9802018' target='_blank'>link</a>)<br>\u2022 Demonstration of Sufficient Control for Two Rounds of Quantum Error Correction in a Solid-State Ensemble Quantum Information Processor (<a href='https://arxiv.org/abs/1108.4842' target='_blank'>link</a>)<br>\u2022 Experimental quantum error correction with high fidelity (<a href='https://arxiv.org/abs/1109.4821' target='_blank'>link</a>)",
      "<b>NV centers</b> - Repetition Code<br>1 experiments<br>6.2% of Repetition Code<br>1.8% of total<br>\u2022 Quantum error correction in a solid-state hybrid spin register (<a href='https://arxiv.org/abs/1309.6424' target='_blank'>link</a>)",
      "<b>Superconducting circuit</b> - Repetition Code<br>10 experiments<br>62.5% of Repetition Code<br>17.5% of total<br>\u2022 Realization of Three-Qubit Quantum Error Correction with Superconducting Circuits (<a href='https://arxiv.org/abs/1109.4948' target='_blank'>link</a>)<br>\u2022 State preservation by repetitive error detection in a superconducting quantum circuit (<a href='https://arxiv.org/abs/1411.7403' target='_blank'>link</a>)<br>\u2022 Detecting bit-flip errors in a logical qubit using stabilizer measurements (<a href='https://arxiv.org/abs/1411.5542' target='_blank'>link</a>)<br>\u2022 Repeated quantum error correction on a continuously encoded qubit by real-time feedback (<a href='https://arxiv.org/abs/1508.01388' target='_blank'>link</a>)<br>\u2022 A repetition code of 15 qubits (<a href='https://arxiv.org/abs/1709.00990' target='_blank'>link</a>)<br>\u2022 Benchmarking near-term devices with quantum error correction (<a href='https://arxiv.org/abs/2004.11037' target='_blank'>link</a>)<br>\u2022 Exponential suppression of bit or phase flip errors with repetitive error correction (<a href='https://arxiv.org/abs/2102.06132' target='_blank'>link</a>)<br>\u2022 Suppressing quantum errors by scaling a surface code logical qubit (<a href='https://arxiv.org/abs/2207.06431' target='_blank'>link</a>)<br>\u2022 Hardware-efficient quantum error correction using concatenated bosonic qubits (<a href='https://arxiv.org/abs/2409.13025' target='_blank'>link</a>)<br>\u2022 Quantum error correction below the surface code threshold (<a href='https://arxiv.org/abs/2408.13687' target='_blank'>link</a>)",
      "<b>Neutral atoms</b> - Surface Code<br>2 experiments<br>25.0% of Surface Code<br>3.5% of total<br>\u2022 A quantum processor based on coherent transport of entangled atom arrays (<a href='https://arxiv.org/abs/2112.03923' target='_blank'>link</a>)<br>\u2022 Logical quantum processor based on reconfigurable atom arrays (<a href='https://arxiv.org/abs/2312.03982' target='_blank'>link</a>)",
      "<b>Photons</b> - Surface Code<br>1 experiments<br>12.5% of Surface Code<br>1.8% of total<br>\u2022 Experimental demonstration of a graph state quantum error-correction code (<a href='https://arxiv.org/abs/1404.5498' target='_blank'>link</a>)",
      "<b>Superconducting circuit</b> - Surface Code<br>5 experiments<br>62.5% of Surface Code<br>8.8% of total<br>\u2022 Repeated Quantum Error Detection in a Surface Code (<a href='https://arxiv.org/abs/1912.09410' target='_blank'>link</a>)<br>\u2022 Realizing repeated quantum error correction in a distance-three surface code (<a href='https://arxiv.org/abs/2112.03708' target='_blank'>link</a>)<br>\u2022 Suppressing quantum errors by scaling a surface code logical qubit (<a href='https://arxiv.org/abs/2207.06431' target='_blank'>link</a>)<br>\u2022 Quantum error correction below the surface code threshold (<a href='https://arxiv.org/abs/2408.13687' target='_blank'>link</a>)<br>\u2022 Demonstrating dynamic surface codes (<a href='https://arxiv.org/abs/2412.14360' target='_blank'>link</a>)",
      "<b>NMR</b> - [[5,1,3]] Perfect Code<br>2 experiments<br>66.7% of [[5,1,3]] Perfect Code<br>3.5% of total<br>\u2022 Benchmarking Quantum Computers: The Five-Qubit Error Correcting Code (<a href='https://arxiv.org/abs/quant-ph/0101034' target='_blank'>link</a>)<br>\u2022 Experimental implementation of encoded logical qubit operations in a perfect quantum error correcting code (<a href='https://arxiv.org/abs/1208.4797' target='_blank'>link</a>)",
      "<b>Superconducting circuit</b> - [[5,1,3]] Perfect Code<br>1 experiments<br>33.3% of [[5,1,3]] Perfect Code<br>1.8% of total<br>\u2022 Experimental exploration of five-qubit quantum error correcting code with superconducting qubits (<a href='https://arxiv.org/abs/1907.04507' target='_blank'>link</a>)"
    ],
    "hovertemplate": "%{customdata}<extra></extra>",
    "ids": [
      "All QEC Codes",
      "Bacon-Shor Code",
      "Bell State",
      "Cluster State",
      "Color Code",
      "Four-qubit Code",
      "Repetition Code",
      "Surface Code",
      "[[5,1,3]] Perfect Code",
      "Bacon-Shor Code-Ion traps",
      "Bacon-Shor Code-Neutral atoms",
      "Bacon-Shor Code-Photons",
      "Bell State-Superconducting circuit",
      "Cluster State-Neutral atoms",
      "Color Code-Ion traps",
      "Color Code-Neutral atoms",
      "Color Code-Superconducting circuit",
      "Four-qubit Code-Ion traps",
      "Four-qubit Code-Neutral atoms",
      "Four-qubit Code-Photons",
      "Four-qubit Code-Superconducting circuit",
      "Repetition Code-Ion traps",
      "Repetition Code-NMR",
      "Repetition Code-NV centers",
      "Repetition Code-Superconducting circuit",
      "Surface Code-Neutral atoms",
      "Surface Code-Photons",
      "Surface Code-Superconducting circuit",
      "[[5,1,3]] Perfect Code-NMR",
      "[[5,1,3]] Perfect Code-Superconducting circuit"
    ],
    "insidetextorientation": "radial",
    "labels": [
      "All QEC Codes (57)",
      "Bacon-Shor Code (3)",
      "Bell State (3)",
      "Cluster State (1)",
      "Color Code (7)",
      "Four-qubit Code (16)",
      "Repetition Code (16)",
      "Surface Code (8)",
      "[[5,1,3]] Perfect Code (3)",
      "Ion traps (1)",
      "Neutral atoms (1)",
      "Photons (1)",
      "Superconducting circuit (3)",
      "Neutral atoms (1)",
      "Ion traps (2)",
      "Neutral atoms (3)",
      "Superconducting circuit (2)",
      "Ion traps (2)",
      "Neutral atoms (2)",
      "Photons (1)",
      "Superconducting circuit (11)",
      "Ion traps (2)",
      "NMR (3)",
      "NV centers (1)",
      "Superconducting circuit (10)",
      "Neutral atoms (2)",
      "Photons (1)",
      "Superconducting circuit (5)",
      "NMR (2)",
      "Superconducting circuit (1)"
    ],
    "leaf": {
      "opacity": 1
    },
    "marker": {
      "line": {
        "color": "#ffffff",
        "width": 2
      }
    },
    "maxdepth": 3,
    "outsidetextfont": {
      "color": "#333333",
      "size": 16
    },
    "parents": [
      "",
      "All QEC Codes",
      "All QEC Codes",
      "All QEC Codes",
      "All QEC Codes",
      "All QEC Codes",
      "All QEC Codes",
      "All QEC Codes",
      "All QEC Codes",
      "Bacon-Shor Code",
      "Bacon-Shor Code",
      "Bacon-Shor Code",
      "Bell State",
      "Cluster State",
      "Color Code",
      "Color Code",
      "Color Code",
      "Four-qubit Code",
      "Four-qubit Code",
      "Four-qubit Code",
      "Four-qubit Code",
      "Repetition Code",
      "Repetition Code",
      "Repetition Code",
      "Repetition Code",
      "Surface Code",
      "Surface Code",
      "Surface Code",
      "[[5,1,3]] Perfect Code",
      "[[5,1,3]] Perfect Code"
    ],
    "textfont": {
      "size": 18,
      "family": "Arial"
    },
    "values": [
      57,
      3,
      3,
      1,
      7,
      16,
      16,
      8,
      3,
      1,
      1,
      1,
      3,
      1,
      2,
      3,
      2,
      2,
      2,
      1,
      11,
      2,
      3,
      1,
      10,
      2,
      1,
      5,
      2,
      1
    ],
    "type": "sunburst",
    "hoverlabel": {
      "font": {
        "family": "Arial"
      }
    }
  }
];

const qec_platform_sunburstLayout = {
  "font": {
    "color": "#2F3136",
    "family": "Arial",
    "size": 14
  },
  "height": 800,
  "hovermode": "closest",
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
    "text": "Distribution of QEC Implementations Across Platforms"
  },
  "width": 1000,
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

Plotly.newPlot('qec-platform-sunburst', qec_platform_sunburstData, qec_platform_sunburstLayout);

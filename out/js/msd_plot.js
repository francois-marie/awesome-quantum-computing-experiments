// Msd Plot Plot
const msd_plotData = [
  {
    "legendgroup": "header_platform",
    "legendrank": 0,
    "marker": {
      "color": "rgba(0,0,0,0)",
      "size": 0,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "\ud835\udc0f\ud835\udc25\ud835\udc1a\ud835\udc2d\ud835\udc1f\ud835\udc28\ud835\udc2b\ud835\udc26",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "platform_legend",
    "legendrank": 1,
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
    "name": "Neutral atoms",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "platform_legend",
    "legendrank": 2,
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
    "name": "Superconducting qubits",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "platform_legend",
    "legendrank": 3,
    "marker": {
      "color": "#FFC107",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "Trapped-ion",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "header_magic_state",
    "legendrank": 100,
    "marker": {
      "color": "rgba(0,0,0,0)",
      "size": 0,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "\ud835\udc0c\ud835\udc1a\ud835\udc20\ud835\udc22\ud835\udc1c \ud835\udc12\ud835\udc2d\ud835\udc1a\ud835\udc2d\ud835\udc1e",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "magic_state_legend",
    "legendrank": 101,
    "marker": {
      "color": "gray",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "triangle-up"
    },
    "mode": "markers",
    "name": "CZ",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "magic_state_legend",
    "legendrank": 102,
    "marker": {
      "color": "gray",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "H",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "magic_state_legend",
    "legendrank": 103,
    "marker": {
      "color": "gray",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "diamond"
    },
    "mode": "markers",
    "name": "M",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
    "legendgroup": "magic_state_legend",
    "legendrank": 104,
    "marker": {
      "color": "gray",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "square"
    },
    "mode": "markers",
    "name": "T",
    "showlegend": true,
    "x": [
      null
    ],
    "y": [
      null
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
      [
        "|M>",
        "Steane",
        "Preparation and Distillation",
        2024,
        "https://arxiv.org/abs/2412.15165"
      ]
    ],
    "hovertemplate": "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
    "legendgroup": "data_Neutral atoms_|M>",
    "marker": {
      "color": "#95A5A6",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "diamond"
    },
    "mode": "markers",
    "name": "Neutral atoms (|M>)",
    "showlegend": false,
    "text": [
      "Experimental Demonstration of Logical Magic State Distillation"
    ],
    "x": [
      1.0
    ],
    "y": [
      0.006000000000000005
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
    "error_y": {
      "array": [
        0.0040000000000000036
      ],
      "arrayminus": [
        0.0030000000000000027
      ],
      "color": "#95A5A6",
      "symmetric": false,
      "thickness": 2,
      "type": "data",
      "width": 4
    },
    "hoverinfo": "skip",
    "marker": {
      "color": "#95A5A6",
      "opacity": 0
    },
    "mode": "markers",
    "showlegend": false,
    "x": [
      1.0
    ],
    "y": [
      0.006000000000000005
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
      [
        "|CZ>",
        "Surface code",
        "Preparation",
        2023,
        "https://doi.org/10.1038/s41586-023-06846-3"
      ]
    ],
    "hovertemplate": "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
    "legendgroup": "data_Superconducting qubits_|CZ>",
    "marker": {
      "color": "#2ECC71",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "triangle-up"
    },
    "mode": "markers",
    "name": "Superconducting qubits (|CZ>)",
    "showlegend": false,
    "text": [
      "Encoding a magic state with beyond break-even fidelity"
    ],
    "x": [
      17.0
    ],
    "y": [
      0.012299999999999978
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
    "error_y": {
      "array": [
        0.0010999999999999899
      ],
      "arrayminus": [
        0.0010999999999999899
      ],
      "color": "#2ECC71",
      "symmetric": false,
      "thickness": 2,
      "type": "data",
      "width": 4
    },
    "hoverinfo": "skip",
    "marker": {
      "color": "#2ECC71",
      "opacity": 0
    },
    "mode": "markers",
    "showlegend": false,
    "x": [
      17.0
    ],
    "y": [
      0.012299999999999978
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
      [
        "|T>",
        "Surface code",
        "Preparation",
        2023,
        "https://doi.org/10.1103/PhysRevLett.131.210603"
      ],
      [
        "|T>",
        "Steane",
        "Preparation and Injection",
        2024,
        "https://arxiv.org/abs/2412.14256"
      ]
    ],
    "hovertemplate": "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
    "legendgroup": "data_Superconducting qubits_|T>",
    "marker": {
      "color": "#2ECC71",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "square"
    },
    "mode": "markers",
    "name": "Superconducting qubits (|T>)",
    "showlegend": false,
    "text": [
      "Logical Magic State Preparation with Fidelity beyond the Distillation Threshold on a Superconducting Quantum Processor",
      "Scaling and logic in the color code on a superconducting quantum processor"
    ],
    "x": [
      73.41,
      75.2
    ],
    "y": [
      0.12290000000000001,
      0.0008000000000000229
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
    "error_y": {
      "array": [
        0.0009000000000000119,
        0.0014999999999999458
      ],
      "arrayminus": [
        0.0009000000000000119,
        0.00029999999999996696
      ],
      "color": "#2ECC71",
      "symmetric": false,
      "thickness": 2,
      "type": "data",
      "width": 4
    },
    "hoverinfo": "skip",
    "marker": {
      "color": "#2ECC71",
      "opacity": 0
    },
    "mode": "markers",
    "showlegend": false,
    "x": [
      73.41,
      75.2
    ],
    "y": [
      0.12290000000000001,
      0.0008000000000000229
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
      [
        "|H>",
        "Surface code",
        "Preparation",
        2023,
        "https://doi.org/10.1103/PhysRevLett.131.210603"
      ],
      [
        "|H>",
        "Surface code",
        "Injection",
        2024,
        "https://arxiv.org/abs/2412.01446"
      ],
      [
        "|H>",
        "Steane",
        "Preparation and Injection",
        2024,
        "https://arxiv.org/abs/2412.14256"
      ]
    ],
    "hovertemplate": "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
    "legendgroup": "data_Superconducting qubits_|H>",
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
    "name": "Superconducting qubits (|H>)",
    "showlegend": false,
    "text": [
      "Logical Magic State Preparation with Fidelity beyond the Distillation Threshold on a Superconducting Quantum Processor",
      "Magic State Injection on IBM Quantum Processors Above the Distillation Threshold",
      "Scaling and logic in the color code on a superconducting quantum processor"
    ],
    "x": [
      73.41,
      36.3,
      74.6
    ],
    "y": [
      0.09099999999999997,
      0.11939999999999995,
      0.0040999999999999925
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
    "error_y": {
      "array": [
        0.009000000000000008,
        0.00019999999999997797,
        0.0037000000000000366
      ],
      "arrayminus": [
        0.009000000000000008,
        0.00019999999999997797,
        0.0038000000000000256
      ],
      "color": "#2ECC71",
      "symmetric": false,
      "thickness": 2,
      "type": "data",
      "width": 4
    },
    "hoverinfo": "skip",
    "marker": {
      "color": "#2ECC71",
      "opacity": 0
    },
    "mode": "markers",
    "showlegend": false,
    "x": [
      73.41,
      36.3,
      74.6
    ],
    "y": [
      0.09099999999999997,
      0.11939999999999995,
      0.0040999999999999925
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
      [
        "|H>",
        "Bacon-Shor",
        "Preparation",
        2020,
        "https://doi.org/10.1038/s41586-021-03928-y"
      ],
      [
        "|H>",
        "Steane",
        "Preparation",
        2021,
        "https://doi.org/10.1038/s41586-022-04721-1"
      ]
    ],
    "hovertemplate": "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
    "legendgroup": "data_Trapped-ion_|H>",
    "marker": {
      "color": "#FFC107",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "circle"
    },
    "mode": "markers",
    "name": "Trapped-ion (|H>)",
    "showlegend": false,
    "text": [
      "Fault-tolerant control of an error-corrected qubit",
      "Demonstration of fault-tolerant universal quantum gate operations"
    ],
    "x": [
      100.0,
      13.7
    ],
    "y": [
      0.028000000000000025,
      0.006000000000000005
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
    "error_y": {
      "array": [
        0.01200000000000001,
        0.014000000000000012
      ],
      "arrayminus": [
        0.01200000000000001,
        0.0050000000000000044
      ],
      "color": "#FFC107",
      "symmetric": false,
      "thickness": 2,
      "type": "data",
      "width": 4
    },
    "hoverinfo": "skip",
    "marker": {
      "color": "#FFC107",
      "opacity": 0
    },
    "mode": "markers",
    "showlegend": false,
    "x": [
      100.0,
      13.7
    ],
    "y": [
      0.028000000000000025,
      0.006000000000000005
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
      [
        "|T>",
        "Steane",
        "Preparation",
        2021,
        "https://doi.org/10.1103/PhysRevX.11.041058"
      ],
      [
        "|T>",
        "Steane, [[10,1,2]]",
        "Code Switching",
        2024,
        "https://doi.org/10.1038/s41567-024-02727-2"
      ],
      [
        "|T>",
        "[[15,1,3]], Steane",
        "Code Switching",
        2025,
        "https://doi.org/10.48550/arXiv.2506.14169"
      ]
    ],
    "hovertemplate": "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
    "legendgroup": "data_Trapped-ion_|T>",
    "marker": {
      "color": "#FFC107",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12,
      "symbol": "square"
    },
    "mode": "markers",
    "name": "Trapped-ion (|T>)",
    "showlegend": false,
    "text": [
      "Realization of real-time fault-tolerant quantum error correction",
      "Experimental fault-tolerant code switching",
      "Experimental demonstration of high-fidelity logical magic states from code switching"
    ],
    "x": [
      100.0,
      19.0,
      82.58
    ],
    "y": [
      0.02200000000000002,
      0.03700000000000003,
      0.0005100000000000104
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
    "error_y": {
      "array": [
        0.006000000000000005,
        0.0040000000000000036,
        0.00026999999999999247
      ],
      "arrayminus": [
        0.006000000000000005,
        0.0040000000000000036,
        0.00026999999999999247
      ],
      "color": "#FFC107",
      "symmetric": false,
      "thickness": 2,
      "type": "data",
      "width": 4
    },
    "hoverinfo": "skip",
    "marker": {
      "color": "#FFC107",
      "opacity": 0
    },
    "mode": "markers",
    "showlegend": false,
    "x": [
      100.0,
      19.0,
      82.58
    ],
    "y": [
      0.02200000000000002,
      0.03700000000000003,
      0.0005100000000000104
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

const msd_plotLayout = {
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
    "text": "Magic State Preparation: Error vs Acceptance Rate"
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
    "range": [
      0,
      105
    ],
    "showgrid": true,
    "tickcolor": "#2F3136",
    "ticklen": 5,
    "ticks": "outside",
    "tickwidth": 1,
    "title": {
      "text": "Acceptance Rate (%)"
    }
  },
  "yaxis": {
    "dtick": "D1",
    "gridcolor": "#E5E5E5",
    "linecolor": "#2F3136",
    "showgrid": true,
    "showline": true,
    "tickfont": {
      "color": "#2F3136",
      "family": "Arial, Helvetica, sans-serif",
      "size": 14
    },
    "title": {
      "font": {
        "color": "#2F3136",
        "family": "Arial, Helvetica, sans-serif",
        "size": 14
      },
      "text": "Error (1 - Fidelity)"
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

Plotly.newPlot('msd-plot', msd_plotData, msd_plotLayout);

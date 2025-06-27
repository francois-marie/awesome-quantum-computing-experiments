// Qubit Count Plot Plot
const qubit_count_plotData = [
  {
    "customdata": [
      "https://arxiv.org/abs/quant-ph/9806012",
      "https://www.nature.com/articles/35005011",
      "https://arxiv.org/abs/1009.6126",
      "https://arxiv.org/abs/1711.11092",
      "https://arxiv.org/abs/2302.00565"
    ],
    "hovertemplate": "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#FFC107",
      "width": 3
    },
    "marker": {
      "color": "#FFC107",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12
    },
    "mode": "markers",
    "name": "Ion traps",
    "text": [
      "Experimental Demonstration of a Controlled-NOT Quantum Gate",
      "Experimental Entanglement of Four Particles",
      "14-qubit entanglement: creation and coherence",
      "Observation of Entangled States of a Fully Controlled 20-Qubit System",
      "Controlling two-dimensional Coulomb crystals of more than 100 ions in a monolithic radio-frequency trap"
    ],
    "x": [
      1998,
      2000,
      2011,
      2017,
      2023
    ],
    "y": [
      2,
      4,
      14,
      20,
      100
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
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "Ion traps fit (\u00d72 every 5.0y)",
    "showlegend": true,
    "x": [
      1998,
      2023
    ],
    "y": [
      2.312210991968367,
      72.41642562019827
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
      "https://doi.org/10.1103/PhysRevX.9.031045"
    ],
    "hovertemplate": "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
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
      "size": 12
    },
    "mode": "markers",
    "name": "NV centers",
    "text": [
      "A Ten-Qubit Solid-State Spin Register with Quantum Memory up to One Minute"
    ],
    "x": [
      2019
    ],
    "y": [
      10
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
      "https://arxiv.org/abs/0908.0454",
      "https://arxiv.org/abs/1607.03042",
      "https://arxiv.org/abs/1707.04344",
      "https://arxiv.org/abs/1902.00284",
      "https://arxiv.org/abs/2012.12281",
      "https://arxiv.org/abs/2207.06500",
      "https://arxiv.org/abs/2403.12021",
      "https://doi.org/10.48550/arXiv.2412.14647",
      "https://doi.org/10.1103/PhysRevApplied.22.024073"
    ],
    "hovertemplate": "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
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
      "size": 12
    },
    "mode": "markers",
    "name": "Neutral atoms",
    "text": [
      "Entanglement of two individual neutral atoms using Rydberg blockade",
      "An atom-by-atom assembler of defect-free arbitrary 2d atomic arrays",
      "Probing many-body dynamics on a 51-atom quantum simulator",
      "Defect-free assembly of 2D clusters of more than 100 single-atom quantum systems",
      "Quantum Phases of Matter on a 256-Atom Programmable Quantum Simulator",
      "In-situ equalization of single-atom loading in large-scale optical tweezers arrays",
      "A tweezer array with 6100 highly coherent atomic qubits",
      "AI-Enabled Rapid Assembly of Thousands of Defect-Free Neutral Atom Arrays with Constant-time-overhead",
      "Rearrangement of individual atoms in a 2000-site optical-tweezer array at cryogenic temperatures"
    ],
    "x": [
      2010,
      2016,
      2017,
      2019,
      2021,
      2022,
      2024,
      2024,
      2024
    ],
    "y": [
      2,
      50,
      51,
      111,
      256,
      324,
      6100,
      2024,
      2088
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
    "name": "Neutral atoms fit (\u00d72 every 1.4y)",
    "showlegend": true,
    "x": [
      2010,
      2024
    ],
    "y": [
      1.650552029845658,
      1972.8793579052046
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
      "https://arxiv.org/abs/1708.04214",
      "https://doi.org/10.1038/s41586-021-03332-6",
      "https://arxiv.org/abs/2202.09252"
    ],
    "hovertemplate": "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
    "line": {
      "color": "#F7DC6F",
      "width": 3
    },
    "marker": {
      "color": "#F7DC6F",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12
    },
    "mode": "markers",
    "name": "Semiconductor spins",
    "text": [
      "A programmable two-qubit quantum processor in silicon",
      "A four-qubit germanium quantum processor",
      "Universal control of a six-qubit quantum processor in silicon"
    ],
    "x": [
      2018,
      2021,
      2022
    ],
    "y": [
      2,
      4,
      6
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
      "color": "#F7DC6F",
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "Semiconductor spins fit (\u00d72 every 2.6y)",
    "showlegend": true,
    "x": [
      2018,
      2022
    ],
    "y": [
      1.9601524522027287,
      5.648469838357207
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
      "https://www.science.org/doi/10.1126/science.1130886",
      "https://doi.org/10.1038/ncomms5015",
      "https://www.nature.com/articles/nature13171",
      "https://www.nature.com/articles/s41586-019-1666-5",
      "https://www.nature.com/articles/s41586-023-06096-3"
    ],
    "hovertemplate": "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
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
      "size": 12
    },
    "mode": "markers",
    "name": "Superconducting circuit",
    "text": [
      "Measurement of the Entanglement of Two Superconducting Qubits via State Tomography",
      "Implementing a strand of a scalable fault-tolerant quantum computing fabric",
      "Superconducting quantum circuits at the surface code threshold for fault tolerance",
      "Quantum supremacy using a programmable superconducting processor",
      "Evidence for the utility of quantum computing before fault tolerance"
    ],
    "x": [
      2006,
      2013,
      2014,
      2019,
      2023
    ],
    "y": [
      2,
      3,
      5,
      53,
      127
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
    "name": "Superconducting circuit fit (\u00d72 every 2.6y)",
    "showlegend": true,
    "x": [
      2006,
      2023
    ],
    "y": [
      1.02595373729172,
      98.69510829422686
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

const qubit_count_plotLayout = {
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
    "text": "Physical Qubit Count Evolution"
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
      "text": "Physical Qubit Count"
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

Plotly.newPlot('qubit-count-plot', qubit_count_plotData, qubit_count_plotLayout);

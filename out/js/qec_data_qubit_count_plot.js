// Qec Data Qubit Count Plot Plot
const qec_data_qubit_count_plotData = [
  {
    "hovertemplate": "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: Ion traps<extra></extra>",
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
    "mode": "lines+markers",
    "name": "Ion traps",
    "x": [
      2004,
      2011,
      2014,
      2017,
      2020,
      2024
    ],
    "y": [
      3.0,
      3.0,
      7.0,
      4.0,
      9.0,
      4.0
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
    "name": "Ion traps fit (\u00d72 every 22.0y)",
    "showlegend": true,
    "x": [
      2004,
      2024
    ],
    "y": [
      3.229739763566537,
      6.063345784406207
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
    "hovertemplate": "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: NMR<extra></extra>",
    "line": {
      "color": "#3498DB",
      "width": 3
    },
    "marker": {
      "color": "#3498DB",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12
    },
    "mode": "lines+markers",
    "name": "NMR",
    "x": [
      1998,
      2001,
      2011,
      2012
    ],
    "y": [
      3.0,
      5.0,
      3.0,
      5.0
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
      "color": "#3498DB",
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "NMR fit (\u00d72 every 101.1y)",
    "showlegend": true,
    "x": [
      1998,
      2012
    ],
    "y": [
      3.678848156318525,
      4.049501467651669
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
    "hovertemplate": "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: NV centers<extra></extra>",
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
    "mode": "lines+markers",
    "name": "NV centers",
    "x": [
      2014
    ],
    "y": [
      3.0
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
    "hovertemplate": "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: Neutral atoms<extra></extra>",
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
    "mode": "lines+markers",
    "name": "Neutral atoms",
    "x": [
      2021,
      2023,
      2024
    ],
    "y": [
      16.0,
      49.0,
      17.0
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
    "name": "Neutral atoms fit (\u00d72 every 7.1y)",
    "showlegend": true,
    "x": [
      2021,
      2024
    ],
    "y": [
      20.161269242261454,
      26.992598503134452
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
    "hovertemplate": "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: Photons<extra></extra>",
    "line": {
      "color": "#7A288A",
      "width": 3
    },
    "marker": {
      "color": "#7A288A",
      "line": {
        "color": "white",
        "width": 2
      },
      "size": 12
    },
    "mode": "lines+markers",
    "name": "Photons",
    "x": [
      2014,
      2020,
      2022
    ],
    "y": [
      4.0,
      9.0,
      4.0
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
      "color": "#7A288A",
      "dash": "dot",
      "width": 2
    },
    "mode": "lines",
    "name": "Photons fit (\u00d72 every 22.2y)",
    "showlegend": true,
    "x": [
      2014,
      2022
    ],
    "y": [
      4.531499299474124,
      5.815750529753256
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
    "hovertemplate": "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: Superconducting circuit<extra></extra>",
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
    "mode": "lines+markers",
    "name": "Superconducting circuit",
    "x": [
      2012,
      2014,
      2015,
      2016,
      2017,
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "y": [
      3.0,
      5.0,
      3.0,
      3.0,
      4.0,
      8.0,
      5.0,
      22.0,
      9.0,
      4.0,
      25.0,
      49.0
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
    "name": "Superconducting circuit fit (\u00d72 every 3.6y)",
    "showlegend": true,
    "x": [
      2012,
      2024
    ],
    "y": [
      2.129724418691146,
      21.02967787014283
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

const qec_data_qubit_count_plotLayout = {
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
    "text": "QEC Data Qubit Count Evolution"
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
      "text": "Number of Data Qubits"
    },
    "type": "linear"
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

Plotly.newPlot('qec-data-qubit-count-plot', qec_data_qubit_count_plotData, qec_data_qubit_count_plotLayout);

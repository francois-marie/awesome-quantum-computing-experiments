import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def sample_qec_data():
    return pd.DataFrame({
        'Article Title': ['Test QEC Paper'],
        'Link': ['https://arxiv.org/test'],
        'Year': [2024],
        'Platform': ['Test Platform'],
        'Code Parameters': ['[3,1,3]'],
        'Code Name': ['Repetition Code'],
        'Notes': ['Test note']
    })

@pytest.fixture
def sample_entangled_data():
    return pd.DataFrame({
        'Article Title': ['Test Entangled Paper'],
        'Link': ['https://arxiv.org/test'],
        'Year': [2024],
        'Platform': ['Test Platform'],
        'Entangled State Error': [0.001],
        'Notes': ['Test note']
    })

@pytest.fixture
def sample_qubit_count_data():
    return pd.DataFrame({
        'Article Title': ['Test Qubit Paper'],
        'Link': ['https://arxiv.org/test'],
        'Year': [2024],
        'Platform': ['Test Platform'],
        'Number of qubits': [100],
        'Notes': ['Test note']
    }) 
import pytest
import matplotlib.pyplot as plt
from src.plotting.base import BasePlot
from src.plotting.qubit_count_plot import QubitCountPlot
from src.plotting.entangled_error_plot import EntangledErrorPlot
from src.plotting.qec_time_plot import QECTimePlot
from src.plotting.nkd_plot import NKDPlot

class TestBasePlot:
    def test_setup_plot(self, mocker):
        # Create a concrete class for testing the abstract base class
        class TestPlot(BasePlot):
            def create_plot(self):
                pass
        
        plot = TestPlot()
        plot.setup_plot("Test Title", "X Label", "Y Label")
        
        assert plt.gca().get_title() == "Test Title"
        assert plt.gca().get_xlabel() == "X Label"
        assert plt.gca().get_ylabel() == "Y Label"
        plt.close()

class TestQubitCountPlot:
    def test_load_data(self, sample_qubit_count_data, mocker):
        mocker.patch('pandas.read_csv', return_value=sample_qubit_count_data)
        plot = QubitCountPlot()
        assert 'Number of qubits' in plot.data.columns
        assert plot.data['Year'].dtype.kind in 'int'
    
    def test_create_plot(self, sample_qubit_count_data, mocker):
        mocker.patch('pandas.read_csv', return_value=sample_qubit_count_data)
        plot = QubitCountPlot()
        plot.create_plot()
        assert plt.gca().get_yscale() == 'log'
        plt.close()

class TestEntangledErrorPlot:
    def test_load_data(self, sample_entangled_data, mocker):
        mocker.patch('pandas.read_csv', return_value=sample_entangled_data)
        plot = EntangledErrorPlot()
        assert 'Entangled State Error' in plot.data.columns
        assert plot.data['Year'].dtype.kind in 'int'
    
    def test_create_plot(self, sample_entangled_data, mocker):
        mocker.patch('pandas.read_csv', return_value=sample_entangled_data)
        plot = EntangledErrorPlot()
        plot.create_plot()
        assert plt.gca().get_yscale() == 'log'
        plt.close()

    def test_parse_code_parameters_brackets(self):
        plot = NKDPlot()
        
        # Test single bracket case
        n, k, d = plot.parse_code_parameters("[3,1,3]")
        assert n == [3]
        assert k == [1]
        assert d == [1], "Single brackets should give d=1"
        
        # Test double bracket case
        n, k, d = plot.parse_code_parameters("[[3,1,3]]")
        assert n == [3]
        assert k == [1]
        assert d == [3], "Double brackets should preserve original d"
        
        # Test multiple parameters case with single brackets
        n, k, d = plot.parse_code_parameters("[3,1,3],[5,1,3]")
        assert n == [3, 5]
        assert k == [1, 1]
        assert d == [1, 1], "Multiple single-bracket parameters should all have d=1"
        
        # Test mixed case
        n, k, d = plot.parse_code_parameters("[[3,1,3]],[5,1,3]")
        assert n == [3, 5]
        assert k == [1, 1]
        assert d == [3, 1], "Mixed brackets should respect each parameter's bracket type" 
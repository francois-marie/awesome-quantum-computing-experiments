import pytest
import pandas as pd
from src.markdown.base import ExperimentSection
from src.markdown.sections import QECSection, EntangledSection, QubitCountSection, PhysicalQubitsSection
from src.markdown.generator import MarkdownGenerator

class TestExperimentSection:
    def test_format_anchor(self):
        assert ExperimentSection.format_anchor("[Test] Name, 123") == "test-name-123"
        assert ExperimentSection.format_anchor("[[5,1,3]] Code") == "513-code"

class TestQECSection:
    def test_generate_content(self, sample_qec_data):
        section = QECSection(sample_qec_data)
        content = section.generate_content()
        assert "## Quantum Error Correction" in content
        assert "[Test QEC Paper]" in content
        assert "[3,1,3]" in content
        assert "Test Platform" in content
    
    def test_generate_toc(self, sample_qec_data):
        section = QECSection(sample_qec_data)
        toc = section.generate_toc()
        assert "- [Repetition Code](#repetition-code)" in toc

class TestEntangledSection:
    def test_generate_content(self, sample_entangled_data):
        section = EntangledSection(sample_entangled_data)
        content = section.generate_content()
        assert "## Entangled State Error" in content
        assert "[Test Entangled Paper]" in content
        assert "0.001" in content
        assert "Test Platform" in content

class TestMarkdownGenerator:
    def test_generate(self, mocker, sample_qec_data, sample_entangled_data, 
                     sample_qubit_count_data, sample_physical_qubits_data):
        # Mock data loading
        mock_msd_data = pd.DataFrame({
            "Article Title": [],
            "Link": [],
            "Year": [],
            "Platform": [],
            "Code Name": [],
            "Notes": []
        })
        
        mocker.patch('pandas.read_csv', side_effect=[
            sample_qec_data,
            mock_msd_data,  # msd data with proper columns
            sample_entangled_data,
            sample_qubit_count_data,
            sample_physical_qubits_data  # Add the mock physical qubits data here
        ])
        
        # Mock file writing
        mock_write = mocker.patch('pathlib.Path.write_text')
        
        generator = MarkdownGenerator()
        generator.generate()
        
        # Verify the write was called
        assert mock_write.called
        content = mock_write.call_args[0][0]
        assert "# Awesome Quantum Computing Experiments" in content
        assert "## Table of Contents" in content
        assert "## Contributing" in content 

class TestPhysicalQubitsSection:
    def test_generate_content(self, sample_physical_qubits_data):
        section = PhysicalQubitsSection(sample_physical_qubits_data)
        content = section.generate_content()
        assert "## Physical Qubits" in content
        assert "[Test Physical Qubit Paper]" in content
        assert "T1: 5e-08s" in content
        assert "T2: 1e-07s" in content
        assert "Test Platform" in content 
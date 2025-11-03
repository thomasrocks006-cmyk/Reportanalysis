"""
Tests for the synthesis stage.
"""

import pytest
import pandas as pd
import numpy as np

from reportanalysis.pipeline.synthesis import SynthesisStage


class TestSynthesisStage:
    """Test cases for SynthesisStage."""
    
    def test_initialization(self):
        """Test stage initialization."""
        config = {'enable_ai_insights': True}
        stage = SynthesisStage(config)
        
        assert stage.config == config
    
    def test_execute_returns_dict(self):
        """Test that execute returns expected structure."""
        # Create sample data
        data = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': [10, 20, 30, 40, 50],
            'col3': ['A', 'B', 'A', 'B', 'C']
        })
        
        stage = SynthesisStage({})
        result = stage.execute(data)
        
        assert isinstance(result, dict)
        assert 'raw_data' in result
        assert 'summary' in result
        assert 'temporal_aggregations' in result
        assert 'categorical_aggregations' in result
        assert 'data_quality' in result
        assert 'metadata' in result
    
    def test_summary_generation(self):
        """Test summary generation."""
        data = pd.DataFrame({
            'numeric': [1, 2, 3, 4, 5],
            'category': ['A', 'B', 'A', 'B', 'C']
        })
        
        stage = SynthesisStage({})
        result = stage.execute(data)
        
        summary = result['summary']
        assert summary['total_rows'] == 5
        assert summary['total_columns'] == 2
        assert 'numeric' in summary['numeric_summary']
        assert 'category' in summary['categorical_summary']
    
    def test_data_quality_assessment(self):
        """Test data quality metrics."""
        data = pd.DataFrame({
            'col1': [1, 2, np.nan, 4, 5],
            'col2': [10, 20, 30, np.nan, 50]
        })
        
        stage = SynthesisStage({})
        result = stage.execute(data)
        
        quality = result['data_quality']
        assert 'completeness' in quality
        assert 'missing_values' in quality
        assert quality['missing_values'] == 2
        assert quality['completeness'] < 100

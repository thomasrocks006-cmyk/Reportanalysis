"""
Integration tests for the complete pipeline.
"""

import pytest
import tempfile
from pathlib import Path
import pandas as pd
import numpy as np

from reportanalysis import ReportPipeline
from reportanalysis.utils.config import ConfigManager


class TestReportPipeline:
    """Integration tests for the complete report generation pipeline."""
    
    def test_complete_pipeline_csv(self):
        """Test the complete pipeline with CSV data."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("date,sales,units,category\n")
            f.write("2023-01-01,1000,50,A\n")
            f.write("2023-01-02,1500,75,B\n")
            f.write("2023-01-03,1200,60,A\n")
            f.write("2023-01-04,1800,90,B\n")
            f.write("2023-01-05,1600,80,C\n")
            temp_csv = f.name
        
        # Create temporary output path
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_pdf = f.name
        
        try:
            # Initialize pipeline with default config
            config = ConfigManager.load_config()
            pipeline = ReportPipeline(config)
            
            # Run pipeline
            report_path = pipeline.run(temp_csv, temp_pdf)
            
            # Verify report was created
            assert report_path.exists()
            assert report_path.suffix == '.pdf'
            assert report_path.stat().st_size > 0
            
        finally:
            Path(temp_csv).unlink()
            if Path(temp_pdf).exists():
                Path(temp_pdf).unlink()
    
    def test_pipeline_status(self):
        """Test pipeline status method."""
        config = ConfigManager.load_config()
        pipeline = ReportPipeline(config)
        
        status = pipeline.get_status()
        
        assert 'version' in status
        assert 'stages' in status
        assert 'mcp_connected' in status
        
        assert status['stages']['data_ingestion'] == 'ready'
        assert status['stages']['synthesis'] == 'ready'
        assert status['stages']['analysis'] == 'ready'
        assert status['stages']['report_generation'] == 'ready'
    
    def test_pipeline_with_custom_config(self):
        """Test pipeline with custom configuration."""
        config = {
            'data': {'min_rows': 3},
            'synthesis': {'enable_ai_insights': False},
            'analysis': {'correlation_threshold': 0.8},
            'report': {'include_visualizations': True},
            'mcp': {'enabled': False}
        }
        
        pipeline = ReportPipeline(config)
        
        # Verify configuration is applied
        assert pipeline.data_ingestion.config['min_rows'] == 3
        assert pipeline.analysis.config['correlation_threshold'] == 0.8

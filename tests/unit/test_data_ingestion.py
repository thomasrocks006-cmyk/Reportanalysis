"""
Tests for the data ingestion stage.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile

from reportanalysis.pipeline.data_ingestion import DataIngestionStage


class TestDataIngestionStage:
    """Test cases for DataIngestionStage."""
    
    def test_initialization(self):
        """Test stage initialization."""
        config = {'min_rows': 10}
        stage = DataIngestionStage(config)
        
        assert stage.config == config
        assert len(stage.supported_formats) > 0
    
    def test_load_csv(self):
        """Test loading CSV data."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1,col2,col3\n")
            f.write("1,2,3\n")
            f.write("4,5,6\n")
            temp_path = f.name
        
        try:
            stage = DataIngestionStage({})
            data = stage.execute(temp_path)
            
            assert isinstance(data, pd.DataFrame)
            assert len(data) == 2
            assert len(data.columns) == 3
        finally:
            Path(temp_path).unlink()
    
    def test_file_not_found(self):
        """Test error handling for non-existent file."""
        stage = DataIngestionStage({})
        
        with pytest.raises(FileNotFoundError):
            stage.execute('/nonexistent/path/file.csv')
    
    def test_unsupported_format(self):
        """Test error handling for unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            stage = DataIngestionStage({})
            
            with pytest.raises(ValueError, match="Unsupported file format"):
                stage.execute(temp_path)
        finally:
            Path(temp_path).unlink()
    
    def test_validation_min_rows(self):
        """Test data validation for minimum rows."""
        # Create temporary CSV with insufficient rows
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1,col2\n")
            f.write("1,2\n")
            temp_path = f.name
        
        try:
            stage = DataIngestionStage({'min_rows': 10})
            
            with pytest.raises(ValueError, match="minimum required"):
                stage.execute(temp_path)
        finally:
            Path(temp_path).unlink()

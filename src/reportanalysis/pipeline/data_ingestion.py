"""
Data Ingestion Stage - Loads and validates historical data from various sources.

Supports multiple data formats including CSV, Excel, JSON, and SQL databases.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Union
import pandas as pd

logger = logging.getLogger(__name__)


class DataIngestionStage:
    """
    Stage 1: Data Ingestion
    
    Responsible for loading historical data from various sources and
    performing initial validation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data ingestion stage.
        
        Args:
            config: Configuration dictionary for data ingestion
        """
        self.config = config
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.parquet']
        logger.info("Data ingestion stage initialized")
    
    def execute(self, data_source: Union[str, Path]) -> pd.DataFrame:
        """
        Load and validate data from the specified source.
        
        Args:
            data_source: Path to the data file or directory
            
        Returns:
            pandas DataFrame containing the loaded data
            
        Raises:
            FileNotFoundError: If the data source doesn't exist
            ValueError: If the data format is not supported
        """
        data_path = Path(data_source)
        
        if not data_path.exists():
            raise FileNotFoundError(f"Data source not found: {data_source}")
        
        # Detect file format and load accordingly
        suffix = data_path.suffix.lower()
        
        logger.info(f"Loading data from: {data_path}")
        
        if suffix == '.csv':
            data = self._load_csv(data_path)
        elif suffix in ['.xlsx', '.xls']:
            data = self._load_excel(data_path)
        elif suffix == '.json':
            data = self._load_json(data_path)
        elif suffix == '.parquet':
            data = self._load_parquet(data_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        # Validate data
        self._validate_data(data)
        
        logger.info(f"Successfully loaded {len(data)} rows and {len(data.columns)} columns")
        return data
    
    def _load_csv(self, path: Path) -> pd.DataFrame:
        """Load data from CSV file."""
        encoding = self.config.get('csv_encoding', 'utf-8')
        return pd.read_csv(path, encoding=encoding)
    
    def _load_excel(self, path: Path) -> pd.DataFrame:
        """Load data from Excel file."""
        sheet_name = self.config.get('excel_sheet', 0)
        return pd.read_excel(path, sheet_name=sheet_name)
    
    def _load_json(self, path: Path) -> pd.DataFrame:
        """Load data from JSON file."""
        orient = self.config.get('json_orient', 'records')
        return pd.read_json(path, orient=orient)
    
    def _load_parquet(self, path: Path) -> pd.DataFrame:
        """Load data from Parquet file."""
        return pd.read_parquet(path)
    
    def _validate_data(self, data: pd.DataFrame) -> None:
        """
        Validate the loaded data.
        
        Args:
            data: DataFrame to validate
            
        Raises:
            ValueError: If validation fails
        """
        if data.empty:
            raise ValueError("Loaded data is empty")
        
        min_rows = self.config.get('min_rows', 1)
        if len(data) < min_rows:
            raise ValueError(f"Data has only {len(data)} rows, minimum required: {min_rows}")
        
        logger.info("Data validation passed")

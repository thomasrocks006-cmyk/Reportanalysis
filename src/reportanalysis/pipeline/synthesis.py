"""
Synthesis Stage - Processes and aggregates raw data into meaningful structures.

Uses MCP for intelligent data summarization and pattern detection.
"""

import logging
from typing import Dict, Any
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class SynthesisStage:
    """
    Stage 2: Data Synthesis
    
    Processes raw data, performs aggregations, and creates
    synthesized data structures for analysis.
    """
    
    def __init__(self, config: Dict[str, Any], mcp_client=None):
        """
        Initialize the synthesis stage.
        
        Args:
            config: Configuration dictionary for synthesis
            mcp_client: MCP client for AI-powered synthesis
        """
        self.config = config
        self.mcp_client = mcp_client
        logger.info("Synthesis stage initialized")
    
    def execute(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Synthesize the raw data into structured formats.
        
        Args:
            data: Raw data DataFrame
            
        Returns:
            Dictionary containing synthesized data structures
        """
        logger.info("Starting data synthesis")
        
        synthesized = {
            'raw_data': data,
            'summary': self._generate_summary(data),
            'temporal_aggregations': self._temporal_aggregations(data),
            'categorical_aggregations': self._categorical_aggregations(data),
            'data_quality': self._assess_data_quality(data),
            'metadata': self._extract_metadata(data)
        }
        
        # Use MCP for intelligent insights if available
        if self.mcp_client and self.mcp_client.is_connected():
            synthesized['ai_insights'] = self._generate_ai_insights(data)
        
        logger.info("Data synthesis completed")
        return synthesized
    
    def _generate_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate statistical summary of the data."""
        summary = {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'column_types': data.dtypes.astype(str).to_dict(),
            'numeric_summary': {},
            'categorical_summary': {}
        }
        
        # Numeric columns summary
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            summary['numeric_summary'][col] = {
                'mean': float(data[col].mean()),
                'median': float(data[col].median()),
                'std': float(data[col].std()),
                'min': float(data[col].min()),
                'max': float(data[col].max()),
                'missing': int(data[col].isna().sum())
            }
        
        # Categorical columns summary
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            value_counts = data[col].value_counts()
            summary['categorical_summary'][col] = {
                'unique_values': int(data[col].nunique()),
                'top_values': value_counts.head(5).to_dict(),
                'missing': int(data[col].isna().sum())
            }
        
        return summary
    
    def _temporal_aggregations(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform temporal aggregations if date columns exist."""
        date_columns = data.select_dtypes(include=['datetime64']).columns
        
        if len(date_columns) == 0:
            # Try to detect date columns without modifying original data
            for col in data.columns:
                try:
                    # Test conversion without modifying original
                    pd.to_datetime(data[col])
                    date_columns = [col]
                    break
                except (ValueError, TypeError):
                    continue
        
        temporal = {}
        if len(date_columns) > 0:
            date_col = date_columns[0]
            # Convert to datetime for temporal analysis
            date_data = pd.to_datetime(data[date_col])
            temporal['date_range'] = {
                'start': str(date_data.min()),
                'end': str(date_data.max())
            }
        
        return temporal
    
    def _categorical_aggregations(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform categorical aggregations."""
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
        aggregations = {}
        for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
            aggregations[col] = data[col].value_counts().to_dict()
        
        return aggregations
    
    def _assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess overall data quality."""
        total_cells = len(data) * len(data.columns)
        missing_cells = data.isna().sum().sum()
        
        return {
            'completeness': float((total_cells - missing_cells) / total_cells * 100),
            'missing_values': int(missing_cells),
            'duplicate_rows': int(data.duplicated().sum()),
            'total_cells': int(total_cells)
        }
    
    def _extract_metadata(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Extract metadata about the dataset."""
        return {
            'shape': list(data.shape),
            'columns': list(data.columns),
            'memory_usage': int(data.memory_usage(deep=True).sum())
        }
    
    def _generate_ai_insights(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate AI-powered insights using MCP."""
        try:
            # Use MCP to generate insights
            insights = self.mcp_client.generate_insights(data.head(100).to_dict())
            return insights
        except Exception as e:
            logger.warning(f"Failed to generate AI insights: {str(e)}")
            return {}

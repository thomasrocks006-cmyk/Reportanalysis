"""
Pipeline orchestrator that coordinates the entire report generation process.

The pipeline follows these stages:
1. Data Ingestion - Load and validate historical data
2. Synthesis - Process and aggregate data
3. Analysis - Perform statistical analysis and insights generation
4. Report Generation - Create visually aesthetic reports
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

from reportanalysis.pipeline.data_ingestion import DataIngestionStage
from reportanalysis.pipeline.synthesis import SynthesisStage
from reportanalysis.pipeline.analysis import AnalysisStage
from reportanalysis.pipeline.report_generation import ReportGenerationStage
from reportanalysis.mcp_integration.mcp_client import MCPClient

logger = logging.getLogger(__name__)


class ReportPipeline:
    """
    Orchestrates the entire report generation pipeline.
    
    Attributes:
        config: Configuration dictionary for pipeline stages
        mcp_client: MCP client for AI-powered capabilities
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the report pipeline.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.mcp_client = MCPClient(self.config.get('mcp', {}))
        
        # Initialize pipeline stages
        self.data_ingestion = DataIngestionStage(self.config.get('data', {}))
        self.synthesis = SynthesisStage(self.config.get('synthesis', {}), self.mcp_client)
        self.analysis = AnalysisStage(self.config.get('analysis', {}), self.mcp_client)
        self.report_generation = ReportGenerationStage(
            self.config.get('report', {}), 
            self.mcp_client
        )
        
        logger.info("Report pipeline initialized")
    
    def run(self, data_source: str, output_path: str) -> Path:
        """
        Execute the complete report generation pipeline.
        
        Args:
            data_source: Path to the input data file or directory
            output_path: Path where the report should be saved
            
        Returns:
            Path to the generated report
        """
        logger.info(f"Starting pipeline with data source: {data_source}")
        
        try:
            # Stage 1: Data Ingestion
            logger.info("Stage 1: Data Ingestion")
            raw_data = self.data_ingestion.execute(data_source)
            
            # Stage 2: Synthesis
            logger.info("Stage 2: Data Synthesis")
            synthesized_data = self.synthesis.execute(raw_data)
            
            # Stage 3: Analysis
            logger.info("Stage 3: Data Analysis")
            analysis_results = self.analysis.execute(synthesized_data)
            
            # Stage 4: Report Generation
            logger.info("Stage 4: Report Generation")
            report_path = self.report_generation.execute(
                analysis_results, 
                output_path
            )
            
            logger.info(f"Pipeline completed successfully. Report saved to: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the pipeline.
        
        Returns:
            Dictionary containing pipeline status information
        """
        return {
            'version': '0.1.0',
            'stages': {
                'data_ingestion': 'ready',
                'synthesis': 'ready',
                'analysis': 'ready',
                'report_generation': 'ready'
            },
            'mcp_connected': self.mcp_client.is_connected()
        }

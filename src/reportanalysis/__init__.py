"""
Report Analysis - A comprehensive report generation system for historical data analysis.

This package provides a pipeline-based approach to generate high-quality, visually
aesthetic reports from historical data using MCP (Model Context Protocol) integration.
"""

__version__ = "0.1.0"
__author__ = "Report Analysis Team"

from reportanalysis.pipeline.orchestrator import ReportPipeline

__all__ = ["ReportPipeline"]

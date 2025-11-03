#!/usr/bin/env python3
"""
Example: Generate a report from CSV data

This example demonstrates how to use the Report Analysis library
to generate a professional report from a CSV file.
"""

from reportanalysis import ReportPipeline
from reportanalysis.utils.config import ConfigManager
from reportanalysis.utils.logging_config import setup_logging


def main():
    """Generate a report from the sample sales data."""
    
    # Setup logging
    setup_logging(level='INFO')
    
    # Load configuration (or use defaults)
    config = ConfigManager.load_config()
    
    # You can customize the configuration
    config['report']['include_visualizations'] = True
    config['analysis']['trend_analysis'] = True
    
    # Initialize the pipeline
    print("Initializing report generation pipeline...")
    pipeline = ReportPipeline(config)
    
    # Run the pipeline
    print("Processing data and generating report...")
    report_path = pipeline.run(
        data_source='examples/data/sample_sales_data.csv',
        output_path='output/example_report.pdf'
    )
    
    print(f"\n✓ Report generated successfully!")
    print(f"  Location: {report_path}")
    print(f"\nThe report includes:")
    print("  - Executive summary with key findings")
    print("  - Data quality assessment")
    print("  - Statistical analysis")
    print("  - Visualizations (distributions, correlations)")
    print("  - Actionable recommendations")


if __name__ == '__main__':
    main()

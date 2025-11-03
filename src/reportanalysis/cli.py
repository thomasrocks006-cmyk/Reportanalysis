"""
Command-line interface for the Report Analysis application.

Provides easy-to-use commands for generating reports from historical data.
"""

import click
import logging
from pathlib import Path

from reportanalysis.pipeline.orchestrator import ReportPipeline
from reportanalysis.utils.config import ConfigManager
from reportanalysis.utils.logging_config import setup_logging


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--log-file', type=click.Path(), help='Log file path')
@click.pass_context
def cli(ctx, verbose, log_file):
    """
    Report Analysis - Generate high-quality reports from historical data.
    
    A comprehensive pipeline for data ingestion, synthesis, analysis,
    and professional report generation.
    """
    ctx.ensure_object(dict)
    
    # Setup logging
    log_level = 'DEBUG' if verbose else 'INFO'
    setup_logging(level=log_level, log_file=log_file)
    
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('data_source', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.pass_context
def generate(ctx, data_source, output_path, config):
    """
    Generate a report from historical data.
    
    DATA_SOURCE: Path to the input data file (CSV, Excel, JSON, Parquet)
    OUTPUT_PATH: Path where the report PDF should be saved
    
    Example:
        reportanalysis generate data.csv report.pdf
        reportanalysis generate sales.xlsx quarterly_report.pdf --config config.yaml
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info("Starting report generation")
        
        # Load configuration
        config_dict = ConfigManager.load_config(config)
        
        # Initialize pipeline
        pipeline = ReportPipeline(config_dict)
        
        # Run pipeline
        click.echo(f"Processing data from: {data_source}")
        report_path = pipeline.run(data_source, output_path)
        
        click.echo(f"\n✓ Report generated successfully!")
        click.echo(f"  Location: {report_path}")
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Report generation failed: {str(e)}", exc_info=True)
        click.echo(f"\n✗ Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--output', '-o', default='config.yaml', help='Output configuration file path')
def init_config(output):
    """
    Generate a default configuration file.
    
    Creates a configuration file with default settings that can be customized.
    
    Example:
        reportanalysis init-config
        reportanalysis init-config --output my_config.yaml
    """
    try:
        config = ConfigManager.DEFAULT_CONFIG
        ConfigManager.save_config(config, output)
        
        click.echo(f"✓ Configuration file created: {output}")
        click.echo("  Edit this file to customize report generation settings.")
        
    except Exception as e:
        click.echo(f"✗ Error creating config file: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def status(config):
    """
    Check the status of the report generation pipeline.
    
    Displays information about pipeline components and configuration.
    
    Example:
        reportanalysis status
        reportanalysis status --config config.yaml
    """
    try:
        # Load configuration
        config_dict = ConfigManager.load_config(config)
        
        # Initialize pipeline
        pipeline = ReportPipeline(config_dict)
        
        # Get status
        status_info = pipeline.get_status()
        
        click.echo("\nReport Analysis Pipeline Status")
        click.echo("=" * 40)
        click.echo(f"Version: {status_info['version']}")
        click.echo(f"\nPipeline Stages:")
        for stage, state in status_info['stages'].items():
            icon = "✓" if state == "ready" else "✗"
            click.echo(f"  {icon} {stage}: {state}")
        
        click.echo(f"\nMCP Integration: {'Connected' if status_info['mcp_connected'] else 'Not connected'}")
        
    except Exception as e:
        click.echo(f"✗ Error checking status: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
def version():
    """Display version information."""
    from reportanalysis import __version__
    click.echo(f"Report Analysis version {__version__}")


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()

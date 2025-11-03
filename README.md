# Report Analysis

A comprehensive report generation system for creating accurate, high-quality reports from historical data.

## Overview

Report Analysis provides a complete pipeline for transforming raw historical data into professional, visually aesthetic reports. The system leverages a four-stage pipeline architecture with optional MCP (Model Context Protocol) integration for AI-powered insights.

## Features

### 🔄 Complete Pipeline Architecture
- **Data Ingestion**: Load data from CSV, Excel, JSON, and Parquet formats
- **Synthesis**: Process and aggregate data with intelligent summarization
- **Analysis**: Perform statistical analysis, trend detection, and correlation analysis
- **Report Generation**: Create professional PDF reports with visualizations

### 📊 Advanced Analytics
- Descriptive statistics and distributions
- Correlation analysis with heatmaps
- Trend detection and forecasting
- Outlier detection using IQR method
- Data quality assessment

### 🎨 Visual Reports
- Professional PDF generation with custom styling
- Distribution plots and correlation heatmaps
- Clean, modern design with color-coded sections
- Executive summaries and key findings
- Actionable recommendations

### 🤖 MCP Integration
- Optional integration with Model Context Protocol servers
- AI-powered insights and pattern detection
- Enhanced analysis capabilities
- Intelligent report enhancements

## Installation

### From Source

```bash
git clone https://github.com/thomasrocks006-cmyk/Reportanalysis.git
cd Reportanalysis
pip install -r requirements.txt
pip install -e .
```

### Dependencies

- Python 3.8+
- pandas, numpy
- matplotlib, seaborn, plotly
- reportlab
- pyyaml, click

See `requirements.txt` for complete list.

## Quick Start

### Generate Your First Report

```bash
# Using the included sample data
reportanalysis generate examples/data/sample_sales_data.csv output/report.pdf

# With custom configuration
reportanalysis generate data.csv report.pdf --config config.yaml
```

### Initialize Configuration

```bash
# Create a default configuration file
reportanalysis init-config

# Create with custom path
reportanalysis init-config --output my_config.yaml
```

### Check Status

```bash
# Check pipeline status
reportanalysis status

# With configuration
reportanalysis status --config config.yaml
```

## Pipeline Architecture

```
┌─────────────────┐
│  Data Sources   │
│ CSV/Excel/JSON  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 1. Data         │
│    Ingestion    │  ← Load and validate data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Synthesis    │  ← Aggregate and summarize
│    (+ MCP)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Analysis     │  ← Statistical analysis
│    (+ MCP)      │     and insights
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Report       │  ← Generate PDF with
│    Generation   │     visualizations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Report     │
└─────────────────┘
```

## Usage Examples

### Python API

```python
from reportanalysis import ReportPipeline
from reportanalysis.utils.config import ConfigManager

# Load configuration
config = ConfigManager.load_config('config.yaml')

# Initialize pipeline
pipeline = ReportPipeline(config)

# Generate report
report_path = pipeline.run(
    data_source='data/sales.csv',
    output_path='output/sales_report.pdf'
)

print(f"Report generated: {report_path}")
```

### Command Line

```bash
# Basic usage
reportanalysis generate input.csv output.pdf

# With verbose logging
reportanalysis generate input.csv output.pdf --verbose

# With custom config and log file
reportanalysis generate input.csv output.pdf \
    --config config.yaml \
    --log-file report.log
```

## Configuration

The system can be configured using a YAML file. Generate a default configuration:

```bash
reportanalysis init-config --output config.yaml
```

### Configuration Options

```yaml
# Data ingestion settings
data:
  min_rows: 1
  csv_encoding: utf-8
  excel_sheet: 0
  json_orient: records

# Synthesis settings
synthesis:
  enable_ai_insights: true

# Analysis settings
analysis:
  correlation_threshold: 0.7
  outlier_method: iqr
  trend_analysis: true

# Report generation settings
report:
  page_size: letter
  include_visualizations: true
  max_charts: 10

# MCP integration (optional)
mcp:
  enabled: false
  server_url: ""
  timeout: 30
```

## MCP Integration

Report Analysis supports integration with Model Context Protocol (MCP) servers for enhanced AI capabilities:

1. Configure MCP in `config.yaml`:
```yaml
mcp:
  enabled: true
  server_url: "http://your-mcp-server:8000"
  timeout: 30
```

2. The pipeline will automatically use MCP for:
   - Intelligent data insights
   - Pattern detection
   - Advanced analysis
   - Report enhancements

## Example Data

Sample data is included in `examples/data/sample_sales_data.csv`:
- 500 records of historical sales data
- Multiple dimensions: sales, units, customers, categories, regions
- Time series data for trend analysis
- Realistic correlations and patterns

## Development

### Running Tests

```bash
pytest tests/
```

### Project Structure

```
Reportanalysis/
├── src/reportanalysis/          # Main package
│   ├── pipeline/                # Pipeline stages
│   │   ├── orchestrator.py     # Pipeline orchestration
│   │   ├── data_ingestion.py   # Data loading
│   │   ├── synthesis.py        # Data processing
│   │   ├── analysis.py         # Statistical analysis
│   │   └── report_generation.py # PDF generation
│   ├── mcp_integration/         # MCP client
│   │   └── mcp_client.py
│   ├── utils/                   # Utilities
│   │   ├── config.py           # Configuration management
│   │   └── logging_config.py   # Logging setup
│   └── cli.py                   # Command-line interface
├── examples/                    # Example data and outputs
├── config/                      # Configuration files
├── tests/                       # Test suite
└── requirements.txt             # Dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/thomasrocks006-cmyk/Reportanalysis).
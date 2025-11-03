"""
Report Generation Stage - Creates visually aesthetic reports from analysis results.

Generates PDF reports with charts, tables, and insights using professional templates.
"""

import logging
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

logger = logging.getLogger(__name__)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


class ReportGenerationStage:
    """
    Stage 4: Report Generation
    
    Creates professional, visually aesthetic reports from analysis results.
    """
    
    def __init__(self, config: Dict[str, Any], mcp_client=None):
        """
        Initialize the report generation stage.
        
        Args:
            config: Configuration dictionary for report generation
            mcp_client: MCP client for AI-powered report enhancements
        """
        self.config = config
        self.mcp_client = mcp_client
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info("Report generation stage initialized")
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles for the report."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT
        ))
    
    def execute(self, analysis_results: Dict[str, Any], output_path: str) -> Path:
        """
        Generate the final report.
        
        Args:
            analysis_results: Dictionary containing all analysis results
            output_path: Path where the report should be saved
            
        Returns:
            Path to the generated report
        """
        logger.info("Starting report generation")
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build report content
        story = []
        
        # Title page
        story.extend(self._create_title_page(analysis_results))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        # Data Overview
        story.extend(self._create_data_overview(analysis_results))
        story.append(PageBreak())
        
        # Statistical Analysis
        story.extend(self._create_statistical_section(analysis_results))
        story.append(PageBreak())
        
        # Visualizations
        story.extend(self._create_visualizations_section(analysis_results))
        
        # Key Findings and Recommendations
        if analysis_results.get('recommendations'):
            story.append(PageBreak())
            story.extend(self._create_recommendations_section(analysis_results))
        
        # Build PDF
        doc.build(story)
        
        logger.info(f"Report generated successfully: {output_file}")
        return output_file
    
    def _create_title_page(self, analysis_results: Dict[str, Any]) -> list:
        """Create the title page."""
        story = []
        
        # Title
        title = Paragraph(
            "Data Analysis Report",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5 * inch))
        
        # Subtitle
        subtitle = Paragraph(
            "Historical Data Analysis and Insights",
            self.styles['Heading2']
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.3 * inch))
        
        # Date
        date_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 1 * inch))
        
        # Summary table
        summary = analysis_results['synthesized_data']['summary']
        data = [
            ['Dataset Information', ''],
            ['Total Records', f"{summary['total_rows']:,}"],
            ['Total Variables', str(summary['total_columns'])],
            ['Numeric Variables', str(len(summary['numeric_summary']))],
            ['Categorical Variables', str(len(summary['categorical_summary']))]
        ]
        
        table = Table(data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        return story
    
    def _create_executive_summary(self, analysis_results: Dict[str, Any]) -> list:
        """Create executive summary section."""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Key findings
        findings = analysis_results.get('key_findings', [])
        for finding in findings:
            bullet = Paragraph(f"• {finding}", self.styles['BodyText'])
            story.append(bullet)
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Data quality metrics
        quality = analysis_results['synthesized_data']['data_quality']
        quality_text = (
            f"The dataset demonstrates <b>{quality['completeness']:.1f}%</b> completeness "
            f"with <b>{quality['missing_values']:,}</b> missing values across all variables. "
            f"<b>{quality['duplicate_rows']:,}</b> duplicate records were identified."
        )
        story.append(Paragraph(quality_text, self.styles['BodyText']))
        
        return story
    
    def _create_data_overview(self, analysis_results: Dict[str, Any]) -> list:
        """Create data overview section."""
        story = []
        
        story.append(Paragraph("Data Overview", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))
        
        summary = analysis_results['synthesized_data']['summary']
        
        # Numeric variables overview
        if summary['numeric_summary']:
            story.append(Paragraph("Numeric Variables Summary", self.styles['Heading3']))
            
            # Create table for numeric summary
            headers = [['Variable', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']]
            data = headers.copy()
            
            for var, stats in list(summary['numeric_summary'].items())[:10]:
                row = [
                    var,
                    f"{stats['mean']:.2f}",
                    f"{stats['median']:.2f}",
                    f"{stats['std']:.2f}",
                    f"{stats['min']:.2f}",
                    f"{stats['max']:.2f}"
                ]
                data.append(row)
            
            table = Table(data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(table)
        
        return story
    
    def _create_statistical_section(self, analysis_results: Dict[str, Any]) -> list:
        """Create statistical analysis section."""
        story = []
        
        story.append(Paragraph("Statistical Analysis", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Correlation analysis
        corr_analysis = analysis_results.get('correlation_analysis', {})
        strong_corr = corr_analysis.get('strong_correlations', [])
        
        if strong_corr:
            story.append(Paragraph("Strong Correlations Detected", self.styles['Heading3']))
            
            for corr in strong_corr[:5]:
                text = (
                    f"• <b>{corr['variable1']}</b> and <b>{corr['variable2']}</b>: "
                    f"{corr['correlation']:.2f} ({corr['strength']})"
                )
                story.append(Paragraph(text, self.styles['BodyText']))
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Trend analysis
        trends = analysis_results.get('trend_analysis', {}).get('temporal_trends', {})
        if trends:
            story.append(Paragraph("Trend Analysis", self.styles['Heading3']))
            
            for var, trend in trends.items():
                text = (
                    f"• <b>{var}</b>: {trend['direction']} trend "
                    f"(R² = {trend['r_squared']:.3f}, {trend['strength']} relationship)"
                )
                story.append(Paragraph(text, self.styles['BodyText']))
        
        return story
    
    def _create_visualizations_section(self, analysis_results: Dict[str, Any]) -> list:
        """Create visualizations section with charts."""
        story = []
        
        story.append(Paragraph("Data Visualizations", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Create and add charts
        data = analysis_results['synthesized_data']['raw_data']
        numeric_cols = data.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            # Distribution plot for first numeric column
            chart_buffer = self._create_distribution_chart(data, numeric_cols[0])
            if chart_buffer:
                img = Image(chart_buffer, width=5*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
        
        if len(numeric_cols) >= 2:
            # Correlation heatmap
            chart_buffer = self._create_correlation_heatmap(data)
            if chart_buffer:
                img = Image(chart_buffer, width=5*inch, height=4*inch)
                story.append(img)
        
        return story
    
    def _create_distribution_chart(self, data, column):
        """Create a distribution chart for a numeric column."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            data[column].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
            ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
            ax.set_xlabel(column, fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            
            buffer.seek(0)
            return buffer
        except Exception as e:
            logger.warning(f"Failed to create distribution chart: {str(e)}")
            return None
    
    def _create_correlation_heatmap(self, data):
        """Create a correlation heatmap."""
        try:
            numeric_data = data.select_dtypes(include=['number'])
            if numeric_data.shape[1] < 2:
                return None
            
            # Limit to first 10 numeric columns for readability
            numeric_data = numeric_data.iloc[:, :10]
            
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = numeric_data.corr()
            sns.heatmap(
                corr, 
                annot=True, 
                fmt='.2f', 
                cmap='coolwarm', 
                center=0,
                square=True,
                ax=ax,
                cbar_kws={'shrink': 0.8}
            )
            ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
            
            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            
            buffer.seek(0)
            return buffer
        except Exception as e:
            logger.warning(f"Failed to create correlation heatmap: {str(e)}")
            return None
    
    def _create_recommendations_section(self, analysis_results: Dict[str, Any]) -> list:
        """Create recommendations section."""
        story = []
        
        story.append(Paragraph("Recommendations", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))
        
        recommendations = analysis_results.get('recommendations', [])
        for rec in recommendations:
            bullet = Paragraph(f"• {rec}", self.styles['BodyText'])
            story.append(bullet)
        
        return story

"""
Analysis Stage - Performs statistical analysis and generates insights.

Uses advanced analytics and MCP for intelligent pattern recognition.
"""

import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


class AnalysisStage:
    """
    Stage 3: Data Analysis
    
    Performs statistical analysis, trend detection, and insight generation
    on the synthesized data.
    """
    
    def __init__(self, config: Dict[str, Any], mcp_client=None):
        """
        Initialize the analysis stage.
        
        Args:
            config: Configuration dictionary for analysis
            mcp_client: MCP client for AI-powered analysis
        """
        self.config = config
        self.mcp_client = mcp_client
        logger.info("Analysis stage initialized")
    
    def execute(self, synthesized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the synthesized data and generate insights.
        
        Args:
            synthesized_data: Dictionary containing synthesized data
            
        Returns:
            Dictionary containing analysis results and insights
        """
        logger.info("Starting data analysis")
        
        data = synthesized_data['raw_data']
        
        analysis_results = {
            'synthesized_data': synthesized_data,
            'statistical_analysis': self._statistical_analysis(data),
            'trend_analysis': self._trend_analysis(data),
            'correlation_analysis': self._correlation_analysis(data),
            'outlier_detection': self._detect_outliers(data),
            'key_findings': self._generate_key_findings(data, synthesized_data),
            'recommendations': []
        }
        
        # Use MCP for advanced insights if available
        if self.mcp_client and self.mcp_client.is_connected():
            analysis_results['ai_analysis'] = self._ai_powered_analysis(
                data, 
                synthesized_data
            )
            analysis_results['recommendations'] = self._generate_recommendations(
                analysis_results
            )
        
        logger.info("Data analysis completed")
        return analysis_results
    
    def _statistical_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        analysis = {
            'descriptive_stats': {},
            'distributions': {}
        }
        
        for col in numeric_cols:
            col_data = data[col].dropna()
            
            analysis['descriptive_stats'][col] = {
                'count': int(len(col_data)),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'mode': float(col_data.mode()[0]) if len(col_data.mode()) > 0 else None,
                'std': float(col_data.std()),
                'variance': float(col_data.var()),
                'skewness': float(stats.skew(col_data)),
                'kurtosis': float(stats.kurtosis(col_data)),
                'quartiles': {
                    'q1': float(col_data.quantile(0.25)),
                    'q2': float(col_data.quantile(0.50)),
                    'q3': float(col_data.quantile(0.75))
                }
            }
        
        return analysis
    
    def _trend_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze trends in the data."""
        trends = {
            'temporal_trends': {},
            'growth_rates': {}
        }
        
        # Detect date columns for temporal analysis
        date_columns = data.select_dtypes(include=['datetime64']).columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(date_columns) > 0 and len(numeric_cols) > 0:
            date_col = date_columns[0]
            
            for num_col in numeric_cols[:3]:  # Analyze first 3 numeric columns
                # Sort by date and calculate trend
                sorted_data = data.sort_values(date_col)
                values = sorted_data[num_col].dropna()
                
                if len(values) > 1:
                    # Simple linear trend
                    x = np.arange(len(values))
                    slope, intercept, r_value, _, _ = stats.linregress(x, values)
                    
                    trends['temporal_trends'][num_col] = {
                        'slope': float(slope),
                        'direction': 'increasing' if slope > 0 else 'decreasing',
                        'r_squared': float(r_value ** 2),
                        'strength': 'strong' if abs(r_value) > 0.7 else 'moderate' if abs(r_value) > 0.4 else 'weak'
                    }
        
        return trends
    
    def _correlation_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between numeric variables."""
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            return {'correlations': {}, 'strong_correlations': []}
        
        corr_matrix = numeric_data.corr()
        
        # Find strong correlations (excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'variable1': corr_matrix.columns[i],
                        'variable2': corr_matrix.columns[j],
                        'correlation': float(corr_value),
                        'strength': 'strong positive' if corr_value > 0 else 'strong negative'
                    })
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }
    
    def _detect_outliers(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers in numeric columns using IQR method."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        outliers = {}
        for col in numeric_cols:
            col_data = data[col].dropna()
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outlier_count = ((col_data < lower_bound) | (col_data > upper_bound)).sum()
            
            outliers[col] = {
                'count': int(outlier_count),
                'percentage': float(outlier_count / len(col_data) * 100),
                'bounds': {
                    'lower': float(lower_bound),
                    'upper': float(upper_bound)
                }
            }
        
        return outliers
    
    def _generate_key_findings(
        self, 
        data: pd.DataFrame, 
        synthesized_data: Dict[str, Any]
    ) -> List[str]:
        """Generate key findings from the analysis."""
        findings = []
        
        summary = synthesized_data['summary']
        
        # Data size finding
        findings.append(
            f"Dataset contains {summary['total_rows']:,} records "
            f"across {summary['total_columns']} variables"
        )
        
        # Data quality finding
        quality = synthesized_data['data_quality']
        findings.append(
            f"Data completeness: {quality['completeness']:.1f}% "
            f"({quality['missing_values']:,} missing values)"
        )
        
        # Numeric insights
        if summary['numeric_summary']:
            findings.append(
                f"Analysis includes {len(summary['numeric_summary'])} "
                f"numeric variables and {len(summary['categorical_summary'])} "
                f"categorical variables"
            )
        
        return findings
    
    def _ai_powered_analysis(
        self, 
        data: pd.DataFrame, 
        synthesized_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use MCP for advanced AI-powered analysis."""
        try:
            analysis = self.mcp_client.analyze_data({
                'summary': synthesized_data['summary'],
                'sample': data.head(50).to_dict()
            })
            return analysis
        except Exception as e:
            logger.warning(f"Failed to perform AI analysis: {str(e)}")
            return {}
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Based on data quality
        quality = analysis_results['synthesized_data']['data_quality']
        if quality['completeness'] < 90:
            recommendations.append(
                "Consider addressing missing data to improve analysis accuracy"
            )
        
        # Based on outliers
        outliers = analysis_results['outlier_detection']
        high_outlier_cols = [
            col for col, info in outliers.items() 
            if info['percentage'] > 5
        ]
        if high_outlier_cols:
            recommendations.append(
                f"Review outliers in: {', '.join(high_outlier_cols[:3])}"
            )
        
        return recommendations

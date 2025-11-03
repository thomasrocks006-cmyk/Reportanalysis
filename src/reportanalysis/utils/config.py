"""
Configuration management utilities.

Handles loading and validation of configuration files.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        'data': {
            'min_rows': 1,
            'csv_encoding': 'utf-8',
            'excel_sheet': 0,
            'json_orient': 'records'
        },
        'synthesis': {
            'enable_ai_insights': True
        },
        'analysis': {
            'correlation_threshold': 0.7,
            'outlier_method': 'iqr',
            'trend_analysis': True
        },
        'report': {
            'page_size': 'letter',
            'include_visualizations': True,
            'max_charts': 10
        },
        'mcp': {
            'enabled': False,
            'server_url': '',
            'timeout': 30
        }
    }
    
    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Args:
            config_path: Optional path to configuration file
            
        Returns:
            Configuration dictionary
        """
        config = cls.DEFAULT_CONFIG.copy()
        
        if config_path:
            config_file = Path(config_path)
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        user_config = yaml.safe_load(f)
                    
                    # Merge with defaults
                    config = cls._merge_configs(config, user_config)
                    logger.info(f"Loaded configuration from {config_path}")
                    
                except Exception as e:
                    logger.warning(f"Failed to load config file: {str(e)}, using defaults")
            else:
                logger.warning(f"Config file not found: {config_path}, using defaults")
        
        return config
    
    @classmethod
    def _merge_configs(
        cls, 
        default: Dict[str, Any], 
        user: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursively merge user configuration with defaults.
        
        Args:
            default: Default configuration
            user: User-provided configuration
            
        Returns:
            Merged configuration
        """
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = cls._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    @classmethod
    def save_config(cls, config: Dict[str, Any], config_path: str):
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
            config_path: Path where to save the configuration
        """
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}")
            raise

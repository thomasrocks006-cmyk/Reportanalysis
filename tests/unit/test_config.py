"""
Tests for configuration management.
"""

import pytest
import tempfile
from pathlib import Path

from reportanalysis.utils.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        config = ConfigManager.load_config()
        
        assert isinstance(config, dict)
        assert 'data' in config
        assert 'synthesis' in config
        assert 'analysis' in config
        assert 'report' in config
        assert 'mcp' in config
    
    def test_load_from_file(self):
        """Test loading configuration from file."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("data:\n  min_rows: 100\n")
            temp_path = f.name
        
        try:
            config = ConfigManager.load_config(temp_path)
            
            assert config['data']['min_rows'] == 100
            # Default values should still be present
            assert 'synthesis' in config
        finally:
            Path(temp_path).unlink()
    
    def test_save_config(self):
        """Test saving configuration to file."""
        config = {'test': 'value'}
        
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            ConfigManager.save_config(config, temp_path)
            
            # Verify file was created
            assert Path(temp_path).exists()
            
            # Load and verify content
            loaded = ConfigManager.load_config(temp_path)
            assert 'test' in loaded
        finally:
            Path(temp_path).unlink()
    
    def test_merge_configs(self):
        """Test configuration merging."""
        default = {
            'section1': {'key1': 'value1', 'key2': 'value2'},
            'section2': {'key3': 'value3'}
        }
        
        user = {
            'section1': {'key1': 'new_value'},
            'section3': {'key4': 'value4'}
        }
        
        merged = ConfigManager._merge_configs(default, user)
        
        assert merged['section1']['key1'] == 'new_value'
        assert merged['section1']['key2'] == 'value2'
        assert merged['section2']['key3'] == 'value3'
        assert merged['section3']['key4'] == 'value4'

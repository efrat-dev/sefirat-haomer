# config.py
import os
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Union
from pathlib import Path
from enum import Enum


class OutputFormat(Enum):
    """Output format options"""
    HEBREW = "hebrew"
    TRANSLITERATED = "transliterated"
    BOTH = "both"
    ENGLISH = "english"


class DateFormat(Enum):
    """Date format options"""
    HEBREW_ONLY = "hebrew_only"
    GREGORIAN_ONLY = "gregorian_only"
    BOTH = "both"
    ISO = "iso"


@dataclass
class OmerConfig:
    """Configuration class for Omer package"""
    # Text output options
    include_transliteration: bool = False
    include_english_translation: bool = False
    output_format: OutputFormat = OutputFormat.HEBREW
    
    # Date options
    include_gregorian_dates: bool = False
    date_format: DateFormat = DateFormat.HEBREW_ONLY
    gregorian_format: str = "%Y-%m-%d"  # Default ISO format
    
    # Display options
    show_week_info: bool = True
    show_day_count: bool = True
    show_remaining_days: bool = False
    compact_output: bool = False
    
    # Validation options
    strict_validation: bool = True
    allow_future_dates: bool = True
    
    # Localization
    locale: str = "he_IL"  # Hebrew Israel
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if isinstance(self.output_format, str):
            self.output_format = OutputFormat(self.output_format)
        if isinstance(self.date_format, str):
            self.date_format = DateFormat(self.date_format)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        config_dict = asdict(self)
        # Convert enums to their values
        config_dict['output_format'] = self.output_format.value
        config_dict['date_format'] = self.date_format.value
        return config_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OmerConfig':
        """Create config from dictionary"""
        return cls(**data)
    
    def save_to_file(self, filepath: Union[str, Path]) -> None:
        """Save configuration to JSON file"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: Union[str, Path]) -> 'OmerConfig':
        """Load configuration from JSON file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)


class ConfigManager:
    """Configuration manager for the Omer package"""
    
    DEFAULT_CONFIG_DIR = Path.home() / ".sfirat_haomer"
    DEFAULT_CONFIG_FILE = "config.json"
    
    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        self.config_dir = Path(config_dir) if config_dir else self.DEFAULT_CONFIG_DIR
        self.config_file = self.config_dir / self.DEFAULT_CONFIG_FILE
        self._config: Optional[OmerConfig] = None
    
    @property
    def config(self) -> OmerConfig:
        """Get current configuration"""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def load_config(self) -> OmerConfig:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                return OmerConfig.load_from_file(self.config_file)
            except Exception as e:
                print(f"Error loading config: {e}. Using default configuration.")
                return OmerConfig()
        else:
            return OmerConfig()
    
    def save_config(self, config: Optional[OmerConfig] = None) -> None:
        """Save configuration to file"""
        if config is None:
            config = self._config or OmerConfig()
        
        config.save_to_file(self.config_file)
        self._config = config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration with new values"""
        current_config = self.config
        config_dict = current_config.to_dict()
        config_dict.update(kwargs)
        
        self._config = OmerConfig.from_dict(config_dict)
        self.save_config()
    
    def reset_config(self) -> None:
        """Reset configuration to default values"""
        self._config = OmerConfig()
        self.save_config()
    
    def get_config_path(self) -> Path:
        """Get path to configuration file"""
        return self.config_file


# Global configuration manager instance
_config_manager = ConfigManager()


def get_config() -> OmerConfig:
    """Get current global configuration"""
    return _config_manager.config


def set_config(config: OmerConfig) -> None:
    """Set global configuration"""
    _config_manager.save_config(config)


def update_config(**kwargs) -> None:
    """Update global configuration"""
    _config_manager.update_config(**kwargs)


def reset_config() -> None:
    """Reset global configuration to defaults"""
    _config_manager.reset_config()


def configure_output_format(format_type: Union[str, OutputFormat]) -> None:
    """Configure output format"""
    if isinstance(format_type, str):
        format_type = OutputFormat(format_type)
    update_config(output_format=format_type)


def configure_dates(
    include_gregorian: bool = False,
    date_format: Union[str, DateFormat] = DateFormat.HEBREW_ONLY,
    gregorian_format: str = "%Y-%m-%d"
) -> None:
    """Configure date display options"""
    if isinstance(date_format, str):
        date_format = DateFormat(date_format)
    
    update_config(
        include_gregorian_dates=include_gregorian,
        date_format=date_format,
        gregorian_format=gregorian_format
    )


def configure_display(
    show_week_info: bool = True,
    show_day_count: bool = True,
    show_remaining_days: bool = False,
    compact_output: bool = False
) -> None:
    """Configure display options"""
    update_config(
        show_week_info=show_week_info,
        show_day_count=show_day_count,
        show_remaining_days=show_remaining_days,
        compact_output=compact_output
    )


# Environment variable support
def load_config_from_env() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    config_dict = {}
    
    # Map environment variables to config keys
    env_mapping = {
        'OMER_OUTPUT_FORMAT': 'output_format',
        'OMER_INCLUDE_TRANSLITERATION': 'include_transliteration',
        'OMER_INCLUDE_ENGLISH': 'include_english_translation',
        'OMER_INCLUDE_GREGORIAN': 'include_gregorian_dates',
        'OMER_DATE_FORMAT': 'date_format',
        'OMER_SHOW_WEEK_INFO': 'show_week_info',
        'OMER_COMPACT_OUTPUT': 'compact_output',
        'OMER_LOCALE': 'locale'
    }
    
    for env_var, config_key in env_mapping.items():
        value = os.getenv(env_var)
        if value is not None:
            # Convert string values to appropriate types
            if config_key in ['include_transliteration', 'include_english_translation', 
                             'include_gregorian_dates', 'show_week_info', 'compact_output']:
                config_dict[config_key] = value.lower() in ('true', '1', 'yes', 'on')
            else:
                config_dict[config_key] = value
    
    return config_dict


def apply_env_config() -> None:
    """Apply configuration from environment variables"""
    env_config = load_config_from_env()
    if env_config:
        update_config(**env_config)


# Auto-apply environment configuration on import
apply_env_config()
# Detailed Usage Guide

## Installation Requirements

### Python Version

- Python 3.7 or higher
- pip (Python package manager)

### Network Requirements

- SSH access to Cisco devices
- Valid credentials with appropriate privilege levels
- Network connectivity to target devices

## Configuration

### Basic Configuration

1. Copy `config_example.py` to `config.py`
2. Edit `config.py` with your preferred settings:

```python
# Customize diagnostic commands
DIAGNOSTIC_COMMANDS = [
    'show version',
    'show ip interface brief',
    # Add your commands here
]

"""
Configuration example for Cisco Troubleshooting Toolkit
Copy this file to config.py and update with your settings
"""

# Device connection settings
DEFAULT_DEVICE_TYPE = 'cisco_ios'
DEFAULT_TIMEOUT = 30
DEFAULT_PORT = 22

# Diagnostic commands to run
DIAGNOSTIC_COMMANDS = [
    'show version',
    'show ip interface brief',
    'show interfaces status',
    'show logging | last 50',
    'show processes cpu | exclude 0.00%__0.00%__0.00%',
    'show memory statistics',
    'show environment all',
    'show inventory',
]

# Report settings
REPORT_FORMAT = 'text'  # Options: 'text', 'json'
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Example device list (for bulk operations)
DEVICES = [
    {
        'ip': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
        'device_type': 'cisco_ios'
    },
    # Add more devices as needed
]
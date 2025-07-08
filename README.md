# Cisco Troubleshooting Toolkit

A Python-based automation tool for rapid Cisco device diagnostics and troubleshooting.

## Features

- ✅ Automated health checks for Cisco routers and switches
- ✅ Standardized diagnostic command execution
- ✅ Exportable reports for documentation
- ✅ Multi-device support
- ✅ Customizable command sets

## Prerequisites

- Python 3.7+
- Network access to Cisco devices
- Device credentials with appropriate permissions
  
### ⚠️ Python 3.13+ Compatibility Note

Python 3.13 removed the `telnetlib` module from the standard library. This toolkit includes a compatibility fix, but you must install the requirements:

```bash
pip install -r requirements.txt

## Installation

1. Clone the repository:

```bash

git clone https://github.com/xBinaryCodex/cisco-troubleshooting-toolkit.git
cd cisco-troubleshooting-toolkit

```

1. Install required packages:

```bash

pip install -r requirements.txt

```

1. Copy and configure the example config:

``` bash

cp config_example.py config.py
# Edit config.py with your device information

```

## Quick Start

```python
from cisco_troubleshooter import CiscoTroubleshooter

# Initialize the troubleshooter
ts = CiscoTroubleshooter('192.168.1.1', 'username', 'password')

# Run basic diagnostics
results = ts.run_diagnostics()

# Generate report
ts.generate_report(results, 'device_report.txt')
```

## Usage Examples

### Basic Health Check

```python
# Check single device
ts = CiscoTroubleshooter('10.0.0.1', 'admin', 'password')
health = ts.check_health()
print(health)

# Multiple Device Scan

devices = [
    {'ip': '10.0.0.1', 'username': 'admin', 'password': 'pass'},
    {'ip': '10.0.0.2', 'username': 'admin', 'password': 'pass'}
]

for device in devices:
    ts = CiscoTroubleshooter(**device)
    results = ts.run_diagnostics()
    ts.save_results(f"report_{device['ip']}.txt")
```

## Supported Commands

The tool runs the following diagnostic commands by default:

show version
show ip interface brief
show interfaces status
show logging
show processes cpu
show memory statistics

You can customize the command set in config.py.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Use Cases

NOC/SOC daily health checks
Troubleshooting automation
Pre/Post maintenance verification
Documentation generation
Compliance auditing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

### Jose Diaz

GitHub: @xBinaryCodex
LinkedIn: Jose Diaz

## Acknowledgments

Thanks to the Switchovr community for feedback and testing
Built with Netmiko for device connectivity

## Disclaimer

This tool is provided as-is. Always test in a lab environment before using in production. The author is not responsible for any network outages or misconfigurations.

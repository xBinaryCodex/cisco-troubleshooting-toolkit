#!/usr/bin/env python3
"""
Example usage of the Cisco Troubleshooting Toolkit
"""

from cisco_troubleshooter import CiscoTroubleshooter

# Example 1: Basic health check
def basic_health_check():
    """Run a basic health check on a single device"""
    ts = CiscoTroubleshooter('192.168.1.1', 'admin', 'password')
    
    if ts.connect():
        health = ts.check_health()
        print(f"Device Status: {health['status']}")
        print("Issues found:")
        for issue in health['issues']:
            print(f"  - {issue}")
        ts.disconnect()


# Example 2: Custom diagnostics
def custom_diagnostics():
    """Run custom diagnostic commands"""
    ts = CiscoTroubleshooter('192.168.1.1', 'admin', 'password')
    
    custom_commands = [
        'show version',
        'show running-config | include hostname',
        'show ip route summary',
        'show cdp neighbors'
    ]
    
    if ts.connect():
        results = ts.run_diagnostics(custom_commands)
        ts.generate_report(results, 'custom_report.txt')
        ts.disconnect()


# Example 3: Multiple devices
def multiple_devices():
    """Check multiple devices and generate individual reports"""
    devices = [
        {'ip': '192.168.1.1', 'username': 'admin', 'password': 'pass1'},
        {'ip': '192.168.1.2', 'username': 'admin', 'password': 'pass2'},
        {'ip': '192.168.1.3', 'username': 'admin', 'password': 'pass3'},
    ]
    
    for device in devices:
        print(f"\nChecking device: {device['ip']}")
        ts = CiscoTroubleshooter(**device)
        
        if ts.connect():
            # Run diagnostics
            results = ts.run_diagnostics()
            
            # Save report with device-specific name
            report_name = f"report_{device['ip'].replace('.', '_')}.txt"
            ts.generate_report(results, report_name)
            
            ts.disconnect()
        else:
            print(f"Skipping {device['ip']} - connection failed")


if __name__ == "__main__":
    # Uncomment the example you want to run
    # basic_health_check()
    # custom_diagnostics()
    # multiple_devices()
    pass
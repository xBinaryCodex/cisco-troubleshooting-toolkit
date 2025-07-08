#!/usr/bin/env python3
"""
Cisco Troubleshooting Toolkit
Author: Jose Diaz
Description: Automated diagnostics and troubleshooting for Cisco devices
"""

import sys
import json
import datetime
from typing import Dict, List, Optional
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Default configuration (used if config.py doesn't exist)
DEFAULT_DEVICE_TYPE = 'cisco_ios'
DEFAULT_TIMEOUT = 30
DEFAULT_PORT = 22
DIAGNOSTIC_COMMANDS = [
    'show version',
    'show ip interface brief',
    'show interfaces status',
    'show logging | last 50',
    'show processes cpu | exclude 0.00%__0.00%__0.00%',
    'show memory statistics',
]
REPORT_FORMAT = 'text'
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Import configuration
# Import configuration
try:
    from config import (
        DEFAULT_DEVICE_TYPE, DEFAULT_TIMEOUT, DEFAULT_PORT,
        DIAGNOSTIC_COMMANDS, REPORT_FORMAT, TIMESTAMP_FORMAT
    )
except ImportError:
    print("Error: config.py not found. Please copy config_example.py to config.py")
    sys.exit(1)
except AttributeError:
    print("Error: config.py is empty or missing required settings.")
    print("Please copy the contents of config_example.py to config.py and update with your settings.")
    sys.exit(1)


class CiscoTroubleshooter:
    """Main class for Cisco device troubleshooting and diagnostics"""
    
    def __init__(self, ip: str, username: str, password: str, 
                 device_type: str = DEFAULT_DEVICE_TYPE,
                 port: int = DEFAULT_PORT):
        """
        Initialize the troubleshooter with device credentials
        
        Args:
            ip: Device IP address
            username: Login username
            password: Login password
            device_type: Netmiko device type (default: cisco_ios)
            port: SSH port (default: 22)
        """
        self.device = {
            'device_type': device_type,
            'ip': ip,
            'username': username,
            'password': password,
            'port': port,
            'timeout': DEFAULT_TIMEOUT,
        }
        self.connection = None
        self.hostname = None
        
    def connect(self) -> bool:
        """
        Establish connection to the device
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            print(f"Connecting to {self.device['ip']}...")
            self.connection = ConnectHandler(**self.device)
            self.hostname = self.connection.find_prompt()[:-1]
            print(f"Successfully connected to {self.hostname}")
            return True
        except NetmikoAuthenticationException:
            print(f"Authentication failed for {self.device['ip']}")
            return False
        except NetmikoTimeoutException:
            print(f"Connection timeout for {self.device['ip']}")
            return False
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Safely disconnect from the device"""
        if self.connection:
            self.connection.disconnect()
            print(f"Disconnected from {self.hostname}")
    
    def run_command(self, command: str) -> str:
        """
        Execute a single command on the device
        
        Args:
            command: Command to execute
            
        Returns:
            str: Command output
        """
        if not self.connection:
            return "Error: Not connected to device"
        
        try:
            output = self.connection.send_command(command)
            return output
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def run_diagnostics(self, commands: List[str] = None) -> Dict[str, str]:
        """
        Run diagnostic commands on the device
        
        Args:
            commands: List of commands to run (uses default if None)
            
        Returns:
            dict: Command outputs keyed by command
        """
        if not self.connection:
            if not self.connect():
                return {"error": "Failed to connect to device"}
        
        commands = commands or DIAGNOSTIC_COMMANDS
        results = {
            'device': self.device['ip'],
            'hostname': self.hostname,
            'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
            'diagnostics': {}
        }
        
        print(f"\nRunning diagnostics on {self.hostname}...")
        for cmd in commands:
            print(f"  Executing: {cmd}")
            output = self.run_command(cmd)
            results['diagnostics'][cmd] = output
            
        return results
    
    def check_health(self) -> Dict[str, any]:
        """
        Perform quick health check on the device
        
        Returns:
            dict: Health status indicators
        """
        if not self.connection:
            if not self.connect():
                return {"error": "Failed to connect to device"}
        
        health = {
            'device': self.device['ip'],
            'hostname': self.hostname,
            'status': 'healthy',
            'issues': []
        }
        
        # Check CPU usage
        cpu_output = self.run_command('show processes cpu | include CPU')
        if "Error" not in cpu_output:
            # Parse CPU usage (this is simplified - adjust based on actual output)
            lines = cpu_output.strip().split('\n')
            for line in lines:
                if 'five minutes:' in line:
                    cpu_5min = int(line.split('five minutes:')[1].split('%')[0])
                    if cpu_5min > 80:
                        health['issues'].append(f"High CPU usage: {cpu_5min}%")
                        health['status'] = 'warning'
        
        # Check memory
        mem_output = self.run_command('show memory statistics | include Processor')
        if "Error" not in mem_output and "Free" in mem_output:
            # Parse memory (simplified)
            if int(mem_output.split()[-1]) < 10000000:  # Less than 10MB free
                health['issues'].append("Low memory")
                health['status'] = 'warning'
        
        # Check interfaces
        int_output = self.run_command('show ip interface brief | include down')
        if "Error" not in int_output and int_output.strip():
            down_count = len(int_output.strip().split('\n'))
            if down_count > 0:
                health['issues'].append(f"{down_count} interfaces down")
        
        if not health['issues']:
            health['issues'].append("No issues detected")
            
        return health
    
    def generate_report(self, results: Dict, filename: str = None):
        """
        Generate a report from diagnostic results
        
        Args:
            results: Diagnostic results dictionary
            filename: Output filename (auto-generated if None)
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            hostname = results.get('hostname', 'unknown')
            filename = f"cisco_report_{hostname}_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write(f"Cisco Diagnostic Report\n")
                f.write(f"Device: {results.get('device', 'Unknown')}\n")
                f.write(f"Hostname: {results.get('hostname', 'Unknown')}\n")
                f.write(f"Generated: {results.get('timestamp', 'Unknown')}\n")
                f.write("=" * 80 + "\n\n")
                
                # Diagnostic outputs
                diagnostics = results.get('diagnostics', {})
                for cmd, output in diagnostics.items():
                    f.write(f"\n{'#' * 60}\n")
                    f.write(f"# Command: {cmd}\n")
                    f.write(f"{'#' * 60}\n\n")
                    f.write(output)
                    f.write("\n\n")
                    
            print(f"Report saved to: {filename}")
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")
    
    def save_json(self, results: Dict, filename: str = None):
        """
        Save results as JSON for programmatic use
        
        Args:
            results: Diagnostic results
            filename: Output filename
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            hostname = results.get('hostname', 'unknown')
            filename = f"cisco_report_{hostname}_{timestamp}.json"
            
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"JSON report saved to: {filename}")
        except Exception as e:
            print(f"Error saving JSON: {str(e)}")


def main():
    """Example usage of the troubleshooter"""
    # This is just an example - real credentials should come from config or args
    print("Cisco Troubleshooting Toolkit")
    print("-" * 30)
    
    # Example usage (replace with actual device info)
    ip = input("Enter device IP: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Create troubleshooter instance
    ts = CiscoTroubleshooter(ip, username, password)
    
    # Connect to device
    if ts.connect():
        # Run diagnostics
        results = ts.run_diagnostics()
        
        # Generate report
        ts.generate_report(results)
        
        # Also save as JSON
        ts.save_json(results)
        
        # Quick health check
        health = ts.check_health()
        print(f"\nHealth Status: {health['status']}")
        for issue in health['issues']:
            print(f"  - {issue}")
        
        # Disconnect
        ts.disconnect()
    else:
        print("Failed to establish connection")


if __name__ == "__main__":
    main()
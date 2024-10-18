import shutil
import subprocess
import logging

REQUIRED_TOOLS = ["airmon-ng", "airodump-ng", "aircrack-ng", "reaver", "nmap", "bully"]

def check_tools_installed():
    """Check if all required tools are installed."""
    missing_tools = [tool for tool in REQUIRED_TOOLS if not shutil.which(tool)]
    
    if missing_tools:
        return f"The following tools are missing: {', '.join(missing_tools)}. Please install them."
    return "All required tools are installed."

def enable_monitor_mode(interface):
    """Enable monitor mode on the given interface."""
    logging.info(f"Enabling monitor mode on interface: {interface}")
    result = run_command(f"sudo airmon-ng start {interface}")
    logging.info(result)
    return f"{interface}mon"

def disable_monitor_mode(interface):
    """Disable monitor mode on the given interface."""
    logging.info(f"Disabling monitor mode on interface: {interface}")
    result = run_command(f"sudo airmon-ng stop {interface}")
    logging.info(result)

def run_command(command):
    try:
        logging.info(f"Running command: {command}")
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.decode('utf-8')
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return "Operation cancelled"
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with error: {e.stderr.decode('utf-8')}")
        return f"Command failed: {e.stderr.decode('utf-8')}"

def scan_networks(interface):
    """Scan for available networks using airodump-ng."""
    logging.info(f"Scanning networks on interface: {interface}")
    result = run_command(f"sudo airodump-ng {interface}mon")
    logging.info(result)
    return result
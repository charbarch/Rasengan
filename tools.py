
import shutil
import subprocess

REQUIRED_TOOLS = ["airmon-ng", "airodump-ng", "aircrack-ng", "reaver", "nmap"]

def check_tools_installed():
    """Check if all required tools are installed."""
    missing_tools = []
    for tool in REQUIRED_TOOLS:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        return f"The following tools are missing: {', '.join(missing_tools)}. Please install them."
    return "All required tools are installed."

def run_command(command):
    """Function to run system commands and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode()}"

def enable_monitor_mode(interface):
    return run_command(f"sudo airmon-ng start {interface}")

def disable_monitor_mode(interface):
    return run_command(f"sudo airmon-ng stop {interface}mon")

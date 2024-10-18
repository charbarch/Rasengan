import shutil
import subprocess

REQUIRED_TOOLS = ["airmon-ng", "airodump-ng", "aircrack-ng", "reaver", "nmap"]

def check_tools_installed():
    """Check if all required tools are installed."""
    missing_tools = [tool for tool in REQUIRED_TOOLS if not shutil.which(tool)]
    
    if missing_tools:
        return f"The following tools are missing: {', '.join(missing_tools)}. Please install them."
    return "All required tools are installed."

def run_command(command):
    """Run a system command and return its output or an error message."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}': {e.stderr.strip()}"

def enable_monitor_mode(interface):
    """Enable monitor mode on a given network interface."""
    return run_command(f"sudo airmon-ng start {interface}")

def disable_monitor_mode(interface):
    """Disable monitor mode on a given network interface."""
    return run_command(f"sudo airmon-ng stop {interface}mon")

if __name__ == "__main__":
    # Example usage
    tools_status = check_tools_installed()
    print(tools_status)
    
    if "All required tools are installed" in tools_status:
        interface = "wlan0"  # Replace with your actual interface name
        print(enable_monitor_mode(interface))
        print(disable_monitor_mode(interface))

# Rasengan: Wi-Fi Security Checker

Rasengan is a CLI tool designed for automating Wi-Fi security checks, such as network scanning, WPA handshake capture, WPA password cracking, WPS attacks, and port scanning on routers.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/charbarch/rasengan.git
   ```

2. Navigate into the project directory:

   ```bash
   cd rasengan
   ```

3. Ensure all required tools are installed:

   ```bash
   sudo apt install aircrack-ng reaver nmap
   ```

4. Run the tool:

   ```bash
   python3 rasengan.py
   ```

## Requirements

Make sure the following tools are installed on your system:

- `airmon-ng`
- `airodump-ng`
- `aircrack-ng`
- `reaver`
- `nmap`

Rasengan will check for these tools when it starts and notify you if any are missing.

## Features

- **Network Scanning**: Scan for nearby Wi-Fi networks using `airodump-ng`.
- **WPA Handshake Capture**: Capture WPA/WPA2 handshakes for password cracking.
- **WPA Password Cracking**: Use a wordlist to attempt cracking the captured handshake with `aircrack-ng`.
- **WPS Attack**: Attempt to exploit WPS vulnerabilities using `Reaver`.
- **Port Scanning**: Scan a router for open ports using `nmap`.
- **Monitor Mode Management**: Automatically enable and disable monitor mode on your Wi-Fi adapter.

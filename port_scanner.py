#!/usr/bin/env python3

"""
Simple TCP Port Scanner

This program checks whether specified TCP ports are open or closed
on a target host.

For educational use only. Scan systems you own or have permission
to test. scanme.nmap.org is provided by the Nmap project for testing.
"""

import socket
import sys
import time
from datetime import datetime

# ---------------------------------------------------------
# Check one port
# ---------------------------------------------------------
def scan_port(host, port, timeout=1.0):
	"""
	Attempt to connect to one TCP port.

	Returns:
		True  - if the port is open
		False - if the port is closed or unavailable
	"""

	try:
		# Create an IPv4 TCP socket.
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

			# Prevent the program from waiting too long.
			sock.settimeout(timeout)

			# Attempt to connect to the specified host and port.
			result = sock.connect_ex((host, port))

			# A result of 0 means the connection succeeded.
			return result == 0

	except socket.gaierror:
		print(f"ERROR: Could not resolve host '{host}'.")
		return False

	except socket.timeout:
		return False

	except OSError:
		return False


# ---------------------------------------------------------
# Validate port number
# ---------------------------------------------------------
def validate_port(port):
	"""Check that a port is between 1 and 65535."""

	if not isinstance(port, int):
		return False

	return 1 <= port <= 65535


# ---------------------------------------------------------
# Scan a range of ports
# ---------------------------------------------------------
def scan_range(host, start_port, end_port):
	"""Scan all ports between start_port and end_port."""

	if not validate_port(start_port) or not validate_port(end_port):
		print("ERROR: Port numbers must be between 1 and 65535.")
		return

	if start_port > end_port:
		print("ERROR: Starting port cannot be greater than ending port.")
		return

	print("\n========================================")
	print("TCP PORT SCANNER")
	print("========================================")
	print(f"Target: {host}")
	print(f"Port range: {start_port}-{end_port}")
	print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	print("----------------------------------------")

	# Make sure the hostname can be resolved before scanning.
	try:
		ip_address = socket.gethostbyname(host)
		print(f"IP address: {ip_address}")
	except socket.gaierror:
		print(f"ERROR: Unable to resolve host '{host}'.")
		return

	print("----------------------------------------")

	start_time = time.perf_counter()

	open_ports = []
	closed_ports = []

	# Test every port in the requested range.
	for port in range(start_port, end_port + 1):

		if scan_port(host, port):
			print(f"Port {port:5} - OPEN")
			open_ports.append(port)
		else:
			print(f"Port {port:5} - CLOSED")
			closed_ports.append(port)

	end_time = time.perf_counter()

	elapsed_time = end_time - start_time

	print("----------------------------------------")
	print("Scan complete.")
	print(f"Open ports: {len(open_ports)}")
	print(f"Closed ports: {len(closed_ports)}")
	print(f"Time elapsed: {elapsed_time:.2f} seconds")
	print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	print("========================================")


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------
def main():
	"""Process command-line arguments and start the scan."""

	# The program expects three arguments:
	# host, starting port, and ending port.
	if len(sys.argv) != 4:
		print("Usage:")
		print("python port_scanner.py <host> <start_port> <end_port>")
		print()
		print("Example:")
		print("python port_scanner.py 127.0.0.1 20 100")
		sys.exit(1)

	host = sys.argv[1]

	# Convert port arguments from text to integers.
	try:
		start_port = int(sys.argv[2])
		end_port = int(sys.argv[3])

	except ValueError:
		print("ERROR: Port numbers must be integers.")
		sys.exit(1)

	# Check port ranges before starting.
	if not validate_port(start_port) or not validate_port(end_port):
		print("ERROR: Ports must be between 1 and 65535.")
		sys.exit(1)

	if start_port > end_port:
		print("ERROR: Starting port cannot be greater than ending port.")
		sys.exit(1)

	# Start the scan.
	scan_range(host, start_port, end_port)


if __name__ == "__main__":
	main()

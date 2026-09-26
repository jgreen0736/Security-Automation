#!/usr/bin/env python3

"""
Simple TCP Server

This program creates a server that waits for a client to connect.
After connecting, the server receives a message and sends a response.
"""

import socket

# Server configuration
HOST = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 1024


def main():
	"""Start the server and handle a client connection."""

	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
			server_socket.setsockopt(
				socket.SOL_SOCKET,
				socket.SO_REUSEADDR,
				1
			)
			server_socket.bind((HOST, PORT))
			server_socket.listen(1)

			print(f"Server is listening on {HOST}:{PORT}")
			print("Waiting for a client to connect...")

			client_socket, client_address = server_socket.accept()

			with client_socket:
				print(f"Client connected from {client_address}")

				data = client_socket.recv(BUFFER_SIZE)

				if data:
					message = data.decode("utf-8")
					print(f"Message received from client: {message}")

					response = f"Server received your message: {message}"
					client_socket.sendall(response.encode("utf-8"))
					print("Response sent to client.")

				print("Client disconnected.")
				print("Server shutting down.")

	except OSError as error:
		print(f"Socket error: {error}")

	except KeyboardInterrupt:
		print("\nServer stopped by user.")


if __name__ == "__main__":
	main()

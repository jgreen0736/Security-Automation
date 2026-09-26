

import socket

# Client configuration
HOST = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 1024

def main():
    """Start the client and send a message to the server."""
    try:
        # Create an IPv4 TCP socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server.
            client_socket.connect((HOST, PORT))

            # Send a message to the server.
            message = "Hello, Server!"
            client_socket.sendall(message.encode("utf-8"))

            # Receive a response from the server.
            data = client_socket.recv(BUFFER_SIZE)
            response = data.decode("utf-8")
            print(f"Response from server: {response}")

    except OSError as error:
        print(f"Socket error: {error}")

# Run the program.
if __name__ == "__main__":
    main()
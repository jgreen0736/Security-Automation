# Security Automation

Small educational Python networking exercises:

- `server.py` starts a TCP server on `127.0.0.1:5001`.
- `client.py` connects to the local server and sends a test message.
- `port_scanner.py` checks a user-specified TCP port range.

## Usage

Start the server in one terminal:

```bash
python3 server.py
```

Run the client in a second terminal:

```bash
python3 client.py
```

Scan a host and port range you own or have permission to test:

```bash
python3 port_scanner.py 127.0.0.1 20 25
```

These exercises are for authorized, educational testing only.

## Findings

See [`docs/findings/`](docs/findings/) for the dated exercise notes.

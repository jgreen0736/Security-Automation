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

## Email and Slack alerts

Run both alert paths offline with mocked SMTP and Slack transports:

```bash
python3 alert_demo.py --mock
```

The mock run validates each alert's payload and reports simulated success without contacting either service. To send real alerts, replace the placeholders in `.env` with your own values and run `python3 alert_demo.py --send`. Do not commit `.env`; it is excluded by `.gitignore`.

## Findings

See [`docs/findings/`](docs/findings/) for the dated exercise notes.

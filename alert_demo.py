"""Send email and Slack alerts, or exercise both paths with offline mocks."""

from __future__ import annotations

import argparse
import json
import os
import smtplib
import urllib.request
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch


PLACEHOLDERS = {
    "SMTP_USERNAME": "your_email@example.com",
    "SMTP_PASSWORD": "your_app_password",
    "ALERT_EMAIL": "security-team@example.com",
    "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/your/webhook",
}


def load_env_file(path: Path) -> dict[str, str]:
    """Load simple KEY=VALUE entries, preferring values already in the environment."""
    config: dict[str, str] = {}
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        config[key] = os.environ.get(key, value)
    return config


def require_real_config(config: dict[str, str]) -> None:
    required = (
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "ALERT_EMAIL",
        "SLACK_WEBHOOK_URL",
    )
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError(f"Missing configuration: {', '.join(missing)}")

    placeholder_values = set(PLACEHOLDERS.values())
    placeholder_keys = [key for key in required if config[key] in placeholder_values]
    if placeholder_keys:
        raise ValueError(
            "Replace placeholder values before sending: " + ", ".join(placeholder_keys)
        )


def send_email_alert(config: dict[str, str], subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = config["SMTP_USERNAME"]
    message["To"] = config["ALERT_EMAIL"]
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(
        config["SMTP_HOST"], int(config["SMTP_PORT"]), timeout=10
    ) as smtp:
        smtp.starttls()
        smtp.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
        smtp.send_message(message)


def send_slack_alert(config: dict[str, str], text: str) -> None:
    request = urllib.request.Request(
        config["SLACK_WEBHOOK_URL"],
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        if not 200 <= response.status < 300:
            raise RuntimeError(f"Slack webhook returned HTTP {response.status}")


def run_mock_demo() -> None:
    """Run both alert senders against mocked transports; no network activity occurs."""
    fake_config = {
        "SMTP_HOST": "smtp.example.test",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "sender@example.test",
        "SMTP_PASSWORD": "mock-password",
        "ALERT_EMAIL": "team@example.test",
        "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/mock/mock/mock",
    }
    subject = "Security Automation mock alert"
    body = "Email alert transport mock passed."
    slack_text = "Security Automation mock alert: Slack transport mock passed."

    with patch("alert_demo.smtplib.SMTP") as smtp_factory:
        send_email_alert(fake_config, subject, body)
        smtp = smtp_factory.return_value.__enter__.return_value
        smtp.starttls.assert_called_once_with()
        smtp.login.assert_called_once_with("sender@example.test", "mock-password")
        sent_message = smtp.send_message.call_args.args[0]
        assert sent_message["To"] == "team@example.test"
        assert sent_message["Subject"] == subject
        assert sent_message.get_content().strip() == body
    print("MOCK PASS: email alert composed and submitted through mocked SMTP")

    mock_response: Any = MagicMock()
    mock_response.__enter__.return_value.status = 200
    with patch("alert_demo.urllib.request.urlopen", return_value=mock_response) as urlopen:
        send_slack_alert(fake_config, slack_text)
        request = urlopen.call_args.args[0]
        assert request.full_url == fake_config["SLACK_WEBHOOK_URL"]
        assert request.method == "POST"
        assert json.loads(request.data.decode("utf-8")) == {"text": slack_text}
    print("MOCK PASS: Slack alert posted through mocked webhook (HTTP 200 simulated)")
    print("No email or Slack request was sent over the network.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mock", action="store_true", help="mock both transports offline")
    mode.add_argument("--send", action="store_true", help="send real alerts using .env")
    args = parser.parse_args()

    if args.mock:
        run_mock_demo()
        return

    config = load_env_file(Path(__file__).with_name(".env"))
    require_real_config(config)
    subject = "Security Automation test alert"
    body = "Email alert test from Security Automation."
    send_email_alert(config, subject, body)
    print("Email alert submitted to SMTP.")
    send_slack_alert(config, f"{subject}: Slack webhook test.")
    print("Slack webhook accepted the alert.")


if __name__ == "__main__":
    main()

#!/Users/kamrankafi/.config/google-tokens/venv/bin/python3
"""Gmail multi-account reader for Obsidian ingest pipeline.

Usage:
    gmail-reader.py --setup --account SLUG        # One-time OAuth per account
    gmail-reader.py --account SLUG --after ISO    # Fetch emails as JSON
    gmail-reader.py --account SLUG --after ISO --limit N

Tokens stored in ~/.config/google-tokens/gmail-readonly-{slug}.pickle
Client secret at ~/.config/google-tokens/client_secret.json
"""

import argparse
import base64
import json
import os
import pickle
import re
import sys
from datetime import datetime, timezone
from email.utils import parseaddr
from html.parser import HTMLParser
from pathlib import Path

# --- Google API imports ---
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------------------------------------------------------------------------
# Account configuration
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "k-at-amuse-us": "k@amuse.us",
    "vizucla-at-gmail-com": "vizucla@gmail.com",
    "kkafimd-at-gmail-com": "kkafimd@gmail.com",
    "kam4sale-at-gmail-com": "kam4sale@gmail.com",
}

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_DIR = Path.home() / ".config" / "google-tokens"
CLIENT_SECRET = TOKEN_DIR / "client_secret.json"


# ---------------------------------------------------------------------------
# HTML tag stripper (for emails without text/plain part)
# ---------------------------------------------------------------------------
class _TagStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []

    def handle_data(self, data):
        self._text.append(data)

    def get_text(self):
        return "".join(self._text).strip()


def strip_html(html: str) -> str:
    s = _TagStripper()
    s.feed(html)
    return s.get_text()


# ---------------------------------------------------------------------------
# Token management
# ---------------------------------------------------------------------------
def _token_path(slug: str) -> Path:
    return TOKEN_DIR / f"gmail-readonly-{slug}.pickle"


def _load_or_refresh_creds(slug: str):
    """Load pickled credentials, refresh if expired. Returns None if missing."""
    path = _token_path(slug)
    if not path.exists():
        return None
    with open(path, "rb") as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(path, "wb") as f:
            pickle.dump(creds, f)
    return creds


def _run_oauth_setup(slug: str):
    """Interactive OAuth flow — opens browser, stores token."""
    email = ACCOUNTS[slug]
    if not CLIENT_SECRET.exists():
        _err(f"Missing {CLIENT_SECRET}. Download from GCP Console.")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0, login_hint=email)

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    path = _token_path(slug)
    with open(path, "wb") as f:
        pickle.dump(creds, f)
    os.chmod(path, 0o600)
    print(f"Token saved: {path}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Gmail API helpers
# ---------------------------------------------------------------------------
def _build_service(creds):
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _iso_to_epoch(iso_str: str) -> int:
    """Convert ISO 8601 timestamp to Unix epoch seconds."""
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return int(dt.timestamp())


def _get_header(headers: list, name: str) -> str:
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _extract_body(payload: dict) -> str:
    """Extract text body from Gmail message payload. Prefer text/plain."""
    mime = payload.get("mimeType", "")

    # Simple single-part message
    if mime == "text/plain" and "body" in payload:
        data = payload["body"].get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Multipart — recurse into parts
    parts = payload.get("parts", [])

    # First pass: look for text/plain
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Second pass: look for text/html, strip tags
    for part in parts:
        if part.get("mimeType") == "text/html":
            data = part.get("body", {}).get("data", "")
            if data:
                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                return strip_html(html)

    # Nested multipart (e.g., multipart/alternative inside multipart/mixed)
    for part in parts:
        if part.get("mimeType", "").startswith("multipart/"):
            result = _extract_body(part)
            if result:
                return result

    return ""


def _fetch_messages(service, after_epoch: int, limit: int) -> list:
    """List message IDs matching the time filter."""
    query = f"after:{after_epoch}"
    ids = []
    page_token = None

    while len(ids) < limit:
        resp = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=min(limit - len(ids), 100),
                pageToken=page_token,
            )
            .execute()
        )
        for msg in resp.get("messages", []):
            ids.append(msg["id"])
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return ids[:limit]


def _get_message(service, msg_id: str, account_slug: str) -> dict:
    """Fetch a single message and return structured dict."""
    raw = (
        service.users()
        .messages()
        .get(userId="me", id=msg_id, format="full")
        .execute()
    )
    headers = raw.get("payload", {}).get("headers", [])
    from_raw = _get_header(headers, "From")
    from_name, from_addr = parseaddr(from_raw)

    # Parse date
    date_str = _get_header(headers, "Date")
    date_iso = ""
    if date_str:
        # Try to parse the email date
        from email.utils import parsedate_to_datetime

        try:
            dt = parsedate_to_datetime(date_str)
            date_iso = dt.astimezone(timezone.utc).isoformat()
        except Exception:
            date_iso = date_str

    body = _extract_body(raw.get("payload", {}))

    return {
        "id": msg_id,
        "account": account_slug,
        "subject": _get_header(headers, "Subject"),
        "from": from_addr,
        "from_name": from_name,
        "to": _get_header(headers, "To"),
        "date": date_iso,
        "snippet": raw.get("snippet", ""),
        "body": body,
        "labels": raw.get("labelIds", []),
    }


# ---------------------------------------------------------------------------
# Error output
# ---------------------------------------------------------------------------
def _err(msg: str, account: str = ""):
    """Print structured error to stderr."""
    err = {"error": msg}
    if account:
        err["account"] = account
    print(json.dumps(err), file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Gmail multi-account reader")
    parser.add_argument(
        "--account", required=True, help="Account slug (e.g., k-at-amuse-us)"
    )
    parser.add_argument(
        "--after", help="ISO 8601 timestamp — fetch emails after this date"
    )
    parser.add_argument("--limit", type=int, default=25, help="Max messages (default 25)")
    parser.add_argument(
        "--setup", action="store_true", help="Run interactive OAuth setup"
    )
    args = parser.parse_args()

    if args.account not in ACCOUNTS:
        _err(
            f"Unknown account: {args.account}. Valid: {', '.join(ACCOUNTS.keys())}",
            args.account,
        )
        sys.exit(1)

    # --- Setup mode ---
    if args.setup:
        _run_oauth_setup(args.account)
        print(f"Setup complete for {ACCOUNTS[args.account]}", file=sys.stderr)
        sys.exit(0)

    # --- Read mode ---
    if not args.after:
        _err("--after is required in read mode", args.account)
        sys.exit(1)

    creds = _load_or_refresh_creds(args.account)
    if not creds:
        _err(
            f"No token for {args.account}. Run: gmail-reader.py --setup --account {args.account}",
            args.account,
        )
        sys.exit(1)

    try:
        service = _build_service(creds)
        after_epoch = _iso_to_epoch(args.after)
        msg_ids = _fetch_messages(service, after_epoch, args.limit)

        messages = []
        for mid in msg_ids:
            try:
                messages.append(_get_message(service, mid, args.account))
            except Exception as e:
                print(
                    json.dumps({"warning": f"Failed to fetch {mid}: {e}"}),
                    file=sys.stderr,
                )

        print(json.dumps(messages, indent=2))

    except Exception as e:
        _err(str(e), args.account)
        sys.exit(1)


if __name__ == "__main__":
    main()

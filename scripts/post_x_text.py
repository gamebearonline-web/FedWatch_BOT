import os
import sys
import json
import requests
from requests_oauthlib import OAuth1


def must_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env: {name}")
    return v


def main() -> int:
    api_key = must_env("X_API_KEY")
    api_secret = must_env("X_API_KEY_SECRET")
    access_token = must_env("X_ACCESS_TOKEN")
    access_secret = must_env("X_ACCESS_TOKEN_SECRET")
    text = must_env("POST_TEXT")

    dry_run = os.getenv("DRY_RUN", "false").strip().lower() in ("1", "true", "yes", "y")

    payload = {"text": text}

    if dry_run:
        print("DRY_RUN=true; would post payload:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    url = "https://api.twitter.com/2/tweets"

    auth = OAuth1(
        client_key=api_key,
        client_secret=api_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_secret,
        signature_type="auth_header",
    )

    r = requests.post(url, json=payload, auth=auth, timeout=30)
    if r.status_code >= 300:
        print("❌ Post failed")
        print("Status:", r.status_code)
        print("Body:", r.text)
        return 1

    print("✅ Posted:", r.text)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("❌ Error:", str(e))
        sys.exit(1)

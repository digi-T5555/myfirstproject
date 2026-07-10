#!/usr/bin/env python3

import sys
import time
import hashlib
import requests

BASE_URL = "https://users.roblox.com/v1/users"


def get_response(userid):
    url = f"{BASE_URL}/{userid}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def hash_content(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <userid>")
        sys.exit(1)

    userid = sys.argv[1]
    previous_hash = None

    print(f"Monitoring {BASE_URL}/{userid}")
    print("Checking every 5 minutes...\n")

    while True:
        try:
            content = get_response(userid)
            current_hash = hash_content(content)

            if previous_hash is None:
                print("Initial response received.")
                previous_hash = current_hash
            elif current_hash != previous_hash:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] CHANGE DETECTED!")
                previous_hash = current_hash
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] No change.")

        except requests.RequestException as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request failed: {e}")

        time.sleep(300)


if __name__ == "__main__":
    main()

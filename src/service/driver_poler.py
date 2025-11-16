import json
import os  # <-- ADDED
import time
from datetime import datetime

import requests
from google.oauth2.credentials import Credentials
from unzip_functions import unzip_file

TOKEN_JSON = "token.json"
PAGE_TOKEN_FILE = "page_token.json"
POLL_INTERVAL = 60  # seconds between checks
DOWNLOAD_DIR = "transcriptdownloads"  # <-- ADDED: Directory to save downloaded files


def save_page_token(token):
    """Save the page token to disk"""
    with open(PAGE_TOKEN_FILE, "w") as f:
        json.dump({"page_token": token}, f)


def load_page_token():
    """Load the page token from disk"""
    try:
        with open(PAGE_TOKEN_FILE, "r") as f:
            return json.load(f).get("page_token")
    except FileNotFoundError:
        return None


def get_start_page_token(creds):
    """Get a fresh start page token from Google Drive"""
    token_url = "https://www.googleapis.com/drive/v3/changes/startPageToken"
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.get(token_url, headers=headers)
    resp.raise_for_status()
    return resp.json()["startPageToken"]


def check_for_changes(creds, page_token):
    """
    Check for changes since the given page token.
    Returns: (changes_list, new_page_token)
    """
    changes_url = "https://www.googleapis.com/drive/v3/changes"
    headers = {"Authorization": f"Bearer {creds.token}"}
    params = {
        "pageToken": page_token,
        "spaces": "drive",
        "pageSize": 100,
        "includeItemsFromAllDrives": False,
        "supportsAllDrives": False,
        "fields": "nextPageToken,newStartPageToken,changes(fileId,changeType,file(id,name,mimeType,trashed,parents,modifiedTime))",
    }

    resp = requests.get(changes_url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    changes = data.get("changes", [])

    # Get the new page token (prefer newStartPageToken over nextPageToken)
    new_token = data.get("newStartPageToken") or data.get("nextPageToken")

    return changes, new_token


# --- NEW FUNCTION ---
def download_file(creds, file_id, filename):
    """Download a file from Google Drive"""
    print(f"      📥 Downloading '{filename}'...")

    # Ensure download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
    headers = {"Authorization": f"Bearer {creds.token}"}
    params = {"alt": "media"}  # This is crucial for downloading file content

    try:
        # Use stream=True for potentially large files
        with requests.get(
            download_url, headers=headers, params=params, stream=True
        ) as resp:
            resp.raise_for_status()
            # Write the file in chunks
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"      ✅ Successfully downloaded to: {filepath}")
        return filepath
    except requests.exceptions.HTTPError as e:
        # This can happen if you try to download a Google Doc without exporting
        print(f"      ❌ FAILED to download '{filename}': {e}")
    except Exception as e:
        print(f"      ❌ An error occurred during download: {e}")


# --- MODIFIED FUNCTION ---
def process_changes(creds, changes):  # <-- ADDED 'creds'
    """Process and display the changes"""
    if not changes:
        return

    print(f"\n{'='*60}")
    print(f"🔔 CHANGES DETECTED: {len(changes)} change(s)")
    print(f"{'='*60}")

    for c in changes:
        change_type = c.get("changeType", "unknown")
        file_id = c.get("fileId")
        file_meta = c.get("file") or {}
        name = file_meta.get("name", "Unknown")
        mime_type = file_meta.get("mimeType", "Unknown")
        trashed = file_meta.get("trashed", False)
        modified_time = file_meta.get("modifiedTime", "Unknown")

        if trashed:
            print(f"  🗑️  DELETED: {name}")
            print(f"      File ID: {file_id}")

        elif change_type == "file":
            # This is an add or modify event

            # Check for Google Folders (can't be downloaded)
            if mime_type == "application/vnd.google-apps.folder":
                print(f"  📁 FOLDER CHANGED: {name}")
                print(f"      File ID: {file_id}")

            # Check for Google native files (require export, not download)
            elif mime_type.startswith("application/vnd.google-apps"):
                print(f"  📑 GOOGLE DOC/SHEET CHANGED: {name}")
                print(f"      Type: {mime_type}")
                print(f"      File ID: {file_id}")
                print("      (Skipping download, requires 'export' API)")

            # This is a standard downloadable file (e.g., PDF, TXT, JPG)
            else:
                print(f"  📄 FILE CHANGED: {name}")
                print(f"      Type: {mime_type}")
                print(f"      File ID: {file_id}")
                print(f"      Modified: {modified_time}")

                # --- THIS IS THE NEW PART ---
                file_path = download_file(creds, file_id, name)
                info = unzip_file(file_path, DOWNLOAD_DIR)

                if info is None:
                    return None

                (transcript, start_time, attendees, team_name) = info

                request_body = {
                    "transcript": transcript,
                    "start_time": start_time,
                    "team_name": team_name,
                    "attendees": attendees
                }

                # Needs to be a request.
                requests.post(f"http://localhost:8000/generateminutes", json=request_body)

                # ----------------------------

        else:
            print(f"  ℹ️  {change_type.upper()}: {name}")
            print(f"      File ID: {file_id}\n")


def poll_drive_changes():
    """Main polling loop"""
    print("=" * 60)
    print("Google Drive Change Poller")
    print("=" * 60)
    print(f"Poll interval: {POLL_INTERVAL} seconds")
    print(f"Files will be saved to: {os.path.abspath(DOWNLOAD_DIR)}")  # <-- ADDED
    print("Press Ctrl+C to stop\n")

    # Load credentials
    creds = Credentials.from_authorized_user_file(
        TOKEN_JSON, scopes=["https://www.googleapis.com/auth/drive"]
    )

    # Get or load page token
    page_token = load_page_token()

    if not page_token:
        print("No stored page token found. Getting fresh start token...")
        page_token = get_start_page_token(creds)
        save_page_token(page_token)
        print(f"✅ Initialized with page token: {page_token}\n")
    else:
        print(f"✅ Loaded page token: {page_token}\n")

    print(f"🔍 Starting to poll for changes...\n")

    poll_count = 0

    try:
        while True:
            poll_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Check for changes
                changes, new_token = check_for_changes(creds, page_token)

                if changes:
                    # --- MODIFIED CALL ---
                    process_changes(creds, changes)  # <-- Pass 'creds'
                else:
                    print(
                        f"[{timestamp}] Poll #{poll_count}: No changes detected",
                        flush=True,
                    )

                # Update the page token
                if new_token and new_token != page_token:
                    page_token = new_token
                    save_page_token(page_token)

            except requests.exceptions.HTTPError as e:
                print(f"❌ HTTP Error: {e}")
                if e.response.status_code == 401:
                    print("Token expired. Please refresh your credentials.")
                    break
            except Exception as e:
                print(f"❌ Error: {e}")

            # Wait before next poll
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n🛑 Polling stopped by user")
        print(f"Total polls: {poll_count}")
        print(f"Final page token saved: {page_token}")


if __name__ == "__main__":
    poll_drive_changes()

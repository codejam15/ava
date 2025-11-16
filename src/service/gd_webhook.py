from oauthlib.oauth2.rfc6749.clients import AUTH_HEADER
import uvicorn
from fastapi import FastAPI, APIRouter, Header, status, HTTPException
from typing import Annotated
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import uuid



if __name__ == "__main__":

    watch_url = "https://www.googleapis.com/drive/v3/changes/watch"
    # --- 1. Load OAuth credentials from token.json ---
    creds = Credentials.from_authorized_user_file(
        "token.json",
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    # # Refresh the access token if expired
    # if not creds.valid and creds.refresh_token:
    #     creds.refresh(Request())

    # --- 2. Define your watch URL and request body ---
    watch_url = "https://www.googleapis.com/drive/v3/changes/watch"

    id_uuid = str(uuid.uuid4())

    # --- 3. Add the Authorization header ---
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }


    url = "https://www.googleapis.com/drive/v3/changes/startPageToken"
    headers = {
        "Authorization": f"Bearer {creds.token}"
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    start_page_token = resp.json()["startPageToken"]
    print("Start page token:", start_page_token)



    request_body = {
        "id": id_uuid,
        "type": "web_hook",
        "address": "https://unclandestinely-sealable-layne.ngrok-free.dev/webhook/drive"
    }



    response = requests.post(watch_url, params={"pageToken": start_page_token}, headers=headers, json=request_body)

    print(response.status_code)
    print(response.text)

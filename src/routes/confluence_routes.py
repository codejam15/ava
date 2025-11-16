from datetime import date

import requests

from src.db.schema import Team
from src.models.meeting import MeetingResponseModel
from src.db.dao import TeamDao


def createPage(team: Team, model: MeetingResponseModel) -> str:
    today = date.today()
    # --- Confluence API info ---
    base_url = "https://zaatarfluence.atlassian.net/wiki/api/v2/pages"
    auth = (
        "maalekianmahan@gmail.com",
        "ATATT3xFfGF0WUsHWadDCwKXYbQz2f14ieetZ7pcgmwU935aO82zSDiHvIbkl3eavBUsJYCAfVbxeG6t0qNeY0zweb9ajSDyK_7wp-MMfNSLDZb2XTjBVnTxwtlvYesEtafK-oNbBpFPHvkhfqilxr1kSjwUhKnHj3f-WExvm-XjN1ugxSNnH5s=DC769044",
    )
    space_key = "MFS"
    
    space_id: str = team.space_id
    parent_id: str = team.parent_id
    page_title: str = "Meeting of " + today.strftime("%B %d, %Y")

    # --- Meeting info ---

    # --- HTML template with placeholders ---
    html_template: str = f"""
    <h1>Meeting Minutes: {model.title}</h1>
    <p><strong>Date:</strong> {model.meeting_date}</p>
    <p><strong>Attendees:</strong> {model.attendees}</p>

    <h2>Updates</h2>
    <p>{model.updates}</p>
    <h2>RoadBlocks</h2>
    <p>{model.roadblocks}</p>
    <h2>Next Steps</h2>
    <p>{model.nextsteps}</p>
    <h2>Notes</h2>
    <p>{model.notes}</p>
"""

    print(html_template)
    # --- Prepare payload ---
    payload = {
        "spaceId": space_id,
        "status": "current",
        "title": page_title,
        "parentId": parent_id,
        "body": {"representation": "storage", "value": html_template},
        "subtype": "live",
    }
    # --- Make the API request ---
    response = requests.post(base_url, auth=auth, json=payload)
    # --- Output result ---
    if response.status_code == 200 or response.status_code == 201:
        data = response.json()
        print("Page created successfully!")
        url = data["_links"]["base"] + data["_links"]["webui"]
        return url
    else:
        print("Error creating page:", response.status_code)
        print(response.text)
        raise Exception("The confluence page could not be created")

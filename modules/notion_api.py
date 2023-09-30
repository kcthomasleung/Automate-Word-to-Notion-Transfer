import json
import requests
from datetime import datetime
from typing import List, Dict


class NotionAPI:
    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.notion_api_url = "https://api.notion.com/v1/pages"
        self.notion_query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-02-22",  # Notion API version
            "Content-Type": "application/json"
        }

    def split_content_into_blocks(self, content: str) -> List[Dict]:
        max_length = 2000  # Maximum allowed characters per text block in Notion
        blocks = []
        while len(content) > max_length:
            # Find the last space within the allowable length
            split_index = content.rfind(' ', 0, max_length)
            # If no space found, just split at the maximum length
            if split_index == -1:
                split_index = max_length
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"type": "text", "text": {"content": content[:split_index]}}]}})


            content = content[split_index:].strip()
        # Append the remaining content as a block
        if content:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}})
            return blocks

    def entry_exists(self, date: str) -> bool:
        query_payload = {
            "filter": {
                "property": "Date",
                "date": {"equals": date}
            }
        }
        response = requests.post(self.notion_query_url, json=query_payload, headers=self.headers)
        if response.status_code == 200:
            results = response.json().get('results', [])
            return len(results) > 0
        else:
            print(f"Failed to query entries: {response.text}")
            return False

    def readDatabase(self):
        res = requests.request("POST", self.notion_query_url, headers=self.headers)
        data = res.json()
        json_string = json.dumps(data["results"], indent=4)
        print(res.status_code)
        print(json_string)

        return data

    def upload_entries(self, entries: List[Dict]):
        for entry in entries:
            # Parse and format the date string
            date_object = datetime.strptime(entry['date'], "%d-%m-%Y")
            formatted_date_string = date_object.strftime("%Y-%m-%d")

            if self.entry_exists(formatted_date_string):
                print(f"Entry already exists for {formatted_date_string}, skipping.")
                continue

            print(entry)

            # Split content into multiple blocks if it exceeds the limit
            children_blocks = self.split_content_into_blocks(entry['content'])

            page_properties = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    'Date': {
                        'type': 'date',
                        'date': {
                            'start': formatted_date_string
                        }
                    },
                },
                "children": children_blocks
            }
            response = requests.post(self.notion_api_url, json=page_properties, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to upload entry: {entry['date']}. Error: {response.text}")

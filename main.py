import os
from dotenv import load_dotenv
import pprint
from modules.word_extractor import WordExtractor
from modules.notion_api import NotionAPI

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    token = os.getenv('NOTION_KEY')
    database_id = os.getenv('NOTION_PAGE_ID')
    path_to_document = 'data/Journal.docx'

    # Extract entries from the Word document
    extractor = WordExtractor(path_to_document)
    entries = extractor.extract_entries()

    # Upload entries to Notion
    notion = NotionAPI(token, database_id)
    notion.upload_entries(entries)


if __name__ == "__main__":
    main()

from docx import Document
import re
from dateutil import parser


class WordExtractor:
    def __init__(self, path):
        self.document = Document(path)

    def extract_entries(self):
        entries = []
        year = None
        month = None
        entry_date = None
        entry_title = None
        content = []

        # Define a date pattern to match the potential date strings more precisely
        date_pattern = re.compile(r"^\d{1,2}[-/]\d{1,2}( \w+)?[-/]?(\d{2,4})?( [-–—] \w+)?|\d{1,2} \w+ \d{2,4}( [-–—] \w+)?|\d{1,2} \w+$")


        for paragraph in self.document.paragraphs:
            text = paragraph.text.strip()

            # Check if the paragraph is a Year
            if re.match(r"^\d{4}$", text):
                year = text
                print(f"Currently in {year}\n-------------------------------------------")
                continue

            # Check if the paragraph is a Month
            if re.match(r"^(January|February|March|April|May|June|July|August|September|October|November|December)$",
                        text):
                month = text
                print(f"Currently in {month}")
                continue

            # Try to parse the date, if the paragraph text matches the refined date pattern
            if date_pattern.match(text):
                try:
                    # Extract title if present
                    title = None
                    if '–' in text or '—' in text or '-' in text:
                        text, title = re.split('[-–—]', text, maxsplit=1)
                        text, title = text.strip(), title.strip()

                    # Remove day name, if present, before parsing
                    date_string = re.sub(r" \w+$", "", text)
                    date = parser.parse(date_string, dayfirst=True)  # Adjust dayfirst as per your date format
                    if year and date.year != int(year):
                        date = date.replace(year=int(year))

                    # Save the previous entry
                    if entry_date and content:
                        entries.append({
                            "date": entry_date,
                            "content": "\n".join(content),
                            "title": entry_title  # Save the title
                        })

                    # Start a new entry
                    entry_date = date.strftime("%d-%m-%Y")
                    entry_title = title  # Save the new title
                    content = []
                except ValueError:
                    content.append(text)
            else:
                # If it's not a date, consider it as content
                content.append(text)

        # Save the last entry
        if entry_date and content:
            entries.append({
                "date": entry_date,
                "content": "\n".join(content),
                "title": entry_title
            })

        return entries








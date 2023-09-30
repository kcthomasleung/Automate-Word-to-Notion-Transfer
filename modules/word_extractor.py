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
        content = []

        # Define a date pattern to match the potential date strings more precisely
        date_pattern = re.compile(
            r"^\d{1,2}[-/]\d{1,2}( \w+)?[-/]?(\d{2,4})?( - \w+)?|\d{1,2} \w+ \d{2,4}( - \w+)?|\d{1,2} \w+$")
        for paragraph in self.document.paragraphs:
            text = paragraph.text.strip()

            # Check if the paragraph is a Year
            if re.match(r"^\d{4}$", text):
                year = text
                continue

            # Check if the paragraph is a Month
            if re.match(r"^(January|February|March|April|May|June|July|August|September|October|November|December)$",
                        text):
                month = text
                continue

            # Try to parse the date, if the paragraph text matches the date pattern
            if date_pattern.match(text):
                try:
                    # Remove day name and hyphen if present, before parsing
                    date_string = re.sub(r"( - \w+)|( \w+)$", "", text)
                    date = parser.parse(date_string,
                                        dayfirst=True)  # Adjust dayfirst as per your date format  # Adjust dayfirst as per your date format
                    if year and date.year != int(year):
                        date = date.replace(year=int(year))
                    if entry_date and content:
                        entries.append({
                            "date": entry_date,
                            "content": "\n".join(content)
                        })
                    entry_date = date.strftime("%d-%m-%Y")
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
                "content": "\n".join(content)
            })

        return entries







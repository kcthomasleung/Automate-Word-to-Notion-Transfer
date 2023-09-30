import unittest
from modules.word_extractor import WordExtractor

word_file_path = '../data/Journal.docx'


class TestWordExtractor(unittest.TestCase):

    def test_entries_content(self):
        extractor = WordExtractor(word_file_path)
        entries = extractor.extract_entries()

        # Loop through each entry in entries
        for entry in entries:
            print("Date:", entry.get('date'))
            print("Content:", entry.get('content'))
            # Check if 'date' and 'content' keys exist and have values
            self.assertIn('date', entry, "Entry should have a 'date' field")
            self.assertIn('content', entry, "Entry should have a 'content' field")
            self.assertTrue(entry['date'], "Entry 'date' field should not be empty")
            self.assertTrue(entry['content'], "Entry 'content' field should not be empty")


if __name__ == '__main__':
    unittest.main()

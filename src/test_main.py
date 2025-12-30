import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title"
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_title(self):
        markdown = "This is a title"
        self.assertRaises(ValueError, extract_title, markdown)


if __name__ == "__main__":
    unittest.main()

import unittest

from helperfunctions import extract_title

class TestHelperFunctions(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# This is a title\n\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title", "The extracted title should match the expected value.")
        with self.assertRaises(ValueError):
            extract_title("No title here")

    def test_extract_title_no_title(self):
        with self.assertRaises(ValueError):
            extract_title("This is just some content without a title.")

    def test_extract_title_multiple_titles(self):
        markdown = "# First Title\n\nSome content here.\n\n# Second Title"
        title = extract_title(markdown)
        self.assertEqual(title, "First Title", "The extracted title should be the first one found.")

    def test_extract_title_no_hash(self):
        markdown = "This is just some content without a title."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_extract_title_only_title(self):
        markdown = "# Only Title"
        title = extract_title(markdown)
        self.assertEqual(title, "Only Title", "The extracted title should match the expected value.")
        with self.assertRaises(ValueError):
            extract_title("#")


if __name__ == "__main__":
    unittest.main()
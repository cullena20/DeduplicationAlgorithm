import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from duplicate_checker import process, extract_links, remove_links, extract_retweet, remove_retweet
# not testing html_2_text and remove_whitespace because they are already well tested

class TestProcess(unittest.TestCase):
    content1 = ""
    content2 = "       "
    content3 = "hello hi how are you this is a test"
    content4 = "https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html"
    content5 = "hello this is a test blah blah blah https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html blah testing blah blah"
    content6 = "https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html https://publicinfrastructure.org/about/ https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    content7 = "testing testing blah blah https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html testing      blah https://publicinfrastructure.org/about/ testing more testing balh blah blah  https://www.youtube.com/watch?v=dQw4w9WgXcQ potato blah "
    content8 = "potatopotatopotatohttps://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html"
    content9 = "https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html".upper()
    content10 = "https://<span>" # this shouldn't count
    # ^ do we want this to work (it doesn't)
    # now test werid case links, any other links we want to extract?
    # write code to not count non links as links (when they have characters that are not supposed to be there)

    def test_extract_links(self):
        self.assertEqual(extract_links(self.content1), []) # empty string
        self.assertEqual(extract_links(self.content2), []) # string with only whitespace
        self.assertEqual(extract_links(self.content3), []) # string of characters with no links
        self.assertEqual(extract_links(self.content4), ["https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html"]) # string of only link
        self.assertEqual(extract_links(self.content5), ["https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html"]) # link interspliced with words
        self.assertEqual(extract_links(self.content6), ["https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html", "https://publicinfrastructure.org/about/", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"]) # three links
        self.assertEqual(extract_links(self.content7), ["https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html", "https://publicinfrastructure.org/about/", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"]) # three links interspliced with words
        self.assertEqual(extract_links(self.content8), ["https://www.nytimes.com/2023/03/01/world/europe/ukraine-russia-tanks.html"]) # seperate link with no whitespace behind it

    def test_remove_links(self):
        self.assertEqual(remove_links(self.content1), self.content1)
        self.assertEqual(remove_links(self.content2), self.content2)
        self.assertEqual(remove_links(self.content3), self.content3)
        self.assertEqual(remove_links(self.content4), "")
        self.assertEqual(remove_links(self.content5), "hello this is a test blah blah blah  blah testing blah blah")
        self.assertEqual(remove_links(self.content6), "  ")
        self.assertEqual(remove_links(self.content7),  "testing testing blah blah  testing      blah  testing more testing balh blah blah   potato blah ")
        self.assertEqual(remove_links(self.content8), "potatopotatopotato")


    def test_extract_retweet(self):
        pass

    def test_remove_retweet(self):
        pass


if __name__ == "__main__":
    unittest.main()
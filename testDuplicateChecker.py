import unittest
from PostClass import Post
from duplicate_checker import identical_content, similar_content, similar_names, identical_cross, similar_cross, same_author_content, same_media, is_duplicate
import pickle

with open("complete_dataset.pickle", "rb") as file:
 df = pickle.load(file)

class TestDuplicateChecker(unittest.TestCase):
    post1 = Post(content="")
    post2 = Post(content="")
    post3 = Post(content="testing")
    post4 = Post(content="testing")
    post5 = Post(content="different_testing")
    post6 = Post(content="TESTING")
    post7 = Post(content="and so it goes as the jackelope leaped over the stream of idle dolphins")
    post8 = Post(content="ajd so itt goes ass the jayckalope leaps over the sreim of ilde doplahins")
    post9 = Post(content="               and    so it         goes as the    jackelope     leaped over         the stream    of idle dolphins              ")
    post10 = Post(content="               and    so it         goes as the    jackelope     leaped over         the stream    of idle dolphins              ".upper())
    post11 = Post(content='<p>NASA, along with the @WhiteHouse and other federal agencies, has declared 2023 a <a href=""https://social.beachcom.org/tags/YearOfOpenScience"" class=""mention hashtag"" rel=""nofollow noopener noreferrer"" target=""_blank"">#<span>YearOfOpenScience</span></a> to celebrate the benefits and successes created through the open sharing of data, information, and knowledge.</p><p>Learn more: <a href=""http://bit.ly/3jFWAoW"" rel=""nofollow noopener noreferrer"" target=""_blank""><span class=""invisible"">http://</span><span class="""">bit.ly/3jFWAoW</span><span class=""invisible""></span></a><br><a href=""https://social.beachcom.org/tags/NASAEarth"" class=""mention hashtag"" rel=""nofollow noopener noreferrer"" target=""_blank"">#<span>NASAEarth</span></a></p>')
    post12 = Post(content="NASA, along with the @WhiteHouse and other federal agencies, has declared 2023 a https://social.beachcom.org/tags/YearOfOpenScience YearOfOpenScience to celebrate the benefits and successes created through the open sharing of data, information, and knowledge. Learn more: ""http://bit.ly/3jFWAoW bit.ly/3jFWAoW https://social.beachcom.org/tags/NASAEarth"" http://bit.ly/3jFWAoW https://social.beachcom.org/tags/NASAEarth NASAEarth")
    post13 = Post(content="NASA, along with the @WhiteHouse and other federal agencies, has declared 2023 a YearOfOpenScience to celebrate the benefits and successes created through the open sharing of data, information, and knowledge. Learn more: NASAEarth") 
    post14 = Post(content="", author="mrfishgills")
    post15 = Post(content="", author="mrfishgills")
    post16 = Post(content="", author="an0nymous_user!")
    post17 = Post(content=post11.content, author="mrfishgills")
    post18 = Post(content=post12.content, author="mrfishgills")
    post19 = Post(content=post12.content, author="someU&ER_")
    post20 = Post(content=post11.content, author="mrfishgills", name="Crazy Nasa Story")
    post21 = Post(content=post12.content, author="mrfishgills", name="Year Of Open Science")
    post22 = Post(content="https://thisisnotareallinksoitshouldntgoanywhere.com")
    threshold = 0.8

    # test a few identical content
    # test empty content 
    def test_identical_content(self):
        self.assertTrue(identical_content(self.post1, self.post2)) # empty content are duplicates
        self.assertFalse(identical_content(self.post1, self.post3)) # empty and non empty content are not duplicates
        self.assertTrue(identical_content(self.post3, self.post4)) # identical content are duplicates
        self.assertFalse(identical_content(self.post4, self.post5)) # different content are not duplicates
        self.assertFalse(identical_content(self.post4, self.post6)) # different casing are not duplicates

    # note this and similar names use process
    # test identical content
    # test various content that should be identical post processing (whitespace, casing, html vs regular, links and retweet tags) 
    # perhaps test above with very high or identical threshold
    # test posts that are very similar but with some typos (also maybe with processing stuff)
    # tests posts that are sufficiently different
    def test_similar_content_identical(self):
        self.assertTrue(similar_content(self.post1, self.post2, self.threshold))
        self.assertFalse(similar_content(self.post1, self.post3, self.threshold))
        self.assertTrue(similar_content(self.post3, self.post4, self.threshold))
        self.assertFalse(similar_content(self.post4, self.post5, self.threshold))

    def test_similar_content(self):
        self.assertTrue(similar_content(self.post4, self.post6, self.threshold)) # casing doesn't matter
        self.assertTrue(similar_content(self.post7, self.post8, self.threshold)) # some typos don't matter
        self.assertTrue(similar_content(self.post7, self.post9, self.threshold)) # whitespace doesn't matter
        self.assertTrue(similar_content(self.post7, self.post10, self.threshold)) # casing and whitespace together doesn't matter
        self.assertTrue(similar_content(self.post11, self.post12, self.threshold)) # html doesn't matter
        self.assertTrue(similar_content(self.post12, self.post13, self.threshold)) # links don't matter
        self.assertTrue(similar_content(self.post11, self.post13, self.threshold)) # links and html together don't matter

    # test identical titles
    # test titles that should be identical post processing
    # test similar titles
    # test sufficiently different titles
    def test_similar_names(self):
        self.assertTrue(similar_names(self.post1.swap_content_name(), self.post2.swap_content_name(), self.threshold)) # empty names are duplicates
        self.assertFalse(similar_names(self.post1.swap_content_name(), self.post3.swap_content_name(), self.threshold)) # empty and non empty content are not duplicates
        self.assertTrue(similar_names(self.post3.swap_content_name(), self.post4.swap_content_name(), self.threshold)) # identical content are duplicates
        self.assertFalse(similar_names(self.post4.swap_content_name(), self.post5.swap_content_name(), self.threshold)) # different content are not duplicates
        self.assertTrue(similar_names(self.post4.swap_content_name(), self.post6.swap_content_name(), self.threshold)) # casing doesn't matter
        self.assertTrue(similar_names(self.post7.swap_content_name(), self.post8.swap_content_name(), self.threshold)) # some typos don't matter
        self.assertTrue(similar_names(self.post7.swap_content_name(), self.post9.swap_content_name(), self.threshold)) # whitespace doesn't matter
        self.assertTrue(similar_names(self.post7.swap_content_name(), self.post10.swap_content_name(), self.threshold)) # casing and whitespace together doesn't matter

    # note that this code uses similar content in it, no need to test similar content too much
    # test similar content and similar names with same author and with different author
    # test similar content and different names with same author and different author
    def test_same_author_content(self):
        self.assertTrue(same_author_content(self.post14, self.post15, self.threshold)) # empty content, none title, same author
        self.assertFalse(same_author_content(self.post14, self.post16, self.threshold)) # empty content, none title, different author
        self.assertTrue(same_author_content(self.post17, self.post18, self.threshold)) # similar content, none title, same author
        self.assertFalse(same_author_content(self.post17, self.post19, self.threshold)) # similar content, none title, different author
        self.assertTrue(same_author_content(self.post20, self.post21, self.threshold)) # similar content, different title, same author

    # similar to regular identical test
    def test_identical_cross(self):
        self.assertTrue(identical_cross(self.post1.swap_content_name(), self.post2)) # 1- empty content are duplicates
        self.assertTrue(identical_cross(self.post1, self.post2.swap_content_name())) # 2- empty content are duplicates
        self.assertFalse(identical_cross(self.post1.swap_content_name(), self.post3)) # 1- empty and non empty content are not duplicates
        self.assertFalse(identical_cross(self.post1, self.post3.swap_content_name())) # 2- empty and non empty content are not duplicates
        self.assertTrue(identical_cross(self.post3.swap_content_name(), self.post4)) # 1- identical content are duplicates
        self.assertTrue(identical_cross(self.post3, self.post4.swap_content_name())) # 2- identical content are duplicates
        self.assertFalse(identical_cross(self.post4.swap_content_name(), self.post5)) # 1- different content are not duplicates
        self.assertFalse(identical_cross(self.post4, self.post5.swap_content_name())) # 2- different content are not duplicates
        self.assertFalse(identical_cross(self.post4.swap_content_name(), self.post6)) # 1- different casing are not duplicates
        self.assertFalse(identical_cross(self.post4, self.post6.swap_content_name())) # 2- different casing are not duplicates

    # similar to regular similar test
    def test_similar_cross(self):
        self.assertTrue(similar_cross(self.post4.swap_content_name(), self.post6, self.threshold)) # casing doesn't matter
        self.assertTrue(similar_cross(self.post4, self.post6.swap_content_name(), self.threshold)) # casing doesn't matter
        self.assertTrue(similar_cross(self.post7.swap_content_name(), self.post8, self.threshold)) # some typos don't matter
        self.assertTrue(similar_cross(self.post7, self.post8.swap_content_name(), self.threshold)) # some typos don't matter
        self.assertTrue(similar_cross(self.post7.swap_content_name(), self.post9, self.threshold)) # whitespace doesn't matter
        self.assertTrue(similar_cross(self.post7, self.post9.swap_content_name(), self.threshold)) # whitespace doesn't matter
        self.assertTrue(similar_cross(self.post7.swap_content_name(), self.post10, self.threshold)) # casing and whitespace together doesn't matter
        self.assertTrue(similar_cross(self.post7, self.post10.swap_content_name(), self.threshold)) # casing and whitespace together doesn't matter
        self.assertTrue(similar_cross(self.post11.swap_content_name(), self.post12, self.threshold)) # html doesn't matter
        self.assertTrue(similar_cross(self.post11, self.post12.swap_content_name(), self.threshold)) # html doesn't matter
        self.assertTrue(similar_cross(self.post12.swap_content_name(), self.post13, self.threshold)) # links don't matter
        self.assertTrue(similar_cross(self.post12, self.post13.swap_content_name(), self.threshold)) # links don't matter
        self.assertTrue(similar_cross(self.post11.swap_content_name(), self.post13, self.threshold)) # links and html together don't matter
        self.assertTrue(similar_cross(self.post11, self.post13.swap_content_name(), self.threshold)) # links and html together don't matter

    # extract_links tested elsewhere, do this assuming extract links works fine
    # check empty lists
    # check lists with false links
    # check lists with identical links
    # check lists with non identical links that lead to same place
    # check lists with non identical links that lead to different places
    # check lists with some matching links, some not
    def test_same_media(self):
        self.assertTrue(same_media(self.post1, self.post2)) # empty posts with empty list of links
        self.assertTrue(same_media(self.post7, self.post8)) # post with empty list of links
        self.assertTrue(same_media(self.post11, self.post12)) # post with two different appearing links that go to same place and other non identical links
        self.assertFalse(same_media(self.post1, self.post11)) # empty link of lists with full list of links
        # think about how to handle false links and test accordingly
        # self.assertTrue(same_media(self.post1, self.post22)) # empty link of lists with list of false links

    # once again, this goes to testing extract_retweet
    def test_same_retweet(self):
        pass

    # test the whole shebang on the dataset
    def test_is_duplicate(self):
        predictions = [is_duplicate(df["Object1"][idx], df["Object2"][idx]) for idx in df.index] # algorithm predicted values
        for i in range(len(predictions)):
            self.assertEqual(predictions[i], df["duplicate"][i])

if __name__ == '__main__':
    unittest.main()

# manually take posts from dataset or manually write them to test these
# account for lots of edge cases
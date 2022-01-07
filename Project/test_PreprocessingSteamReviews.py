from PreprocessingSteamReviews import PreprocessingSteamReviews
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from langdetect import detect
import morfeusz2
import unidecode
import unittest

class TestPreprocessingSteamReviews(unittest.TestCase):

    def test_strip_html_tags(self):
        input = '<h2>Bardzo dobra gra<h2>'
        expected = 'Bardzo dobra gra'
        result = PreprocessingSteamReviews.strip_html_tags(self, input)
        self.assertEqual(result, expected)

    def test_remove_newlines_tabs(self):
        input = 'gra mnie zachwyciła \n\tpolecam'
        expected = 'gra mnie zachwyciła   polecam'
        result = PreprocessingSteamReviews.remove_newlines_tabs(self, input)
        self.assertEqual(result, expected)

    def test_remove_whitespace(self):
        input = 'gra mnie    zachwyciła     polecam'
        expected = 'gra mnie zachwyciła polecam'
        result = PreprocessingSteamReviews.remove_whitespace(self, input)
        self.assertEqual(result, expected)

    def test_remove_non_alphanumeric_chracters(self):
        input = 'polecam, grałem w nią 100 razy!!!<3'
        expected = 'polecam  grałem w nią     razy     '
        result = PreprocessingSteamReviews.remove_non_alphanumeric_chracters(self, input)
        self.assertEqual(result, expected)
    
    def test_remove_polish_stopwords(self):
        input = ['polecam', 'grę', 'z', 'całego', 'serca', 'i', 'zagram', 'w', 'nią', 'raz', 'jeszcze']
        expected = ['polecam', 'grę', 'całego', 'serca', 'zagram', 'raz']
        result = PreprocessingSteamReviews.remove_polish_stopwords(self, input)
        self.assertEqual(result, expected)

    def test_lemmatisation(self):
        morf = morfeusz2.Morfeusz()
        input = ['polecam', 'grę', 'całego', 'serca', 'zagram', 'raz']
        expected = ['polecać', 'gra', 'cały', 'serce', 'zagrać', 'raz']
        result = PreprocessingSteamReviews.lemmatisation(self, input, morf)
        self.assertEqual(result, expected)

    def test_remove_links(self):
        input = "polecam stronę gry.pl z całego serca"
        expected = "polecam stronę  z całego serca"
        result = PreprocessingSteamReviews.remove_links(self, input)
        self.assertEqual(result, expected)

    def test_lowercase_all(self):
        input = pd.DataFrame(data=["Gra mnie zachwyciła bARDzO"], columns=['review'])
        expected = pd.DataFrame(data=["gra mnie zachwyciła bardzo"], columns=['review'])
        result = PreprocessingSteamReviews.lowercase_all(self, input)
        self.assertEqual(result['review'][0], expected['review'][0])

    def test_tokenize_all(self):
        input = pd.DataFrame(data=["gra mnie zachwyciła bardzo"], columns=['review'])
        expected = pd.DataFrame(data={'review': [["gra", "mnie", "zachwyciła", "bardzo"]]})
        result = PreprocessingSteamReviews.tokenize_all(self, input)
        self.assertEqual(result['review'][0], expected['review'][0])

    def test_remove_non_polish_reviews(self):
        input_eng = pd.DataFrame(data=["this game looks very good"], columns=['review'])
        input_pl = pd.DataFrame(data=["ta gra wygląda bardzo dobrze"], columns=['review'])
        expected_eng = pd.DataFrame(data=[], columns=['review'])
        expected_pl = pd.DataFrame(data=["ta gra wygląda bardzo dobrze"], columns=['review'])
        result_eng = PreprocessingSteamReviews.remove_non_polish_reviews(self, input_eng)
        result_pl = PreprocessingSteamReviews.remove_non_polish_reviews(self, input_pl)
        self.assertEqual(result_eng.empty, expected_eng.empty)
        self.assertEqual(result_pl.empty, expected_pl.empty)

    def test_remove_reviews_with_no_alphanumeric_items(self):
        input_with = pd.DataFrame(data=["polecam ten tytuł"], columns=['review'])
        input_without = pd.DataFrame(data=["<3!!!!!"], columns=['review'])
        expected_with = pd.DataFrame(data=["polecam ten tytuł"], columns=['review'])
        expected_without = pd.DataFrame(data=[], columns=['review'])
        result_with = PreprocessingSteamReviews.remove_reviews_with_no_alphanumeric_items(self, input_with)
        result_without = PreprocessingSteamReviews.remove_reviews_with_no_alphanumeric_items(self, input_without)
        self.assertEqual(result_with.empty, expected_with.empty)
        self.assertEqual(result_without.empty, expected_without.empty)

    def test_remove_reviews_under_n_chars(self):
        n = 20
        input_under = pd.DataFrame(data=["polecam ten tytuł"], columns=['review'])
        input_above = pd.DataFrame(data=["bardzo polecam ten tytuł"], columns=['review'])
        expected_under = pd.DataFrame(data=[], columns=['review'])
        expected_above = pd.DataFrame(data=["bardzo polecam ten tytuł z całego serca"], columns=['review'])
        result_under = PreprocessingSteamReviews.remove_reviews_under_n_chars(self, n, input_under)
        result_above = PreprocessingSteamReviews.remove_reviews_under_n_chars(self, n, input_above)
        self.assertEqual(result_under.empty, expected_under.empty)
        self.assertEqual(result_above.empty, expected_above.empty)

    def test_remove_reviews_under_n_words(self):
        n = 5
        input_under = pd.DataFrame(data={'review': [["polecam", "ten", "tytuł"]]})
        input_above = pd.DataFrame(data={'review': [["polecam", "ten", "tytuł", "z", "całego", "serca"]]})
        expected_under = pd.DataFrame(data=[], columns=['review'])
        expected_above = pd.DataFrame(data={'review': [["polecam", "ten", "tytuł", "z", "całego", "serca"]]})
        result_under = PreprocessingSteamReviews.remove_reviews_under_n_words(self, n, input_under)
        result_above = PreprocessingSteamReviews.remove_reviews_under_n_words(self, n, input_above)
        self.assertEqual(result_under.empty, expected_under.empty)
        self.assertEqual(result_above.empty, expected_above.empty)


if __name__ == '__main__':
    unittest.main()

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

    def test_upper(self):
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


if __name__ == '__main__':
    unittest.main()
import unittest
import requests
from bs4 import BeautifulSoup
import pandas as pd
from GetSteamReviews import get_reviews, get_n_appids, get_n_reviews


class TestGetSteamReviews(unittest.TestCase):
    def test_get_n_appids(self):
        n = 5
        result = get_n_appids(n)
        self.assertEqual(len(result), n)

    def test_get_reviews(self):
        appid = "292030"
        params = {
            'json': 1,
            'filter': 'recent',
            'language': 'polish',
            'day_range': 9223372036854775807,
            'review_type': 'all',
            'purchase_type': 'all',
            'cursor': '*'.encode(),
        }
        expected = True
        result = get_reviews(appid, params)
        self.assertEqual(result["success"], expected)

    def test_get_n_reviews(self):
        appid = "292030"
        n = 10
        result = get_n_reviews(appid, n)
        self.assertEqual(len(result), n)


if __name__ == '__main__':
    unittest.main()

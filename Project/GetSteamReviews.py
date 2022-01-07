import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_reviews(appid: int, params: dict) -> dict:
    """
    Funkcja wydobywająca informacje o jednej recenzji z appid.
    Parameters:
        appid (int): ID gry
        params (dict): Parametry wyszukiwania Steam
    Returns:
        dict: Odpowiedź w formacie JSON zawierająca wszystkie informacje o danej recenzji
    """
    if params is None:
        params = {'json': 1}
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + appid, params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()

def get_n_reviews(appid: int, n: int) -> list[str]:
    """
    Funkcja uzyskująca recenzje z gry o ID appid z jednej strony o n recenzjach.
    Parameters:
        appid (int): ID gry
        n (int): Liczba recenzji na stronie
    Returns:
        list[str]: Lista recenzji gier
    """
    reviews = []
    cursor = '*'
    params = {
        'json': 1,
        'filter': 'recent',
        'language': 'polish',
        'day_range': 9223372036854775807,
        'review_type': 'all',
        'purchase_type': 'all'
    }

    while n > 0:
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        cursor = response['cursor']
        reviews += response['reviews']

        if len(response['reviews']) < 100:
            break
    return reviews

def get_n_appids(n: int) -> list[str]:
    """
    Funkcja uzyskująca n ID gier z kategorii RPG.
    Parameters:
        n (int): Liczba ID gier do uzyskania
    Returns:
        list[str]: Lista ID gier w formie stringów
    """
    appids = []
    url = f'https://store.steampowered.com/search/?tags=122&category1=998'
    page = 0

    while page*25 < n:
        page += 1
        response = requests.get(url=url+str(page), headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for row in soup.find_all(class_='search_result_row'):
            appids.append(row['data-ds-appid'])

    return appids[:n]


if __name__ == "__main__":
    all_reviews = []
    all_appids = get_n_appids(25)
    m = 0
    for single_appid in all_appids:
            all_reviews += get_n_reviews(single_appid, 10000)

    df = pd.DataFrame(all_reviews)[['review', 'voted_up']]
    df.to_excel("game_reviews.xlsx")

## Feature selection algorithms in NLP
#Praca inżynierska - Norbert Sak

1. Zebranie danych - pobranie recenzji gier z kategorii RPG z API Steam'a (plik GetSteamReviews.ipynb)
2. Preprocessing zebranych danych:
    * usunięcie "\n" itd
    * usunięcie html'owych tagów
    * usunięcie spacji, gdy jest więcej niż jedna
    * usunięcię znaków interpunkcyjnych i pozostawienie tylko liter z polskiego alfabetu
    * usunięcie linków
    * usunięcie receznji, które mimo wybrania kategorii recenzij polskich to były po angielsku
    * lowercase wszystkich znaków
    * usunięcie recenzji poniżej 20 słów
    * usunięcie polskich stopword'ów
    * lemantyzacja
3. Ekstrakcja cech metodą TFIDF z użyciem unigramów i bigramów.
4. Selekcja cech wybranymi metodami, czyli Chi$^@$


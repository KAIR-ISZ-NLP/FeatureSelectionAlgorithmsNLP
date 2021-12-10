## Feature selection algorithms in NLP
# Praca inżynierska - Norbert Sak

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
    * lematyzacja
3. Ekstrakcja cech metodą TFIDF z użyciem unigramów i bigramów.
4. Selekcja cech wybranymi metodami - filtry -> Chi^2 i ANOVA(?), wrappery -> RFE (Recursive Feature Elimination) i embedded -> regularyzacja L1.
5. Użycie wybranych klasyfikatorów (MultinomialNB, SVC,LogisticRegression, RandomForestClassifier) z grid searchem i porównanie wyników dla każdej metody.
(pliki feature_selection_with_CHI2.ipynb, feature_selection_with_RFE.ipynb, feature_selection_with_LASSO.ipynb, feature_selection_with_ANOVA.ipynb)

Aktualny wygląd wyników (accuracy), w nawiasie koło wyniku liczba cech po ich selekcji (początkowo było ich około 116000):

|                         | BRAK  | Chi^2 | ANOVA | RFE   | L1    |
|-------------------------|-------|-------|-------|-------|-------|
| MultinomialNB           | 0.86  | 0.83 (2000)  | 0.84 (2000)  | 0.85 (1500)  | 0.84 (350)   |
| SVC                     | 0.84  | 0.85 (1500)  | 0.84 (1000)  | 0.86 (2000)  | 0.85 (434)   |
| LogisticRegression      | 0.84  | 0.86 (2500)  | 0.85 (1000)  | 0.87 (2000)  | 0.85 (434)   |
| RandomForestClassifier  | 0.83  | 0.82 (500)   | 0.82 (2000)  | 0.82 (1500)  | 0.82 (1301)  |


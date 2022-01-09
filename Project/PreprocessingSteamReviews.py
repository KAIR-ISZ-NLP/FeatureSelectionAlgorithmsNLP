import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from langdetect import detect
import morfeusz2
import unidecode


class PreprocessingSteamReviews():
    """
    Klasa odpowiedzialna za preprocessing recenzji, aby nadawały się one do użycia w modelach uczenia maszynowego.
    """
    def preprocess(self, df_reviews: pd.DataFrame) -> None:
        """
        Metoda odpowiadająca za wykonanie całego procesu preprocessigu wejściowego DataFrame.
        Parameters:
            text (list[str]): Wejściowy DataFrame
        """
        self.df_reviews = df_reviews
        
        self.df_reviews = self.remove_reviews_under_n_chars(99, self.df_reviews)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_newlines_tabs)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.strip_html_tags)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_whitespace)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_non_alphanumeric_chracters)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_links)
        self.df_reviews = self.remove_reviews_with_no_alphanumeric_items(self.df_reviews)
        self.df_reviews = self.remove_non_polish_reviews(self.df_reviews)
        self.df_reviews = self.lowercase_all(self.df_reviews)
        self.df_reviews = self.tokenize_all(self.df_reviews)
        self.df_reviews = self.remove_reviews_under_n_words(20, self.df_reviews)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_polish_stopwords)
        
        morf = morfeusz2.Morfeusz()
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.lemmatisation, args=(morf,))
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_polish_stopwords)
        
        self.df_reviews['review'] = self.df_reviews['review'].apply(" ".join)
        
        
    def remove_reviews_under_n_chars(self, n: int, df: pd.DataFrame) -> pd.DataFrame:
        """
        Metoda usuwająca wszystkie recenzje z df, które posiadają poniżej n znaków.
        Parameters:
            n (int): Liczba znaków
            df (pd.DataFrame): Wejściowy DataFrame
        Returns:
            pd.DataFrame: Przeprocesowany DataFrame
        """
        df['len'] = df['review'].str.len()
        df = df[df['len'] > n]
        df = df.drop(['len'], axis=1)
        return df
        
    def remove_reviews_under_n_words(self, n: int, df: pd.DataFrame) -> pd.DataFrame:
        """
        Metoda usuwająca wszystkie recenzje (po tokenizacji) z df, które posiadają poniżej n słów.
        Parameters:
            n (int): Liczba słów
            df (pd.DataFrame): Wejściowy DataFrame
        Returns:
            pd.DataFrame: Przeprocesowany DataFrame
        """
        df['len'] = df['review'].str.len()
        df = df[df['len'] > n]
        df = df.drop(['len'], axis=1)
        return df
    
    def remove_newlines_tabs(self, text: str) -> str:
        """
        Metoda usuwająca wszystkie znaki nowej linii oraz tabulacji z recenzji.
        Parameters:
            text (str): Recenzja wejściowa
        Returns:
            str: Przeprocesowana recenzja
        """
        formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ')
        return formatted_text

    def strip_html_tags(self, text: str) -> str:
        """
        Metoda usuwająca wszystkie elementy składni języka HTML z recenzji.
        Parameters:
            text (str): Recenzja wejściowa
        Returns:
            str: Przeprocesowana recenzja
        """
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    def remove_whitespace(self, text: str) -> str:
        """
        Metoda usuwająca nadmiar spacji z recenzji.
        Parameters:
            text (str): Recenzja wejściowa
        Returns:
            str: Przeprocesowana recenzja
        """
        pattern = re.compile(r'\s+') 
        Without_whitespace = re.sub(pattern, ' ', text)
        text = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
        return text

    def remove_non_alphanumeric_chracters(self, text: str) -> str:
        """
        Metoda usuwająca znaki, które nie są alfanumeryczne z recenzji.
        Parameters:
            text (str): Recenzja wejściowa
        Returns:
            str: Przeprocesowana recenzja
        """
        regex = re.compile('[^a-zA-ZAaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż ]')
        text = regex.sub(' ', text)
        return text
    
    def remove_reviews_with_no_alphanumeric_items(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Metoda usuwająca wszystkie recenzje z df, które nie zawierają żadnych znaków alfanumerycznych.
        Parameters:
            df (pd.DataFrame): Wejściowy DataFrame
        Returns:
            pd.DataFrame: Przeprocesowany DataFrame
        """
        for row, data in df.T.iteritems():
            if not any(c.isalpha() for c in data['review']):
                df.drop([row], inplace=True)
        return df
                
    def remove_non_polish_reviews(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Metoda usuwająca wszystkie recenzje z df, których językiem dominującym nie jest polski.
        Parameters:
            df (pd.DataFrame): Wejściowy DataFrame
        Returns:
            pd.DataFrame: Przeprocesowany DataFrame
        """
        for row, data in df.T.iteritems():
            if detect(data['review']) != 'pl':
                df.drop([row], inplace=True)
        return df
                
    def lowercase_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Metoda zamieniająca wszystkie znaki na małe w df.
        Parameters:
            df (pd.DataFrame): Wejściowy DataFrame
        Returns:
            pd.DataFrame: Przeprocesowany DataFrame
        """
        df['review'] = df['review'].str.lower()
        return df
        
    def tokenize_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Metoda zamieniająca wszystkie recenzje w df na listę słów, gdzie separatorem jest spacja.
        Parameters:
            df (pd.DataFrame): Wejściowy DataFrame
        Returns:
            pd.DataFrame: Przeprocesowany DataFrame
        """
        df['review'] = df['review'].str.split()
        return df
    
    def remove_polish_stopwords(self, text: list[str]) -> list[str]:
        """
        Metoda usuwająca polskie stopwordy z recenzji.
        Parameters:
            text (list[str]): Recenzja wejściowa
        Returns:
            list[str]: Przeprocesowana recenzja
        """
        stopwords = []
        with open("polish.stopwords.txt", encoding = 'utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                stopwords.append(stripped_line)
        words = [word for word in text if word.lower() not in stopwords]
        return words
    
    def lemmatisation(self, text: list[str], morf) -> list[str]:
        """
        Metoda lematyzyjąca recenzje.
        Parameters:
            text (list[str]): Recenzja wejściowa
        Returns:
            list[str]: Przeprocesowana recenzja
        """
        res = []
        for i in text:
            analysis = morf.analyse(i)
            x = analysis[0][2][1]
            x = x.split(':')[0].lower()
            res.append(x)
        return res
    
    def remove_links(self, text) -> str:
        """
        Metoda usuwająca linki z recenzji.
        Parameters:
            text (str): Recenzja wejściowa
        Returns:
            str: Przeprocesowana recenzja
        """
        remove_https = re.sub(r'http\S+', '', text)
        remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
        remove_pl = re.sub(r"\ [A-Za-z]*\.pl", " ", remove_com)
        return remove_pl


if __name__ == "__main__":
    print(PreprocessingSteamReviews.strip_html_tags.__doc__)
    # df = pd.read_excel("game_reviews.xlsx", index_col=0)
    # pre = PreprocessingSteamReviews()
    # pre.preprocess(df)
    # df_preprocessed = pre.df_reviews
    # df1 = df_preprocessed[df_preprocessed['voted_up'] == False]
    # len_f = len(df_preprocessed[df_preprocessed['voted_up'] == False])
    # df2 = df_preprocessed[df_preprocessed['voted_up'] == True][:len_f]
    # df_preprocessed = pd.concat([df1,df2])
    # df_preprocessed = df_preprocessed.sample(frac=1)
    # df_preprocessed.to_excel("game_reviews_preprocessed.xlsx")

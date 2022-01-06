import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from langdetect import detect
import morfeusz2
import unidecode


class PreprocessingSteamReviews():
    def preprocess(self, df_reviews):
        self.df_reviews = df_reviews
        
        self.remove_reviews_under_99_chars(99)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_newlines_tabs)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.strip_html_tags)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_whitespace)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_non_alphanumeric_chracters)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_links)
        self.remove_reviews_with_no_alphanumeric_items()
        self.remove_non_polish_reviews()
        self.df_reviews = self.lowercase_all(self.df_reviews)
        self.df_reviews = self.tokenize_all(self.df_reviews)
        self.remove_reviews_under_n_words(20)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_polish_stopwords)
        
        self.morf = morfeusz2.Morfeusz()
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.lemmatisation, self.morf)
        self.df_reviews['review'] = self.df_reviews['review'].apply(self.remove_polish_stopwords)
        
        self.df_reviews['review'] = self.df_reviews['review'].apply(" ".join)
        self.df_reviews.drop(['len'], inplace=True, axis=1)
        self.df_reviews.drop(['len2'], inplace=True, axis=1)
        
        
    def remove_reviews_under_99_chars(self, n):
        self.df_reviews['len'] = self.df_reviews['review'].str.len()
        self.df_reviews = self.df_reviews[self.df_reviews['len'] > n]
        
    def remove_reviews_under_n_words(self, n):
        self.df_reviews['len2'] = self.df_reviews['review'].str.len()
        self.df_reviews = self.df_reviews[self.df_reviews['len2'] > n]
    
    def remove_newlines_tabs(self, text):
        formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ')
        return formatted_text

    def strip_html_tags(self, text):
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    def remove_whitespace(self, text):
        pattern = re.compile(r'\s+') 
        Without_whitespace = re.sub(pattern, ' ', text)
        text = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
        return text

    def remove_non_alphanumeric_chracters(self, text):
        regex = re.compile('[^a-zA-ZAaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż ]')
        text = regex.sub(' ', text)
        return text
    
    def remove_reviews_with_no_alphanumeric_items(self):
        for row, data in self.df_reviews.T.iteritems():
            if not any(c.isalpha() for c in data['review']):
                self.df_reviews.drop([row], inplace=True)
                
    def remove_non_polish_reviews(self):
        for row, data in self.df_reviews.T.iteritems():
            if detect(data['review']) != 'pl':
                self.df_reviews.drop([row], inplace=True)
                
    def lowercase_all(self, df):
        df['review'] = df['review'].str.lower()
        return df
        
    def tokenize_all(self, df):
        df['review'] = df['review'].str.split()
        return df
    
    def remove_polish_stopwords(self, text):
        stopwords = []
        with open("polish.stopwords.txt", encoding = 'utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                stopwords.append(stripped_line)
        words = [word for word in text if word.lower() not in stopwords]
        return words
    
    def lemmatisation(self, text, morf):
        res = []
        for i in text:
            analysis = morf.analyse(i)
            x = analysis[0][2][1]
            x = x.split(':')[0].lower()
            res.append(x)
        return res
    
    def remove_links(self, text):
        remove_https = re.sub(r'http\S+', '', text)
        remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
        remove_pl = re.sub(r"\ [A-Za-z]*\.pl", " ", remove_com)
        return remove_pl

if __name__ == "__main__":
    df = pd.read_excel("game_reviews.xlsx", index_col=0)
    pre = PreprocessingSteamReviews()
    pre.preprocess(df)
    df_preprocessed = pre.df_reviews
    df1 = df_preprocessed[df_preprocessed['voted_up'] == False]
    len_f = len(df_preprocessed[df_preprocessed['voted_up'] == False])
    df2 = df_preprocessed[df_preprocessed['voted_up'] == True][:len_f]
    df_preprocessed = pd.concat([df1,df2])
    df_preprocessed = df_preprocessed.sample(frac=1)
    df_preprocessed.to_excel("game_reviews_preprocessed____.xlsx")
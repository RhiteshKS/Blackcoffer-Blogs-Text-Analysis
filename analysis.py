import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import string


excel_file = 'Input.xlsx'
df = pd.read_excel(excel_file)

output_directory = 'extracted_articles'

os.makedirs(output_directory, exist_ok=True)

def extract_and_save_article(url, url_id):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.title.text.strip() if soup.title else "No Title"
        
        target_div = soup.select_one('div.td-container > div > div.td-pb-span8.td-main-content > div > div.td-post-content.tagdiv-type')
        target_div2 = soup.select_one('#tdi_117 > div > div.vc_column.tdi_120.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_single_content.tdi_130.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type > div')

        if target_div:
            article_text = target_div.get_text(separator='')

        elif target_div2:
            article_text = target_div2.get_text(separator='')

        else:
            print("Target div not found.")

        output_file_path = os.path.join(output_directory, f"{url_id}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)

for index, row in df.iterrows():
    extract_and_save_article(row['URL'], row['URL_ID'])

#------------------------------------------------------------------------------------------------------------
# TEXT ANALYSIS
    

nltk.download('punkt')
nltk.download('stopwords')

class SentimentAnalysis:
    def __init__(self):
        self.stop_words = self.load_stop_words()
        self.positive_words, self.negative_words = self.create_sentiment_dictionary()

    def read_file(self, file_path, encoding='latin-1'): #utf-8 wont work, cannot account for | symbol
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()

    def clean_text(self, text):
        tokens = word_tokenize(text.lower())  
        cleaned_tokens = [word for word in tokens if word.isalpha() and word not in self.stop_words]
        return cleaned_tokens

    def create_sentiment_dictionary(self):
        positive_words = set(self.read_file('MasterDictionary/positive-words.txt').splitlines())
        negative_words = set(self.read_file('MasterDictionary/negative-words.txt').splitlines())
        return positive_words, negative_words

    def load_stop_words(self):
        stop_words_folder = 'StopWords'
        stop_words = set()

        for filename in os.listdir(stop_words_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(stop_words_folder, filename)
                stop_words.update(self.read_file(file_path, encoding='latin-1').splitlines())

        return stop_words

    def calculate_sentiment_scores(self, cleaned_tokens):
        positive_score = 0
        negative_score = 0
        for word in cleaned_tokens:
            if word in self.positive_words:
                positive_score += 1
            elif word in self.negative_words:
                negative_score += 1

        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(cleaned_tokens) + 0.000001)

        return positive_score, negative_score, polarity_score, subjectivity_score

#------------------End of Sentiment Analysis Class-----------------------------------------

class TextAnalysis:

    def __init__(self, text):
        self.text = text
        self.words_0 = word_tokenize(text)
        self.tokens = word_tokenize(text.lower())
        self.stop_words = set(stopwords.words('english'))
        self.words = [word for word in self.tokens if word not in self.stop_words and word not in string.punctuation]
        self.sentences = sent_tokenize(text)
        self.syllables_exceptions = ["es", "ed"]
        
    
    def average_sentence_length(self):
        words = [word for word in self.words_0 if word not in string.punctuation ]
        return len(words) / len(self.sentences) if self.sentences else 0
    

    def percentage_complex_words(self):
        # complex_words_list = []
        complex_words_count = 0
        for word in self.words:
            if self.is_complex_word(word):
                # complex_words_list.append(word)
                complex_words_count += 1
        return (complex_words_count / len(self.words)) * 100

    def fog_index(self):
        average_sentence_length = self.average_sentence_length()
        percentage_complex_words = self.percentage_complex_words()
        return 0.4 * (average_sentence_length + percentage_complex_words)

    def is_complex_word(self, word):
        count = self.syllable_count_per_word(word)
        if count > 2:
            return True
        else:
            return False
            

    def complex_word_count(self):
        complex_words_count = 0
        for word in self.words:
            if self.is_complex_word(word):
                complex_words_count += 1
        return complex_words_count

    def word_count(self):
        filtered_words_count = 0
        for word in self.words:
            if word.lower() not in self.stop_words and word not in string.punctuation:
                filtered_words_count += 1
        return filtered_words_count

    def syllable_count_per_word(self, word):
        word = word.lower()
        syllable_count = 0
        vowels = 'aeiouy'
        if word[0] in vowels: #common rule that assumes a word starting with a vowel contributes at least one syllable.
            syllable_count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index -1] not in vowels:
                syllable_count += 1
        # if word.endswith('e'): #common adjustment since silent 'e' at the end of a word is often not pronounced.
        #     syllable_count -= 1
        for exception in self.syllables_exceptions:
            if word.lower().endswith(exception):
                syllable_count -= 1
        if syllable_count == 0:# and word not in string.punctuation: #minimum syllable count is 1
            syllable_count += 1
        
        return syllable_count
    
    def total_syllables_counts(self):
        sum = 0
        for word in self.words:
            sum += self.syllable_count_per_word(word)
        return sum

    def personal_pronouns_count(self):
        pronouns = ["I", "we", "We", "my", "ours", "us"]
        pronoun_count = 0
        for word in self.words_0:
            if word in pronouns:
                pronoun_count += 1
        return pronoun_count
    '''     alternative code for pronouns
        count = 0
        pronouns = ['i', 'we', 'my', 'ours', 'us']
        for word in self.words_0:
            if word == 'US':
                pass
            elif word.lower() in pronouns:
                count += 1
        return count 
'''

    def average_word_length(self):
        total_characters = 0
        for word in self.words:
            total_characters += len(word)

        return total_characters / len(self.words)
    
#------------------End of Text Analysis Class-------------------------------------


def read_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        return file.read()


df = pd.read_excel('Input.xlsx')  

folder_path = 'extracted_articles'

for index, row in df.iterrows():
    file_name = row['URL_ID'] + '.txt'
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        text = read_file(file_path)

        sentiment_analysis = SentimentAnalysis()
        cleaned_tokens = sentiment_analysis.clean_text(text)
        pos_score, neg_score, pol_score, subj_score = sentiment_analysis.calculate_sentiment_scores(cleaned_tokens)

        t_analysis = TextAnalysis(text)
        
        df.at[index, 'POSITIVE SCORE'] = pos_score
        df.at[index, 'NEGATIVE SCORE'] = neg_score
        df.at[index, 'POLARITY SCORE'] = pol_score
        df.at[index, 'SUBJECTIVITY SCORE'] = subj_score
        df.at[index, 'AVG SENTENCE LENGTH'] = t_analysis.average_sentence_length()
        df.at[index, 'PERCENTAGE OF COMPLEX WORDS'] = t_analysis.percentage_complex_words()
        df.at[index, 'FOG INDEX'] = t_analysis.fog_index()
        df.at[index, 'AVG NUMBER OF WORDS PER SENTENCE'] = t_analysis.average_sentence_length()
        df.at[index, 'COMPLEX WORD COUNT'] = t_analysis.complex_word_count()
        df.at[index, 'WORD COUNT'] = t_analysis.word_count()
        df.at[index, 'SYLLABLE PER WORD'] = t_analysis.total_syllables_counts()/ t_analysis.word_count()
        df.at[index, 'PERSONAL PRONOUNS'] = t_analysis.personal_pronouns_count()
        df.at[index, 'AVG WORD LENGTH'] = t_analysis.average_word_length()


df.to_excel('Output Data Structure.xlsx', index=False)
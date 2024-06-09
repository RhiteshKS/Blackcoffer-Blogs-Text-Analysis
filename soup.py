import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import string

nltk.download('punkt')
nltk.download('stopwords')

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
        # stop_words = set(stopwords.words('english'))
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

file_path = 'blackassign0001.txt'  # Replace with your file path

with open(file_path, 'r') as file:
    text = file.read()

analysis = TextAnalysis(text)

print("Average Sentence Length:", analysis.average_sentence_length())
print("Percentage of Complex Words:", analysis.percentage_complex_words())
print("Fog Index:", analysis.fog_index())
print("Complex Word Count:", analysis.complex_word_count())
print("Word Count:", analysis.word_count())
print("Personal Pronouns Count:", analysis.personal_pronouns_count())
print("Average Word Length:", analysis.average_word_length())


# for word in analysis.words:
#     print(f"Syllable Count in '{word}':", analysis.get_syllable_count_per_word(word))
print("Number of Syllables per word:", analysis.total_syllables_counts()/ analysis.word_count())
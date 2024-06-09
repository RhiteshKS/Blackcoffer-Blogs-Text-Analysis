## Requirements : 
nltk, re, beautiful soup, pandas, requests, lxml(if needed)

## Instructions to run:
* Make sure to maintain the structure of the folders. When downloaded, the analysis.py, Input.xlsx, MasterDictionary, StopWords folders should be in the same directory.

* In Linux:

* create a virtual environment

```
cd ~
python3 -m venv myenv
```
* activate it
```
source myenv/bin/activate
```
* Using pip, install all required modules.

* to run the code,
```
python3 analysis.py
```

# Flow of code:
1. First 'extracted_articles' folder will be created. And inside it, there will be 98 text files with names as their respective URL_IDs with the title and the text scraped from their respective URLs.

    __2 URL_IDs, blackassign0036, blackassign0049, show 404 error code and therfore no text is extracted from them and therefore no analysis is performed on them__.

2. After performing the required analysis on each text file, its output will be written onto the 'Output Data Structure.xlsx' sheet.

# Sentiment Analysis
* For calculating the positive, negative, polarity and subjectivity score, preprocessing using MasterDictionary and Stopwords was done.

# Text Analysis

### Preprocessing
* Used 2 words corpus, with different preprocessing techniques, words_0 and words.
* 'words_0' are just tokenized into words without doing it in lowercase which will help for finding the pronouns which are also stopwords in the english language and also differentiate between pronoun 'us' and the country, 'US'. 
* And 'words' which is used everywhere else is with stopwords and punctuations removed to calculate word length, complex words etc. 

### Syllabus Counting
* It is not clear if for syllables counting, stopwords are allowed or not. If they are, each will account for one syllable increase in the total. I will assume that stopwords are not counted.
* Have assumed numeric values as having a standard single syllable count.
* For syllable counting, there are many exceptions like the silent 'e' in the end. When it is in the end, it is not counted as syllable, eg in 'increase', it is counted as having 2 syllables, inc + rease, but in the case of 'people' if we follow the same logic, the syllable count becomes 1 instead of the correct result being 2, as in peo + ple. 
* I have commented it for now, so it will count words ending in e, which is silent, also as a syllable. so the syllable count of 'increase' will be shown as 3 instead of 2, while 'people' will get the correct syllable count as 2.
* A better approach would be to make a list of all words ending with e which is silent, and applying a different rule for it. But it is a lengthy and cumbersome process.

### Average sentence length
* average sentence length and the average number of words per sentence mean the same thing and only one function is used for it.



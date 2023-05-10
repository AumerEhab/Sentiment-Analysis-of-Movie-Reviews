import glob
import os
import string
import re
import pandas as pd
from nltk import pos_tag
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

def apply_lemmatization(data):
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N": wordnet.NOUN, "V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}
    lemmatized_sentences = []
    for sent in data['review']:
        lemmatized_sent = []
        for subsent in sent:
            pos_text = pos_tag(subsent.split())
            lemmatized_sent.append(
                " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_text]))
        lemmatized_sentences.append(lemmatized_sent)
    return lemmatized_sentences


def apply_stemming(data):
    stemmer = PorterStemmer()
    stemming_sentences = []
    for sent in data['review']:
        stemmed_sent = []
        for subsent in sent:
            stemmed_sent.append(" ".join([stemmer.stem(word) for word in subsent.split()]))
        stemming_sentences.append(stemmed_sent)
    return stemming_sentences


def sentence_tokenizing(data):
    tokenized = []
    for sent in data['review']:
        tokenized.append(sent_tokenize(sent))
    return tokenized


def filtering_stop_words(data):
    stop_words = set(stopwords.words('english'))
    # remove specific words from the set
    stop_words.discard('not')
    stop_words.discard('no')
    filtered_content = []
    for row in data['review']:
        filtered_sent = []
        for sent in row:
            filtered_sentence = [word for word in sent.split() if word.casefold() not in stop_words]
            filtered_sent.append(' '.join(filtered_sentence))
        filtered_content.append(filtered_sent)

    return filtered_content


def pos_tagging(df):
    pos_sentences = []
    for sent in df['review']:
        tages = []
        for subsent in sent:
            pos_sentence = pos_tag(subsent.split())
            tages.append(pos_sentence)
        pos_sentences.append(tages)
    return pos_sentences


def to_lowercase(data, target):
    data[target] = data[target].str.lower()
    return data


def read_data(dir):
    X, Y = [], []

    folders = ["pos", "neg"]
    for folder in folders:
        path = os.path.join(dir, folder, "*")
        sentiment = [1] if folder == "pos" else [0]

        for file in glob.glob(path, recursive=False):
            with open(file, "r") as f:
                file_content = f.read()
            X.append(file_content)
            Y.append(sentiment)

    return X, Y


def remove_punct(df, target):
    contractions = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "couldn't": "could not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it's": "it is",
        "let's": "let us",
        "mustn't": "must not",
        "shan't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "shouldn't": "should not",
        "that's": "that is",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "we'd": "we would",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "where's": "where is",
        "who'll": "who will",
        "who's": "who is",
        "won't": "will not",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have"
    }
    for contraction, expansion in contractions.items():
        df[target] = df[target].str.replace(contraction, expansion)
    for char in string.punctuation:
        if char != '.':
            df[target] = df[target].str.replace(char, '')

    return df


def get_data(dir):
    X, y = read_data(dir)
    df = pd.DataFrame({"review": X, "sentiment": y})
    return df

    # define a set of stopwords


df = get_data(r"C:\Users\Karim\Desktop\txt_sentoken")

# df = pd.DataFrame(df)

df = to_lowercase(df, 'review')

df = remove_punct(df, "review")
print(df['review'][2])

# 1. tokenize our data
df['review'] = sentence_tokenizing(df)
# print(df['review'][1])

# # 2. stop word removing
df['review'] = filtering_stop_words(df)
# print(df['review'][1])


# # 3. pos tagging
# df['review'] = pos_tagging(df)
# print(df['review'][0])

# # 4. Stemming
# df['review'] = apply_stemming(df)
# print(df['review'][0])

# # 5. lemmitization
df['review'] = apply_lemmatization(df)
# print(df['review'][1])


# df_train, df_test = train_test_split(df, test_size=0.2)
# X_train, Y_train = df_train["review"], df_train["sentiment"]
# X_test, Y_test = df_test["review"], df_test["sentiment"]


## removing all numbers in the dataset
## asking the TA about the stemming
## asking the TA about running the code

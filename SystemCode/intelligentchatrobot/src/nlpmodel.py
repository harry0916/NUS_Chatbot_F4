import spacy as sp
import nltk
from nltk import ngrams
from textblob import TextBlob
import string
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os

class NlpModel(object):

    def __init__(self):
        # SpaCy setup
        self.nlp = sp.load("en_core_web_md")
        # Env Variables
        self.dir_path = os.path.dirname(os.path.abspath(__file__)) +"/../data/nightSafariFAQs.txt"
        with open(self.dir_path, 'r') as f:
            raw = f.read()
        # preprocessing
        self.raw = raw.lower()  # converts to lowercase
        nltk.download('punkt')  # first-time use only
        nltk.download('wordnet')  # first-time use only
        self.sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        self.word_tokens = nltk.word_tokenize(raw)  # converts te list of words
        #sent_tokens[0]
       # word_tokens[0:10]

        # lemmatization
        self.lemmer = nltk.stem.WordNetLemmatizer()

    def LemTokens(self, tokens):
        lemmer = nltk.stem.WordNetLemmatizer()
        return [lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        return self.LemTokens(
            nltk.word_tokenize(text.lower().translate(remove_punct_dict))
        )

    def get_ngrams(self, text, n=3):
        tokens = self.LemTokens(text)
        ng = set(ngrams(tokens, n))
        return ng

    def get_paragraphs(self, raw_text):
        paragraphs = [
            para.strip().lower()
            for para in raw_text.split("\n\n")
            if len(para.strip()) > 0
        ]

        return paragraphs

    def compute_jaccard_sim(self, question, sentence, n=2):
        if len(self.LemTokens(question)) < n or len(self.LemTokens(sentence)) < n:
            return 0
        else:
            question_ngram = self.get_ngrams(question, n)
            sentence_ngram = self.get_ngrams(sentence, n)
            similarity = len(question_ngram.intersection(sentence_ngram)) / len(
                question_ngram.union(sentence_ngram)
            )
        return similarity

    def get_relevant_paragraphs(self, paragraphs, question, n=4):

        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words="english")
        paragraphs.append(question[0])
        tfidf = TfidfVec.fit_transform(paragraphs)
        vals = cosine_similarity(tfidf[-1], tfidf)
        ids = vals.flatten().argsort()[-n:-1][::-1]

        return [paragraphs[idx] for idx in ids]

    def get_relevant_sentences(self, paragraphs, question):
        sentences = [
            sentence.raw for para in paragraphs for sentence in TextBlob(para).sentences
        ]

        print("\nSENTENCES\n=============================================\n")
        for sent in sentences:
            print(sent)
            print(self.compute_jaccard_sim(question, sent))
            print()
        sim_score = np.array(
            [self.compute_jaccard_sim(question, sent, n=3) for sent in sentences]
        )
        ids = sim_score.flatten().argsort()[-3:][::-1]

        return [sentences[idx] for idx in ids]


    def get_answer(self, sentences):
        answer = None
        parsed_sentences = [self.nlp(sent) for sent in sentences]
        noun_chunks = [
            chunk
            for parsed_sent in parsed_sentences
            for chunk in parsed_sent.noun_chunks
        ]
        temp = []
        for sent in parsed_sentences:
            for ent in sent.ents:
                    temp.append(ent.text)
        answer = ", ".join(temp)
        print('answer,', answer)

    def query(self, question):

        #print(self.raw)
        paragraphs = self.get_paragraphs(self.raw)
        relevant_paras = self.get_relevant_paragraphs(paragraphs, question)
        print("\nRELEVANT PARAGRAPHS\n==================================================\n")
        for para in relevant_paras:
            print(para)
            print("\n")
        relevant_sentences = self.get_relevant_sentences(relevant_paras, question)
        self.get_answer(relevant_sentences)

    # match input to the preprocessed sentences
    def response(self,user_response):
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if not req_tfidf:
            robo_response += "I am sorry! I don't understand you."
        else:
            robo_response += self.sent_tokens[idx]
        self.sent_tokens.remove(user_response)
        return robo_response

    @staticmethod
    def parse_text(filename):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        fp = open(filename)
        data = fp.read()
        sentences = tokenizer.tokenize(data)
        sentences = [si for si in sentences if "\n" not in si]
        sentences = [s.encode('ascii', 'ignore') for s in sentences]
        return sentences

    @staticmethod
    def easy_find(text):
        return process.extractOne(text, NlpModel.parse_text('data/nightSafariFAQs.txt'), scorer=fuzz.token_sort_ratio)[0]


if __name__ == "__main__":
    nlp = NlpModel()
    for i in range(10):
        a=nlp.response('Can I bring food into the park')
        print('output:',a)
    print("<<<<<")

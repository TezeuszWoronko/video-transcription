import re
import json
import nltk
import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer


class TranscriptionEvaluator:

    def __init__(self, keyword_dict):
        nltk.download('stopwords')
        nltk.download('punkt')

        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.keywords = set([self.stemmer.stem(word.lower())
                             for word in keyword_dict])
        self.word_pattern = re.compile(r'\w+')

    def _preprocess_text(self, text):
        word_tokens = word_tokenize(text.lower())

        filtered_sentence = []
        for word in word_tokens:
            if word not in self.stop_words and bool(self.word_pattern.match(word)):
                filtered_sentence.append(word)

        stemmed_words = [self.stemmer.stem(word) for word in filtered_sentence]
        return stemmed_words

    def _evalute_preprocessed_words(self, words):
        return sum(word in self.keywords for word in words)

    def analyze(self, transcription):
        stemmed_words = self._preprocess_text(transcription)
        common_keywords = set(stemmed_words).intersection(self.keywords)
        return self._evalute_preprocessed_words(stemmed_words), common_keywords


def process_transcription(start_datetime, transcription_path):

    with open(transcription_path, 'r') as f:
        transcription_results = json.load(f)
    with open('keyword_dict.json', 'r') as f:
        keyword_dict = json.load(f)

    results = []
    evaulator = TranscriptionEvaluator(keyword_dict)
    for transcription in transcription_results:
        value, keywords = evaulator.analyze(transcription['text'])
        timestamp = start_datetime + \
            datetime.timedelta(0, 0, transcription['time']*1000)
        results.append({
            "text": transcription['text'],
            "time": str(timestamp),
            "offset": transcription['time'],
            "keywords": list(keywords),
            "value": value
        })

    return results


if __name__ == "__main__":
    output_path = 'output.json'
    start_datetime = datetime.datetime(2019, 10, 19, 11, 20, 0, 0)
    transcription_path = 'transcriptions/Tesla may have more bad news on the horizon_ Analyst 0s - 30s (t3wAEDP6P3E).json'
    results = process_transcription(
        start_datetime, 
        transcription_path
    )

    with open(output_path, 'w') as f:
        f.write(json.dumps(results))
 
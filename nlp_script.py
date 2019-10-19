import re
import json
import nltk
import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')
nltk.download('punkt')

input_json_path = "./analysts.json" 
out_path = "./analysts_counted.json"
target_words = ["Tesla", "Musk"]
start_datetime = datetime.datetime(2019, 10, 19, 11, 20, 0, 0)

def remove_stop_and_punctation (input_text):
    
    input_text = input_text.lower()
    
    p = re.compile(r'\w+')

    stop_words = set(stopwords.words('english')) 
  
    word_tokens = word_tokenize(input_text) 
  
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
    filtered_sentence = [] 
  
    for w in word_tokens: 
        if w not in stop_words and bool(p.match(w)): 
            filtered_sentence.append(w) 
  
    return(filtered_sentence)
    
def stem_words (input_text):
    ps = PorterStemmer()

    stemmed_sentence = []

    for word in input_text:
        stemmed_sentence.append(ps.stem(word))
    
    return(stemmed_sentence)

def calculate_words_nr (stemmed_text, target_words):
    
    target_words = [word.lower() for word in target_words]
    stemmed_words = stem_words(target_words)
    
    words_nr = sum(word in stemmed_words for word in stemmed_text)
    
    return(words_nr)

def convert_stamps_to_datetime (start_datetime, stamp):
    # stamps in milisec
    stamp = 8196
    stamp_us = stamp * 1000

    tst_datetime = start_datetime + datetime.timedelta(0,0, stamp_us)
    tst_datetime = tst_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    return(tst_datetime)

def count_words_in_json (json_path, target_words, start_datetime, out_path):

    with open(json_path) as fhandler:
    
        parsed_json = json.load(fhandler)
        
    for obj in parsed_json:
        text = obj['text']
        text = remove_stop_and_punctation(text)
        text = stem_words(text)
        words_nr = calculate_words_nr(text, target_words)
        stamp_datetime = convert_stamps_to_datetime(start_datetime, obj['time'])
    
        obj['text'] = obj['text']
        obj['text_clean'] = text
        obj['time'] = stamp_datetime
        obj['words_nr'] = words_nr
    
    with open(out_path, "w") as fhandler:
    
        json.dump(parsed_json, fhandler)
        
    return(parsed_json)

new_json = count_words_in_json(input_json_path, target_words, start_datetime)

    


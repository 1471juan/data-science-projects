###############################
#Exercise word classification
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold

alphabet = "abcdefghijklmnopqrstuvwxyzäö-"

def load_finnish():
    with open("data/words_finnish.txt", "r", encoding="utf-8") as f:
        text = f.read()
    # Remove quotes and whitespace, then split by commas
    words = [w.strip().strip('"') for w in text.split(",") if w.strip()]
    return words

def load_english():
    with open("data/words_english.txt", "r", encoding="utf-8") as f:
        text = f.read()
    # Remove quotes and whitespace, then split by commas
    words = [w.strip().strip('"') for w in text.split(",") if w.strip()]
    return words

def get_features(words: np.ndarray) -> np.ndarray:
    features = np.zeros((len(words), len(alphabet)), dtype=int)
    i=0
    while i<len(words):
        for char_w in words[i]:
            for j in range(len(alphabet)):
                if alphabet[j]==char_w:
                    features[i,j] += 1
                    break
        i+=1
    return features

def contains_valid_chars(text: str):
    for char in text:
        if char in alphabet:
            pass
        else: return False
    return True

def lowercase_array(array):
    array_transformed=[]
    for i, w in enumerate(array):
        array_transformed.append(w.lower())
    return array_transformed

def isFirstCharacterUppercase(word:str):
    if word[0].isupper(): return True
    else: return False

def get_features_and_labels():
    finnish_words = load_finnish()
    english_words = load_english()
    #FINNISH
    words_f = [w for w in lowercase_array(finnish_words) if contains_valid_chars(w)]
    #ENGLISH
    words_e = [w for w in english_words if not isFirstCharacterUppercase(w)]
    words_e = lowercase_array(words_e)
    words_e = [w for w in words_e if contains_valid_chars(w)]
    
    #Concatenate the arrays
    words_array = np.concatenate((np.array(words_f), np.array(words_e)))
    #Get features
    X = get_features(words_array)
    #Get Labels
    y=np.zeros(len(words_array), dtype=int)
    y[len(words_f):]=1

    return X, y

def word_classification(method=1):
    X,y= get_features_and_labels()
    model = MultinomialNB()
    if(method==1):
        scores = cross_val_score(model, X, y, cv=5)  # cross val
        return scores
    else:
        kf = KFold(n_splits=5, shuffle=True, random_state=0)
        scores = cross_val_score(model, X, y, cv=kf)
        return scores

print(word_classification(0))
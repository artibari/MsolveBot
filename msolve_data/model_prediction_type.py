import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
from sklearn.feature_extraction.text import *
from numpy import array
import re
nltk.download('wordnet')

### Reading the data 
df = pd.read_csv("D:\\NEW MSOLVE\\msolve_data\\training.csv",,sep='\s*,\s*',
                           header=0, engine='python')
						   
##print(df.head())
df.columns
X = df['issue']
y = df['type']

## Convert the issue into list
issues = issues.tolist()

## Remove the punctuations
Issue =[]
for i in issues:
    text = re.sub(r'[-]',"",i)
    Issue.append(text)
##print(Issue)

## String convert into word tokenize
tokens =[]
for words in Issue:
    word = word_tokenize(words)
    #print(word)
    tokens.append(word)
    #tokens.append(word_tokenize[words])
print(tokens)

## Removes the stop words 
no_stopword=[]
stop_word = stopwords.words('english')
#stop_word
for k in tokens:
    sw=[]
    for x in k:
        if x.lower() not in stop_word:
            sw.append(x)
    no_stopword.append(sw)
print(no_stopword)


### lemmatization 
lem=[]
lemmatizer = WordNetLemmatizer()
for word in no_stopword:
    lem_word=[]
    for l_word in word:
        word_lemmatizer=lemmatizer.lemmatize(l_word)
        #l_wr = "".join(word_lemmatizer)
        lem_word.append(word_lemmatizer.lower())
    iss = " ".join(lem_word)
    lem.append(iss)
print(lem)

## Vectorization of data
countVal = TfidfVectorizer().fit(lem)
a = countVal.transform(lem)
b = df.iloc[:,2].values
pickle.dump(countVal,open("TFIDF_pickle_ver2","wb"),protocol=2)

## Train the model 
X_train, X_test, y_train, y_test =train_test_split(a, b,test_size=0.01, random_state=42)
classifier= LinearSVC()
classifier.fit(X_train, y_train)
data = classifier
pickle.dump(classifier ,open("model_pickle_ver2","wb"),protocol=2)

## Predict the model
with open("TFIDF_pickle_ver2" ,"rb") as tf:
    tdf = pickle.load(tf)
    pre = tdf.transform(["LSMW transaction"])
with open("model_pickle_ver2","rb") as mod:
     model= pickle.load(mod)
     pred = model.predict(pre)
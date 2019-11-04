import sys
sys.path.insert(0, '/var/www/html')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
# import pandas as pd
# import numpy as np
import json
from bucket_extractor import *
from sent_similarity import *

stop_words = set(stopwords.words('english'))

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def get(input_statement):
    closest_statement = ""
    closest_similarity = 0

    print("INSIDE NEAREST MEANING.............{}".format(input_statement))
    # training_data_frame = pd.read_csv("/var/www/html/training_data.csv")
    # train_set = training_data_frame["documents"].tolist()

    with open("D:\\NEW MSOLVE\\msolve_data\\training_data.csv") as f:
        train_set = [i[0] for i in csv.reader(f)]

    bucket_token,sub_bucket,keyword_in_input,transformed_input = extract_buckets(input_statement)
    transformed_input = " ".join([w for w in word_tokenize(transformed_input) if w not in stop_words])

    with open("/var/www/html/buckets.json") as bucket_file:
        bucketData = json.load(bucket_file)

    bucket_list = bucketData["bucket_priority_list"]

    def check_bucket_token(string,token):
        string_tokens = string.split(" ")
        bucket_list.remove(token)
        for i in bucket_list:
            if i in string_tokens and (i not in bucketData["sub_bucket_priority_list"]):
                bucket_list.append(token)
                return False
        bucket_list.append(token)        
        return True

    for statement in train_set:
        if len(keyword_in_input) == 1:
            check_token = check_bucket_token(statement,bucket_token)
            if findWholeWord(bucket_token)(statement) and findWholeWord(sub_bucket)(statement) and check_token:
                similarity = jac_sim(transformed_input.lower(), statement.lower())
                if similarity > closest_similarity :
                    closest_similarity = similarity
                    closest_statement = statement
        else:
            if findWholeWord(bucket_token)(statement) and findWholeWord(sub_bucket)(statement):
                similarity = jac_sim(transformed_input.lower(), statement.lower())
                if similarity > closest_similarity :
                    closest_similarity = similarity
                    closest_statement = statement

    if not closest_statement and bool(sub_bucket) is True:
        for statement in train_set:
            if findWholeWord(bucket_token)(statement):
                similarity = jac_sim(transformed_input.lower(), statement.lower())
                if similarity > closest_similarity :
                    closest_similarity = similarity
                    closest_statement = statement

    return closest_statement

#!/usr/bin/env python3
import re
import pdb
import json 
import math

import csv

# used for text classification. 
from pycorenlp import StanfordCoreNLP
from textblob.classifiers import NaiveBayesClassifier

DATA_FILE = "data_training.csv" 

def calculate_performace(TP, FP, TN, FN):
    beta = 1

    total = TP + FP + TN + FN
    accuracy = (TP + TN) / total
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f_score = 2 * precision * recall / (precision + recall)

    print("TP: {}, FP: {}, TN: {}, FN: {}".format(TP, FP, TN, FN))

    print("| {} | {} | {} | {} |".format(accuracy, precision, recall, f_score))


def get_core_obj():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return nlp



def main(nlp):
    dataset = []
    with open(DATA_FILE) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            res = ""
            annotated_text = nlp.annotate(row[0], properties = {
                'annotators': 'pos',
                'outputFormat': 'json'
            })

            if len(annotated_text['sentences']) > 1:
                print("WEIRD SHIT HAPPENING")
                continue

            for item in annotated_text['sentences'][0]['tokens']:
                res += item['word'] + " " + item['pos']

            dataset.append({
                "sentence": res,
                "label": row[1]
            })


    # dividing the dataset into two pos and neg parts
    pos_all = [{'sentence': item['sentence'], 'label': 'pos'} for item in dataset if item['label'] == "1"]
    neg_all = [{'sentence': item['sentence'], 'label': 'neg'} for item in dataset if item['label'] == "0"]

    # building the trainset from the entire dataset
    pos_train = pos_all[:math.floor(len(pos_all)/5) * 4]
    neg_train = neg_all[:math.floor(len(neg_all)/5) * 4]
    train_set =  pos_train + neg_train

    # preparing train_set to be fed to the classifier
    train_set = [(item['sentence'], item['label']) for item in train_set]


    # preparing the test set
    pos_test = pos_all[math.floor(len(pos_all)/5) * 4:]
    neg_test = neg_all[math.floor(len(neg_all)/5) * 4:]
    test_set = pos_test + neg_test


    print("Train set: {}, Pos train: {}, Neg train : {}".format(len(train_set), len(pos_train), len(neg_train)))
    print("Test set: {}, Pos test: {}, Neg test: {}".format(len(test_set), len(pos_test), len(neg_test)))

    # pdb.set_trace()


    # training the classifier
    model = NaiveBayesClassifier(train_set)

    correct = 0
    TP = 0
    TN = 0
    FP = 0
    FN = 0


    for item in test_set:
        classification = model.classify(item['sentence'])
        if classification == item['label']:
            if classification == "pos":
                TP += 1
            else:
                TN += 1

        else:
            if classification == "pos":
                FP += 1
            else:
                FN += 1


    calculate_performace(TP, FP, TN, FN)


        
if __name__ == "__main__":
    nlp = get_core_obj()
    main(nlp)
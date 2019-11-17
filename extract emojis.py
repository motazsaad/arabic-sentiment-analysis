#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:39:14 2019

@author: xabuka
"""

import emoji
# This regex implementation is backwards-compatible with the standard ‘re’ module, but offers additional functionality.
import regex


def read_tsv(data_file):
    text_data = list()
    labels = list()
    infile = open(data_file, encoding='utf-8')
    for line in infile:
        if not line.strip():
            continue
        label, text = line.split('\t')
        text_data.append(text)
        labels.append(label)
    return text_data, labels


def load_twitter(pos_train_file, neg_train_file, pos_test_file, neg_test_file):
    pos_train_data, pos_train_labels = read_tsv(pos_train_file)
    neg_train_data, neg_train_labels = read_tsv(neg_train_file)

    pos_test_data, pos_test_labels = read_tsv(pos_test_file)
    neg_test_data, neg_test_labels = read_tsv(neg_test_file)
    print('------------------------------------')

    x_pos = list(set(pos_train_data + pos_test_data))
    x_neg = list(set(neg_train_data + neg_test_data))

    print(len(x_pos))
    print(len(x_neg))
    #    print('positive = ',str(len(set(x_pos))))
    #    print('negative = ',str(len(set(x_neg))))
    return x_pos, x_neg


def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list


pos_training = '../../Shami-Sentiment-Analyzer/data/Motaz_corpus/train_Arabic_tweets_positive_20190413.tsv'
neg_training = '../../Shami-Sentiment-Analyzer/data/Motaz_corpus/train_Arabic_tweets_negative_20190413.tsv'

pos_testing = '../../Shami-Sentiment-Analyzer/data/Motaz_corpus/test_Arabic_tweets_positive_20190413.tsv'
neg_testing = '../../Shami-Sentiment-Analyzer/data/Motaz_corpus/test_Arabic_tweets_negative_20190413.tsv'

x_pos, x_neg = load_twitter(pos_training, neg_training, pos_testing, neg_testing)

# line = ["🤔 🙈 me así, se 😌 ds 💕👭👙 hello 👩🏾‍🎓 emoji hello 👨‍👩‍👦‍👦 how are 😊 you today🙅🏽🙅🏽"]
neg = list()
for x in x_neg:
    counter = split_count(x)
    # print(' '.join(emoji for emoji in counter))
    for e in counter:
        neg.append(e)

print(len(list((neg))))

from collections import Counter

print(Counter(neg))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:39:14 2019

@author: xabuka
"""

import emoji
# This regex implementation is backwards-compatible with the standard ‘re’ module, but offers additional functionality.
import regex
from collections import Counter


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


def extract_emo_from_text(text):
    emoji_list = []
    tokens = regex.findall(r'\X', text)
    # print(tokens)
    for word in tokens:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)
    return emoji_list


def extract_emojis(tweets):
    emo = list()
    for tweet in tweets:
        tweet_emos = extract_emo_from_text(tweet)
        emo += tweet_emos
    return emo


pos_file = 'arabic_tweets_tsv/Arabic_tweets_positive_20191104.tsv'
neg_file = 'arabic_tweets_tsv/Arabic_tweets_negative_20191104.tsv'

pos_data, pos_labels = read_tsv(pos_file)
neg_data, neg_labels = read_tsv(neg_file)

# line = ["🤔 🙈 me así, se 😌 ds 💕👭👙 hello 👩🏾‍🎓 emoji hello 👨‍👩‍👦‍👦 how are 😊 you today🙅🏽🙅🏽"]

pos_emos = extract_emojis(pos_data)
neg_emos = extract_emojis(neg_data)

pos_emos_set = set(pos_emos)
neg_emos_set = set(neg_emos)

print('intersection: {}'.format(pos_emos_set.intersection(neg_emos_set)))
print('--------------------------')
print('most freq pos emos')
print(Counter(pos_emos))
print('--------------------------')
print('most freq neg emos')
print(Counter(neg_emos))

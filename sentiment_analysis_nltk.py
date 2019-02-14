import collections
import random
import re
from collections import Counter
from itertools import islice

import nltk
from nltk.metrics.scores import f_measure

arabic_diacritics = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_repeating_char(text):
    # return re.sub(r'(.)\1+', r'\1', text)     # keep only 1 repeat
    return re.sub(r'(.)\1+', r'\1\1', text)  # keep 2 repeat


def process_text(text, grams=False):
    clean_text = remove_diacritics(text)
    clean_text = remove_repeating_char(clean_text)
    if grams is False:
        return clean_text.split()
    else:
        tokens = clean_text.split()
        grams = list(window(tokens))
        grams = [' '.join(g) for g in grams]
        grams = grams + tokens
        return grams


def window(words_seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(words_seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def document_features(document, corpus_features):
    document_words = set(document)
    features = {}
    for word in corpus_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


all_features = list()
texts = list()
data_labels = list()

positive_file = 'arabic_tweets_txt/positive_tweets_arabic_20181207_300.txt'
negative_file = 'arabic_tweets_txt/negative_tweets_arabic_20181207_300.txt'

n_grams_flag = False
min_freq = 13

print('read data ...')
# read positive data
with open(positive_file, encoding='utf-8') as tweets_file:
    for line in tweets_file:
        text_features = process_text(line, grams=n_grams_flag)
        all_features += text_features
        texts.append(text_features)
        data_labels.append('pos')

# read negative data
with open(negative_file, encoding='utf-8') as tweets_file:
    for line in tweets_file:
        text_features = process_text(line, grams=n_grams_flag)
        all_features += text_features
        texts.append(text_features)
        data_labels.append('neg')

print('data size', len(data_labels))
print('# of positive', data_labels.count('pos'))
print('# of negative', data_labels.count('neg'))

tweets = [(t, l) for t, l in zip(texts, data_labels)]
random.shuffle(tweets)
print('sample tweets')
for t in tweets[:10]: print(t)  # see the first 10 instances
print('all words sample')
print(all_features[:20])
print('len(all_words):', len(all_features))
all_features_freq = nltk.FreqDist(w for w in all_features)
print(all_features_freq)
print('sample frequencies')
print(all_features_freq.most_common(20))
print('freq of في', all_features_freq.freq('في'))
print('features frequencies are computed')
thr = min_freq / len(all_features)
print('selecting features')
###################################
# remove features that have frequency below the threshold
my_features = set([word for word in all_features if all_features_freq.freq(word) > thr])
###################################
# my_features = list(all_features_freq)[:3000]  # top 3k features
###################################
print(len(my_features), 'are kept out of', len(all_features))
print('features are selected')
print('------------------------------------')
print('sample features:')
print(list(my_features)[:100])
print('------------------------------------')

print('generating features for documents ...')
feature_sets = [(document_features(d, my_features), c) for (d, c) in tweets]


print('splitting documents into train and test ...')
print('data set size', len(data_labels))
train_percentage = 0.8
splitIndex = int(len(tweets) * train_percentage)
train_set, test_set = feature_sets[:splitIndex], feature_sets[splitIndex:]
y_train = [l for t, l in train_set]
y_test = [l for t, l in test_set]

print('data set:', Counter(data_labels))
print('train:', Counter(y_train))
print('test:', Counter(y_test))

print('training NaiveBayes classifier ...')
classifier = nltk.NaiveBayesClassifier.train(train_set)
print('training is done')

ref_sets = collections.defaultdict(set)
test_sets = collections.defaultdict(set)

for i, (feats, label) in enumerate(test_set):
    ref_sets[label].add(i)
    observed = classifier.classify(feats)
    test_sets[observed].add(i)

print('accuracy:', nltk.classify.accuracy(classifier, test_set))
print('positive f-score:', f_measure(ref_sets['pos'], test_sets['pos']))
print('negative f-score:', f_measure(ref_sets['neg'], test_sets['neg']))


classifier.show_most_informative_features(20)

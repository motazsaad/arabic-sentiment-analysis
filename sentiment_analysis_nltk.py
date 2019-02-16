
import collections
import itertools
import random
import re
import string
from collections import Counter

import nltk
from nltk.metrics.scores import f_measure
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams


def get_n_grams(word_list, n=2):
    my_grams = []
    uni_grams = [word for word in word_list]
    for i in range(2, n + 1):
        my_grams += ngrams(word_list, i)
    grams = ['_'.join(g) for g in my_grams]
    return uni_grams + grams


def pre_process(text):
    my_tokenizer = TweetTokenizer(reduce_len=True)
    text = my_tokenizer.tokenize(text)
    english_punt = list(string.punctuation)
    text = [w for w in text if (w not in english_punt) or (len(w) >= 2)]
    # remove double chars
    text = [re.sub(r'([a-z])\1+', r'\1', w) for w in text]
    # remove double punctuations
    text = [re.sub(r'([^\P{P}-])\1+', r'\1', w) for w in text]
    text = get_n_grams(text, n=2)
    return text


def document_features(document, corpus_features):
    document_words = set(document)
    features = {}
    for word in corpus_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


data = []
data_labels = []

positive_file = 'machine_learning/the_real_life_of_saudi_woman/positive.txt'
negative_file = 'machine_learning/the_real_life_of_saudi_woman/negative.txt'

print('read data ...')
# read positive data
with open(positive_file, encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')
data = data[:2500]
data_labels = data_labels[:2500]
 
# read negative data
with open(negative_file, encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')

data = data[:5000]
data_labels = data_labels[:5000]


print('data size', len(data_labels))
print('# of positive', data_labels.count('pos'))
print('# of negative', data_labels.count('neg'))

label_names = ['negative', 'positive']

dataset = [(t, l) for t, l in zip(data, data_labels)]
random.shuffle(dataset)
# print (dataset[:10])  # see the first 10 instances


# all_features = sum(tweets, [])
all_features = list(itertools.chain.from_iterable(data))
# print(set(all_features.sort())) # check sorted features

# count frequencies
all_features_freq = nltk.FreqDist(all_features)
# print(':( freq:', all_features_freq.freq(':('))
# print(all_features_freq.items())
print('features frequencies are computed')
thr = 3
print('selecting features')
###################################
# remove features that have frequency below the threshold
features_to_remove = set([k for k, v in collections.Counter(all_features_freq).items() if v < thr ])
my_features = set([word for word in  all_features if all_features_freq.freq(word) > thr])
my_features = set([f for f in all_features if f not in features_to_remove])
###################################
# my_features = list(all_features_freq)[:3000]  # top 3k features
###################################
print(len(my_features), 'grams are kept out of', len(all_features))
print('features are selected')

print('generating features for documents ...')
feature_sets = [(document_features(d, my_features), c) for (d,c) in dataset]


print('splitting documents into train and test ...')
print('dataset size', len(data_labels))
train_percentage = 0.8
splitIndex = int(len(dataset) * train_percentage)
train_set, test_set = feature_sets[:splitIndex], feature_sets[splitIndex:]
y_train = [l for t, l in train_set]
y_test = [l for t, l in test_set]

print('dataset:', Counter(data_labels))
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
print('positive f-score:', f_measure(ref_sets['positive'], test_sets['positive']))
print('negative f-score:', f_measure(ref_sets['negative'], test_sets['negative']))
print('neutral f-score:', f_measure(ref_sets['neutral'], test_sets['neutral']))

classifier.show_most_informative_features(20)

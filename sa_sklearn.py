import random
import sys

import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from textutil import *


def load():
    pos_train_file = 'arabic_tweets_tsv/train_pos_20181206_1k.tsv'
    neg_train_file = 'arabic_tweets_tsv/train_neg_20181206_1k.tsv'

    pos_test_file = 'arabic_tweets_tsv/test_pos_20181206_1k.tsv'
    neg_test_file = 'arabic_tweets_tsv/test_neg_20181206_1k.tsv'

    pos_train_data, pos_train_labels = read_tsv(pos_train_file)
    neg_train_data, neg_train_labels = read_tsv(neg_train_file)

    pos_test_data, pos_test_labels = read_tsv(pos_test_file)
    neg_test_data, neg_test_labels = read_tsv(neg_test_file)
    print('------------------------------------')

    sample_size = 2
    print('{} random train tweets (positive) .... '.format(sample_size))
    print(np.array(random.sample(pos_train_data, sample_size)))
    print('------------------------------------')
    print('{} random train tweets (negative) .... '.format(sample_size))
    print(np.array(random.sample(neg_train_data, sample_size)))
    print('------------------------------------')

    x_train = pos_train_data + neg_train_data
    y_train = pos_train_labels + neg_train_labels

    x_test = pos_test_data + neg_test_data
    y_test = pos_test_labels + neg_test_labels

    print('train data size:{}\ttest data size:{}'.format(len(y_train), len(y_test)))
    print('train data: # of pos:{}\t# of neg:{}\t'.format(y_train.count('pos'), y_train.count('neg')))
    print('test data: # of pos:{}\t# of neg:{}\t'.format(y_test.count('pos'), y_test.count('neg')))
    print('------------------------------------')
    return x_train, y_train, x_test, y_test


def do_sa(n, my_classifier):
    my_data = load()
    x_train, y_train, x_test, y_test = my_data
    print('parameters')
    print('n grams:', n)
    print('classifier:', my_classifier.__class__.__name__)
    print('------------------------------------')

    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=5, max_df=0.95,
                                 analyzer='word', lowercase=False,
                                 ngram_range=(1, n))),
        ('clf', my_classifier),
    ])

    pipeline.fit(x_train, y_train)
    feature_names = pipeline.named_steps['vect'].get_feature_names()
    print('features:', )

    y_predicted = pipeline.predict(x_test)

    # Print the classification report
    print(metrics.classification_report(y_test, y_predicted,
                                        target_names=['pos', 'neg']))

    # Print the confusion matrix
    cm = metrics.confusion_matrix(y_test, y_predicted)
    print(cm)
    print('# of features:', len(feature_names))
    print('sample of features:', random.sample(feature_names, 200))


if __name__ == '__main__':
    ngrams = (1, 2, 3)
    classifiers = [LinearSVC(), SVC(), MultinomialNB(),
                   BernoulliNB(), SGDClassifier(), DecisionTreeClassifier(max_depth=5),
                   RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                   KNeighborsClassifier(3)
                   ]
    for alg in classifiers:
        alg_name = alg.__class__.__name__
        for g in ngrams:
            outfile = sys.argv[0][:-2] + '_' + alg_name + '_' + str(g) + '.result'
            sys.stdout = open(outfile, mode='w', encoding='utf-8')
            do_sa(g, alg)

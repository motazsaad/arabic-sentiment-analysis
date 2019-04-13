import collections
import random
import sys
from datetime import datetime

import nltk
from nltk import NaiveBayesClassifier
from nltk.metrics.scores import f_measure, precision, recall

from textutil import *


def do_sa(n, classifier):
    pos_train_file = 'arabic_tweets_tsv/train_pos_20181206_1k.tsv'
    neg_train_file = 'arabic_tweets_tsv/train_neg_20181206_1k.tsv'

    pos_test_file = 'arabic_tweets_tsv/test_pos_20181206_1k.tsv'
    neg_test_file = 'arabic_tweets_tsv/test_neg_20181206_1k.tsv'
    print('data files')
    print('train file (pos)', pos_train_file)
    print('train file (neg)', neg_train_file)
    print('test file (pos)', pos_test_file)
    print('test file (neg)', neg_test_file)
    print('------------------------------------')

    print('parameters')
    min_freq = 5
    print('n grams:', n)
    print('min freq:', min_freq)
    print('------------------------------------')

    print('loading train data ....')
    pos_train_data, pos_train_feat = load_tsv(pos_train_file, n)
    neg_train_data, neg_train_feat = load_tsv(neg_train_file, n)
    print('loading test data ....')
    pos_test_data, pos_test_feat = load_tsv(pos_test_file, n)
    neg_test_data, neg_test_feat = load_tsv(neg_test_file, n)
    print('------------------------------------')

    print('train data info')
    train_data = pos_train_data + neg_train_data
    print('train data size', len(train_data))
    print('# of positive', len(pos_train_data))
    print('# of negative', len(neg_train_data))
    print('------------------------------------')

    sample_size = 100
    print('{} random tweets .... '.format(sample_size))
    print(random.sample(train_data, sample_size))
    print('------------------------------------')

    print('------------------------------------')
    print('test data info')
    test_data = pos_test_data + neg_test_data
    print('test data size', len(train_data))
    print('# of positive', len(pos_test_data))
    print('# of negative', len(neg_test_data))
    print('------------------------------------')

    print('merging all features ... ')
    all_features = pos_train_feat + neg_train_feat + \
                   pos_test_feat + pos_test_feat
    print('len(all_features):', len(all_features))
    print('{} sample features ...'.format(sample_size))
    print(random.sample(all_features, sample_size))
    print('------------------------------------')

    print('compute frequencies')
    all_features_freq = nltk.FreqDist(w for w in all_features)
    print(all_features_freq)
    print('sample frequencies')
    print(all_features_freq.most_common(20))
    word = 'في'
    print('freq of word {} is {}'.format(word, all_features_freq.freq('في')))
    print('features frequencies are computed')
    print('------------------------------------')
    thr = min_freq / len(all_features)
    print('threshold:', thr)
    print('selecting features ...')
    ###################################
    # remove features that have frequency below the threshold
    my_features = set([word for word in all_features if all_features_freq.freq(word) > thr])
    ###################################
    # other method: top 3k features
    # my_features = list(all_features_freq)[:3000]
    ###################################
    print(len(my_features), 'are kept out of', len(all_features))
    print('features are selected')
    print('------------------------------------')
    print('{} sample of selected features:'.format(sample_size))
    print(random.sample(list(my_features), sample_size))
    print('------------------------------------')

    print('generating features for training documents ...')
    feature_sets = [(document_features(d, my_features), c) for (d, c) in train_data]

    print('------------------------------------')
    print('training ...')
    classifier.train(feature_sets)
    print('classifier: {}'.format(classifier.__class__.__name__))
    print('training is done')
    print('------------------------------------')
    if 'Naive' in classifier.__class__.__name__:
        classifier.show_most_informative_features(40)
    if 'DecisionTree' in classifier.__class__.__name__:
        print('Decision Tree:')
        print(classifier)
    print('------------------------------------')

    print('generating features for test documents ...')
    test_features = [(document_features(d, my_features), c) for (d, c) in test_data]

    ref_sets = collections.defaultdict(set)
    test_sets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(test_features):
        ref_sets[label].add(i)
        observed = classifier.classify(feats)
        test_sets[observed].add(i)
    print('test results:')
    print('accuracy: ', nltk.classify.accuracy(classifier, test_features))
    print('pos precision: ', precision(ref_sets['pos'], test_sets['pos']))
    print('pos recall:', recall(ref_sets['pos'], test_sets['pos']))
    print('neg precision: ', precision(ref_sets['neg'], test_sets['neg']))
    print('neg recall:', recall(ref_sets['neg'], test_sets['neg']))
    print('positive f-score:', f_measure(ref_sets['pos'], test_sets['pos']))
    print('negative f-score:', f_measure(ref_sets['neg'], test_sets['neg']))


if __name__ == '__main__':
    time_stamp = datetime.now().strftime('%Y%m%d_%H%M')
    ngrams = (1, 2, 3)
    # algorithms = [NaiveBayesClassifier, DecisionTreeClassifier]
    algorithms = [NaiveBayesClassifier]
    for alg in algorithms:
        for n in ngrams:
            time_stamp = '_'
            alg_name = alg.__class__.__name__
            outfile = sys.argv[0][:-2] + time_stamp + '_' + alg_name + '_' + str(n) + '.result'
            sys.stdout = open(outfile, mode='w', encoding='utf-8')
            do_sa(n, alg)

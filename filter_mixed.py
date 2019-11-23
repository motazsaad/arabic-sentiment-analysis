import emoji
# This regex implementation is backwards-compatible with the standard ‘re’ module, but offers additional functionality.
import regex
from collections import Counter
import random


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
    for word in tokens:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)
    return emoji_list


def load_lexicon(lex_file):
    emoji_lex = open(lex_file, encoding='utf-8').read().split('\n')
    return emoji_lex


def check_emo_in_lex(emos, lex):
    return any([emo in lex for emo in emos])


def label_mix(pos_data, neg_data):
    new_pos = list()
    new_neg = list()
    mixed = list()
    all_tweets = list()
    for tweet in pos_data:
        emojis = extract_emo_from_text(tweet)
        if check_emo_in_lex(emojis, pos_lex) and check_emo_in_lex(emojis, neg_lex):
            mixed.append(tweet)
        else:
            new_pos.append(tweet)
    for tweet in neg_data:
        emojis = extract_emo_from_text(tweet)
        if check_emo_in_lex(emojis, pos_lex) and check_emo_in_lex(emojis, neg_lex):
            mixed.append(tweet)
        else:
            new_neg.append(tweet)
    print('after:', 'pos', len(new_pos), 'neg', len(new_neg), 'mix', len(mixed))
    for tweet in new_pos:
        all_tweets.append('pos\t' + tweet)
    for tweet in new_neg:
        all_tweets.append('neg\t' + tweet)
    for tweet in mixed:
        all_tweets.append('mix\t' + tweet)
    random.shuffle(all_tweets)
    return all_tweets


def write_tsv(outfile_name, tweets):
    outfile = open(outfile_name, encoding='utf-8', mode='w')
    for tweet in tweets:
        outfile.write(tweet + '\n')


pos_lex = load_lexicon('emoji_lex/positive_emoji_v3.txt')
neg_lex = load_lexicon('emoji_lex/negative_emoji_v3.txt')
print(len(pos_lex), len(neg_lex))

##############################################
pos_file = 'arabic_tweets_tsv/20191104/Arabic_tweets_positive_20191104.tsv'
neg_file = 'arabic_tweets_tsv/20191104/Arabic_tweets_negative_20191104.tsv'
pos_data, pos_labels = read_tsv(pos_file)
neg_data, neg_labels = read_tsv(neg_file)
print('before:', 'pos', len(pos_data), 'neg', len(neg_data))

all_tweets = label_mix(pos_data, neg_data)
outfile_name = 'arabic_tweets_tsv/20191104/3labels/Arabic_tweets_20191104.tsv'
write_tsv(outfile_name, all_tweets)
###########################################


pos_file = 'arabic_tweets_tsv/20190413/Arabic_tweets_positive_20190413.tsv'
neg_file = 'arabic_tweets_tsv/20190413/Arabic_tweets_negative_20190413.tsv'
pos_data, pos_labels = read_tsv(pos_file)
neg_data, neg_labels = read_tsv(neg_file)
print('before:', 'pos', len(pos_data), 'neg', len(neg_data))

all_tweets = label_mix(pos_data, neg_data)
outfile_name = 'arabic_tweets_tsv/20190413/3labels/Arabic_tweets_20190413.tsv'
write_tsv(outfile_name, all_tweets)

spam = open('spam_lexicon.txt', encoding='utf-8').read().split('\n')
spam = [word for word in spam if word.strip()]


def has_spam(tweet):
    for word in spam:
        if word in tweet:
            return True
    return False


def filter_tweets(infile, outfile, label):
    outfile = open(outfile, encoding='utf-8', mode='w')
    tweets = open(infile, encoding='utf-8').read().split('\n')
    for tweet in tweets:
        if not tweet.strip():
            continue
        if has_spam(tweet):
            continue
        outfile.write(label + '\t' + tweet + '\n')


if __name__ == '__main__':
    filter_tweets('arabic_tweets_txt/positive_tweets_arabic_20181206_1k.txt',
                  'arabic_tweets_tsv/pos_20181206_1k.tsv', 'pos')
    filter_tweets('arabic_tweets_txt/negative_tweets_arabic_20181206_1k.txt',
                  'arabic_tweets_tsv/neg_20181206_1k.tsv', 'neg')
    print('all done')

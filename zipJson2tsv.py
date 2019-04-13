import json
import zipfile

import preprocessor as tweet_processor

from filter_tweets import *
from textutil import *

tweet_processor.set_options(tweet_processor.OPT.URL,
                            tweet_processor.OPT.MENTION,
                            tweet_processor.OPT.NUMBER,
                            tweet_processor.OPT.RESERVED  # RT and FAV
                            )


def clean(text):
    text = remove_diacritics(text)
    text = remove_repeating_char(text)
    text = tweet_processor.clean(text)
    text = text.replace('\n', ' ')
    return text


def do_work(zip_file, label):
    outfilename = 'arabic_tweets_tsv/' + zip_file.replace('zip', '') + 'tsv'
    outfile = open(outfilename, encoding='utf-8', mode='w')
    with zipfile.ZipFile('arabic_tweets_json/' + zip_file) as z:
        for filename in z.namelist():
            print('processing', filename)
            with z.open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    json_tweet = json.loads(line)
                    if 'retweeted_status' in json_tweet:
                        text = json_tweet['retweeted_status']['text']
                    else:
                        text = json_tweet['text']
                    clean_tweet = clean(text)
                    if has_spam(clean_tweet):
                        continue
                    outfile.write('{}\t{}\n'.format(label, clean_tweet))


if __name__ == '__main__':
    do_work('Arabic_tweets_negative_20190412.zip',
            'neg')
    do_work('Arabic_tweets_positive_20190412.zip',
            'pos')
    print('all done')
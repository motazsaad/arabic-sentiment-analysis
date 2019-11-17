import json
from pyunpack import Archive
import os
import preprocessor as tweet_processor

from filter_tweets import *
from textutil import *
import shutil
import glob

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
    text = text.replace('\t', ' ')
    return text


def do_work(z_file, label):
    outfile_name = 'arabic_tweets_tsv/' + z_file.replace('7z', '') + 'tsv'
    outfile = open(outfile_name, encoding='utf-8', mode='w')

    all_count = 0
    count = 0
    out_dir = '/tmp/' + label
    print(out_dir)
    try:
        shutil.rmtree(out_dir)
        print('directory {} deleted'.format(out_dir))
    except BaseException as error:
        print('Warning: {}'.format(error))
    try:
        os.mkdir(out_dir)
        print('directory {} created'.format(out_dir))
    except BaseException as error:
        print('Warning: {}'.format(error))
    Archive('arabic_tweets_json/' + z_file).extractall(out_dir)
    json_files = glob.glob(out_dir + '/*.json')
    print(json_files[:10])
    print('# of json files: {}'.format(len(json_files)))
    for filename in json_files:
        print('processing', filename)
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                all_count += 1
                json_tweet = json.loads(line)
                # if 'retweeted_status' in json_tweet:
                #     if 'text' in json_tweet['retweeted_status']:
                #         text = json_tweet['retweeted_status']['text']
                # else:
                #     text = json_tweet['text']
                text = None
                if 'retweeted_status' in json_tweet:
                    json_tweet.get('retweeted_status').get('text')
                if text is None:
                    text = json_tweet.get('text')
                if text:
                    clean_tweet = clean(text)
                    if has_spam(clean_tweet):
                        continue
                    if len(clean_tweet.split()) < 3:
                        continue
                    outfile.write('{}\t{}\n'.format(label, clean_tweet))
                    count += 1
    print('{} tweets are kept out of {}'.format(count, all_count))
    print('----------------------')


if __name__ == '__main__':
    do_work('Arabic_tweets_negative_20191104.7z',
            'neg')
    do_work('Arabic_tweets_positive_20191104.7z',
            'pos')
    print('all done')

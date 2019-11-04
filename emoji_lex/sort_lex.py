pos_emoji_file = 'positive_emoji_v3.txt'
neg_emoji_file = 'negative_emoji_v3.txt'


def load_emoj_lex(emoji_file):
    emojis = open(emoji_file, encoding='utf-8').read().split('\n')
    return set(emojis)

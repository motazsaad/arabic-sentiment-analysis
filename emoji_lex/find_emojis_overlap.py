# pos_emoji_file = 'positive_emoji_v3.txt'
# neg_emoji_file = 'negative_emoji_v3.txt'

pos_emoji_file = 'positive_emoji_v3_unicode.txt'
neg_emoji_file = 'negative_emoji_v3_unicode.txt'


def load_emoj_lex(emoji_file):
    emojis = open(emoji_file, encoding='utf-8').read().split('\n')
    return set(emojis)


pos_emojis = load_emoj_lex(pos_emoji_file)
neg_emojis = load_emoj_lex(neg_emoji_file)

pos_emojis.intersection(pos_emojis)

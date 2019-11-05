# pos_emoji_file = 'positive_emoji_v3.txt'
# neg_emoji_file = 'negative_emoji_v3.txt'

pos_emoji_file = 'positive_emoji_v3.txt'
neg_emoji_file = 'negative_emoji_v3.txt'


def load_emoj_lex(emoji_file):
    emojis = open(emoji_file, encoding='utf-8').read().split('\n')
    return set(sorted(emojis))


pos_emojis = load_emoj_lex(pos_emoji_file)
neg_emojis = load_emoj_lex(neg_emoji_file)


def sort_lex(emo_set, emo_file):
    with open(emo_file, encoding='utf-8', mode='w') as file_writer:
        for emo in emo_set:
            file_writer.write(emo + '\n')


sort_lex(pos_emojis, pos_emoji_file)
sort_lex(neg_emojis, neg_emoji_file)

print('all done')

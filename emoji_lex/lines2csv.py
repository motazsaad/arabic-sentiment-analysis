# pos_emoji_file = 'positive_emoji_v3.txt'
# neg_emoji_file = 'negative_emoji_v3.txt'


pos_emoji_file = 'positive_emoji_v3_unicode.txt'
neg_emoji_file = 'negative_emoji_v3_unicode.txt'


def load_emoj_lex(emoji_file):
    emojis = open(emoji_file, encoding='utf-8').read().split('\n')
    return set(sorted(emojis))


pos_emojis = load_emoj_lex(pos_emoji_file)
neg_emojis = load_emoj_lex(neg_emoji_file)


def lines2csv_lex(emo_set, emo_file):
    with open(emo_file, encoding='utf-8', mode='w') as file_writer:
        for emo in emo_set:
            if emo.strip():
                if emo.strip() != emo_set[-1]:
                    file_writer.write(emo + ', ')
                else:
                    file_writer.write(emo)


lines2csv_lex(pos_emojis, pos_emoji_file.replace('.txt', '.csv'))
lines2csv_lex(neg_emojis, neg_emoji_file.replace('.txt', '.csv'))

print('all done')

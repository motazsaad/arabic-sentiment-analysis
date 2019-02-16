from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB, MultinomialNB
import random
from sklearn.metrics import accuracy_score


data = []
data_labels = []

positive_file = 'arabic_tweets_txt/positive_tweets_arabic_20181207_100.txt'
negative_file = 'arabic_tweets_txt/negative_tweets_arabic_20181207_100.txt'

print('read data ...')
# read positive data
with open(positive_file, encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')

data = data[:2500]
data_labels = data_labels[:2500]

# read negative data
with open(negative_file, encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')

data = data[:5000]
data_labels = data_labels[:5000]


print('data size', len(data_labels))
print('# of positive', data_labels.count('pos'))
print('# of negative', data_labels.count('neg'))

print('text to word-frequency vectors')
vectorizer = CountVectorizer(
    analyzer = 'word',
    lowercase = False,
    ngram_range = (1, 2),
    min_df = 3
)

print('transform data to vectors')
features = vectorizer.fit_transform(data)
print('represent features as array')
features_nd = features.toarray()  # for easy usage
test_percentage = 0.2
print('split the data into train ({}%) and test ({}%)'.format(
    (1-test_percentage)*100, test_percentage*100))
X_train, X_test, y_train, y_test = train_test_split(
        features_nd,
        data_labels,
        test_size=test_percentage,
        random_state=42,
        stratify=data_labels)
######################################################

print('define classifier')
# classifier = LogisticRegression()
classifier = MultinomialNB()
# classifier = GaussianNB()
print('classifier:', classifier.__class__)

print('train ...')
classifier = classifier.fit(X=X_train, y=y_train)
print('make predictions on test data')
y_pred = classifier.predict(X_test)


print('accuracy:')
print(accuracy_score(y_test, y_pred))
print('classifier:', classifier.__class__)
print('accuracy:', accuracy_score(y_test, y_pred));
print(metrics.classification_report(y_test, y_pred))

# print('display random predictions from the test data')
# j = random.randint(0, len(X_test)-7)
# for i in range(j, j+7):
#     label = y_pred[0]
#     ind = features_nd.tolist().index(X_test[i].tolist())
#     text = data[ind].strip()
#     print('label:', label, 'text:', text)


print('test example')
docs_new = ['انا احب البيتزا ❤ ❤ ', 'المعنويات عالية :) 👌 ',
            'انا بكره الروتين ']
X_new_counts = vectorizer.transform(docs_new)
predicted = classifier.predict(X_new_counts.toarray())
for doc, category in zip(docs_new, predicted):
    print('label: {}\tdoc: {}'.format(category, doc))
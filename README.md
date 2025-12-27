# arabic-sentiment-analysis
Sentiment Analysis in Arabic tweets 


### Context

This dataset was collected to provide Arabic sentiment corpus for the research community to investigate deep learning approaches for Arabic sentiment analysis. 

### Content


This dataset we collected in April 2019. It contains 58K Arabic tweets (47K training, 11K test) tweets annotated in positive and negative labels. The dataset is balanced and collected using positive and negative emojis lexicon. 

Data format: Tab-separated values TSV 
label




## Python comparability 
This code is compatible with python 3.x. If python 3 is not default in your system, please using python3 and pip3 commands instead of python and pip commands. 

## Install requirements 
`pip install -r requirements.txt`


## Results at Kaggle 
* SciKit-Learn ML algorithms 
    * https://www.kaggle.com/mksaad/sentiment-analysis-in-arabic-tweets-using-sklearn

* NLTK Naive Bayes 
    * https://www.kaggle.com/mksaad/arabic-sentiment-analysis-in-tweets-nb-bow

    * https://www.kaggle.com/mksaad/arabic-sentiment-analysis-in-tweets-nb-bigrams


## Reference
https://mksaad.wordpress.com/2018/12/07/sentiment-analysis-in-arabic-tweets-with-python/ 



## Dataset Citation 

```
@inproceedings{abu-kwaik-etal-2020-arabic,
    title = "An {A}rabic Tweets Sentiment Analysis Dataset ({ATSAD}) using Distant Supervision and Self Training",
    author = "Abu Kwaik, Kathrein  and
      Chatzikyriakidis, Stergios  and
      Dobnik, Simon  and
      Saad, Motaz  and
      Johansson, Richard",
    editor = "Al-Khalifa, Hend  and
      Magdy, Walid  and
      Darwish, Kareem  and
      Elsayed, Tamer  and
      Mubarak, Hamdy",
    booktitle = "Proceedings of the 4th Workshop on Open-Source Arabic Corpora and Processing Tools, with a Shared Task on Offensive Language Detection",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resource Association",
    url = "https://aclanthology.org/2020.osact-1.1/",
    pages = "1--8",
    language = "eng",
    ISBN = "979-10-95546-51-1"
}
```

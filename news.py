from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
from datetime import datetime
import pandas as pd
import nltk


def getNews(topic):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    year, month, date = str(datetime.now()).split()[0].split('-')
    if int(date) > 7:
        py, pm, pd_ = [year, month, int(date)-7]
    else:
        py, pm, pd_ = [year, int(month)-1, 31+(int(date)-7)]

    if int(pm) == 0:
        py, pm, pd_ = [int(year)-1, str(12), 31+(int(date)-7)]


    d, ppd = [f'{month}/{date}/{year}', f'{pm}/{pd_}/{py}']
    print("Showing results from", d, 'to', ppd)
    googlenews=GoogleNews(start=f'{month}/{date}/{year}',end=f'{pm}/{pd_}/{py}')
    googlenews.search(topic)
    result=googlenews.result()
    df=pd.DataFrame(result)
    list=[]
    for ind in df.index:
        try:
            article = Article(df['link'][ind],config=config)
            article.download()
            article.parse()
            article.nlp()
        except:
            pass
        if article.text != '':
            list.append(article.title+': '+article.summary)
            break
    
    return list[0]

top_news = [
getNews('Biggest News'),
getNews('Artificial Intelligence'),
getNews('Stock Market'),
getNews('Technology'),
getNews('MCU'),
getNews('Wake County')]

for i in top_news:
    print(i, '\n\n\n\n')


from janome.tokenizer import Tokenizer
import pandas as pd
import numpy as np
import pprint
import twitter as tw
import csv
import matplotlib.pyplot as plt

pn_df = pd.read_csv('/Users/fujitayukihide/Desktop/pn.csv.m3.120408.trim.txt',
                    sep='\t',
                    encoding='utf-8',
                    names=('Word','PN','Nature'))
# PN Tableをデータフレームからdict型に変換しておく
word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])
for i in range(len(pn_list)):
    if pn_list[i] == "p":
        pn_list[i] = 1.0
    elif pn_list[i] == "e":
        pn_list[i] = 0.0
    elif pn_list[i] == "n":
        pn_list[i] = -1.0
    else:
        pn_list[i] = 0.0 #辞書側が不明としているものは0としておく
pn_dict = dict(zip(word_list, pn_list))

def get_diclist(parsed_tweet):
    diclist = []
    for word in parsed_tweet:
        surface = word.surface
        baseform = word.base_form
        d = {'Surface':surface, 'BaseForm':baseform}
        diclist.append(d)
    return diclist

def add_pnvalue(diclist):
    pn_diclist = []
    for word in diclist:
        base = word['BaseForm']
        if base in pn_dict:
            pn = pn_dict[base]
        else:
            pn = "notfound"
        word['PN'] = pn
        pn_diclist.append(word)
    return pn_diclist

def get_pnmean(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)
    if len(pn_list) > 0:
        pnmean = np.mean(pn_list)
    else:
        pnmean = None
    return(pnmean)

def get_tweet_pnmean_list(tweetlist):
    print()

if __name__ == '__main__':
    t = Tokenizer()
    api = tw.get_api()
    search_results = tw.get_search_results(api, 100)
    tweetlist = tw.get_tweets(search_results)
    tweet_pnmean_list = []
    for td in tweetlist:
        tweet = td['tweet']
        tweet = tweet.replace('\n', '')
        parsed_tweet = t.tokenize(tweet)
        diclist = get_diclist(parsed_tweet)
        diclist = add_pnvalue(diclist)
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(diclist)
        pnmean = get_pnmean(diclist)
        d = {'pnmean': pnmean, 'tweet': tweet}
        tweet_pnmean_list.append(d)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(tweet_pnmean_list)
    df = pd.DataFrame(tweet_pnmean_list)
    df = df.sort_values(by='pnmean', ascending=True)
    df.to_csv('TweetNP.csv',
                index=None,
                encoding='utf-8',
                quoting=csv.QUOTE_NONNUMERIC)
    x = list(df['pnmean'].dropna())
    plt.hist(x)
    plt.show()

from janome.tokenizer import Tokenizer
import pandas as pd
import numpy as np
import pprint

pn_df = pd.read_csv('/Users/fujitayukihide/Desktop/pn_ja.txt',
                    sep=':',
                    encoding='utf-8',
                    names=('Word','Reading','POS', 'PN')
                   )
# PN Tableをデータフレームからdict型に変換しておく
word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])
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

if __name__ == '__main__':
    t = Tokenizer()
    tweet = "を"
    parsed_tweet = t.tokenize(tweet)
    diclist = get_diclist(parsed_tweet)
    diclist = add_pnvalue(diclist)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(diclist)
    print(get_pnmean(diclist))

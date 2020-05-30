# -*- coding: utf-8 -*-
'''
将训练数据使用jieba分词工具进行分词。并且剔除stopList中的词。
得到词表：
        词表的每一行的内容为：词 词的序号 词的频次
'''


import json
import jieba
from tqdm import tqdm

Train_ValidJsonFile = 'data/articles/train_data.json'#训练数据文件
Test_ValidJsonFile = 'data/articles/test_data.json'#测试数据文件
stopwordFile = 'data/txt/stopword.txt'
train_wordLabelFile = 'data/txt/train_wordLabel.txt'
train_lengthFile = 'data/txt/train_length.txt'
test_wordLabelFile = 'data/txt/test_wordLabel.txt'
test_lengthFile = 'data/txt/test_length.txt'


def read_stopword(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')

    return data

"""
File        -->待处理数据（train）
Label       -->词表数据（train）
length      -->词表长度（train）
"""
def main(File,Label,lengthfile):
    worddict = {}
    stoplist = read_stopword(stopwordFile)#读取停用词
    datas = open(File, 'r', encoding='utf_8').read().split('\n')
    datas = list(filter(None, datas))
    data_num = len(datas)
    len_dic = {}
    for line in datas:
        line = json.loads(line)
        title = line['title']
        title_seg = jieba.cut(title, cut_all=False)
        length = 0
        for w in title_seg:
            if w in stoplist:
                continue
            length += 1
            if w in worddict:
                worddict[w] += 1
            else:
                worddict[w] = 1
        if length in len_dic:
            len_dic[length] += 1
        else:
            len_dic[length] = 1

    wordlist = sorted(worddict.items(), key=lambda item:item[1], reverse=True)
    f = open(Label, 'w', encoding='utf_8')
    ind = 0
    for t in wordlist:
        d = t[0] + ' ' + str(ind) + ' ' + str(t[1]) + '\n'
        ind += 1
        f.write(d)

    for k, v in len_dic.items():
        len_dic[k] = round(v * 1.0 / data_num, 3)
    len_list = sorted(len_dic.items(), key=lambda item:item[0], reverse=True)
    f = open(lengthfile, 'w')
    for t in len_list:
        d = str(t[0]) + ' ' + str(t[1]) + '\n'
        f.write(d)

if __name__ == "__main__":
    main(Train_ValidJsonFile,train_wordLabelFile,train_lengthFile)#处理训练数据
    main(Train_ValidJsonFile,test_wordLabelFile,test_lengthFile)#处理测试数据
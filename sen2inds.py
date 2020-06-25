#-*- coding: utf_8 -*-

import json
import sys, io
import jieba
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf_8') #改变标准输出的默认编码

Train_ValidJsonFile = 'data/articles/train_data.json'#训练数据文件
Test_ValidJsonFile = 'data/articles/test_data.json'#测试数据文件
stopwordFile = 'data/txt/stopword.txt'
train_wordLabelFile = 'data/txt/train_wordLabel.txt'
train_lengthFile = 'data/txt/train_length.txt'
trainDataVecFile = 'data/txt/train_data_vec.txt'
train_labelFile = 'data/txt/train_label.txt'

test_wordLabelFile = 'data/txt/test_wordLabel.txt'
test_lengthFile = 'data/txt/test_length.txt'
testDataVecFile = 'data/txt/test_data_vec.txt'
test_labelFile = 'data/txt/test_label.txt'

maxLen = 20


def read_labelFile(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')
    label_w2n = {}
    label_n2w = {}
    for line in data:
        line = line.split(' ')
        name_w = line[0]
        name_n = int(line[1])
        label_w2n[name_w] = name_n
        label_n2w[name_n] = name_w

    return label_w2n, label_n2w


def read_stopword(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')

    return data


def get_worddict(file):
    datas = open(file, 'r', encoding='utf_8').read().split('\n')
    datas = list(filter(None, datas))
    word2ind = {}
    for line in datas:
        line = line.split(' ')
        word2ind[line[0]] = int(line[1])
    
    ind2word = {word2ind[w]:w for w in word2ind}
    return word2ind, ind2word

"""
labelFile           -->标签数据(train/teat)
wordLabelFile       -->词表数据(train/teat)
DataVecFile    -->数字向量数据(train/teat)
ValidJsonFile   -->训练数据/测试数据(train/teat)
"""
def json2txt(labelFile,wordLabelFile,DataVecFile,ValidJsonFile):
    label_dict, label_n2w = read_labelFile(labelFile)
    word2ind, ind2word = get_worddict(wordLabelFile)
    #print("word2ind-->%s" %word2ind)
    traindataTxt = open(DataVecFile, 'w')
    stoplist = read_stopword(stopwordFile)
    datas = open(ValidJsonFile, 'r', encoding='utf_8').read().split('\n')
    datas = list(filter(None, datas))
    random.shuffle(datas)
    for line in datas:
        line = json.loads(line)
        title = line['title']
        cla = line['classify']
        cla_ind = label_dict[cla]

        title_seg = jieba.cut(title, cut_all=False)
        title_ind = [cla_ind]
        for w in title_seg:
            if w in stoplist:
                continue
            print("w-->%s" %w)
            title_ind.append(word2ind[w])
        length = len(title_ind)
        if length > maxLen + 1:
            title_ind = title_ind[0:21]
        if length < maxLen + 1:
            title_ind.extend([0] * (maxLen - length + 1))
        for n in title_ind:
            traindataTxt.write(str(n) + ',')
        traindataTxt.write('\n')


def main():
    json2txt(train_labelFile, train_wordLabelFile, trainDataVecFile, Train_ValidJsonFile)  # 处理训练数据
    json2txt(test_labelFile, test_wordLabelFile, testDataVecFile, Test_ValidJsonFile)  # 处理测试数据

if __name__ == "__main__":
    main()

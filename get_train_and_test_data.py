# -*- coding: utf-8 -*-
'''
从原数据中选取部分数据；
选取数据的title前两个字符在字典WantedClass中；
且各个类别的数量为WantedNum
'''
import jieba
import json


ValidJsonFile = 'data/articles/articles.json'#数据文件
Train_ValidJsonFile = 'data/articles/train_data.json'#训练数据文件
Test_ValidJsonFile = 'data/articles/test_data.json'#测试数据文件


WantedClass = {'种术': 0, '加术': 0, '栽1': 0, '栽2': 0, '温术': 0, '繁种': 0, '养术': 0, '疾治': 0, '饲养': 0, '栽3': 0, '病治': 0, '贮工': 0, '农术': 0, '施术': 0, '饲术': 0}
WantedNum = 1600#共2000条数据，进行二八分，分别作为测试数据，训练数据
numWantedAll = WantedNum * 15#1600*15=24000,400*15=6000,2000*15=30000


def main():
    Datas = open(ValidJsonFile, 'r', encoding='utf_8').readlines()
    train_f = open(Train_ValidJsonFile, 'w', encoding='utf_8')
    test_f = open(Test_ValidJsonFile, 'w', encoding='utf_8')


    for line in Datas:
        data = json.loads(line)
        cla = data['classify'][0]+data['classify'][-1]#得到板块名称
        if cla in WantedClass and WantedClass[cla] < WantedNum:
            data['classify'] = cla
            json_data = json.dumps(data, ensure_ascii=False)
            train_f.write(json_data)
            train_f.write('\n')
            WantedClass[cla] += 1
        elif cla in WantedClass and WantedClass[cla] >= WantedNum:
            data['classify'] = cla
            json_data = json.dumps(data, ensure_ascii=False)
            test_f.write(json_data)
            test_f.write('\n')
            WantedClass[cla] += 1

if __name__ == '__main__':
    main()
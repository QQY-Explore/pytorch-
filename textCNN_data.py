from torch.utils.data import Dataset, DataLoader
import torch
import random
import numpy as np



trainDataVecFile = 'data/txt/train_data_vec.txt'
testDataVecFile = 'data/txt/test_data_vec.txt'
'''
def get_valdata(file=trainDataVecFile):
    valData = open(trainDataVecFile, 'r').read().split('\n')
    valData = list(filter(None, valData))
    random.shuffle(valData)

    return valData
'''
'''
DataVecFile-->词向量（train/test）
'''
class textCNN_data(Dataset):
    def __init__(self,DataVecFile):
        trainData = open(DataVecFile, 'r').read().split('\n')
        trainData = list(filter(None, trainData))
        random.shuffle(trainData)
        self.trainData = trainData

    def __len__(self):
        return len(self.trainData)

    def __getitem__(self, idx):
        data = self.trainData[idx]
        data = list(filter(None, data.split(',')))
        data = [int(x) for x in data]
        cla = data[0]
        sentence = np.array(data[1:])

        return cla, sentence


#DataVecFile    (train/test)
def textCNN_dataLoader(param,DataVecFile):
    dataset = textCNN_data(DataVecFile=DataVecFile)
    batch_size = param['batch_size']
    shuffle = param['shuffle']
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


if __name__ == "__main__":
    DataVecFile = trainDataVecFile  #trainDataVecFile训练数据 testDataVecFile测试数据
    dataset = textCNN_data(DataVecFile=DataVecFile)
    cla, sen = dataset.__getitem__(0)

    print(cla)
    print(sen)
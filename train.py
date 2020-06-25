import torch
import os
import torch.nn as nn
import numpy as np
import time
import matplotlib.pyplot as plt
from model import textCNN
import sen2inds
import textCNN_data

trainDataVecFile = 'data/txt/train_data_vec.txt'
testDataVecFile = 'data/txt/test_data_vec.txt'
#word2ind字典：字符为key，角标为value
#ind2word字典：角标为key，字符为value
word2ind, ind2word = sen2inds.get_worddict('data/txt/train_wordLabel.txt')
#label_w2n字典：字符（子板块名）为key，角标为value
#label_n2w字典：角标为key，字符（子板块名）为value
label_w2n, label_n2w = sen2inds.read_labelFile('data/txt/train_label.txt')
weightFile = 'data/pkl/weight.pkl'
textCNN_param = {
    'vocab_size': len(word2ind),
    'embed_dim': 60,
    'class_num': len(label_w2n),
    "kernel_num": 16,
    "kernel_size": [3, 4, 5],
    "dropout": 0.5,
}
dataLoader_param = {
    'batch_size': 128,
    'shuffle': True,
}


def main():
    #init net
    print('init net...')
    net = textCNN(textCNN_param)

    if os.path.exists(weightFile):
        print('load weight')
        net.load_state_dict(torch.load(weightFile))
    else:
        net.init_weight()
    print("net-->%s" %net)

    net.cuda()

    #init dataset
    print('init dataset...')
    dataLoader = textCNN_data.textCNN_dataLoader(dataLoader_param, trainDataVecFile)#trainDataVecFile训练数据 testDataVecFile测试数据
    #valdata = textCNN_data.get_valdata()

    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    criterion = nn.NLLLoss()

    log = open('data/txt/log_{}.txt'.format(time.strftime('%y%m%d%H')), 'w')
    log.write('epoch step loss\n')
    log_test = open('data/txt/log_test_{}.txt'.format(time.strftime('%y%m%d%H')), 'w')
    log_test.write('epoch step test_acc\n')
    print("training...")
    for epoch in range(100):
        for i, (clas, sentences) in enumerate(dataLoader):
            optimizer.zero_grad()
            sentences = sentences.type(torch.LongTensor).cuda()
            clas = clas.type(torch.LongTensor).cuda()
            out = net(sentences)
            loss = criterion(out, clas)
            loss.backward()
            optimizer.step()

            if (i + 1) % 1 == 0:
                print("epoch:", epoch + 1, "step:", i + 1, "loss:", loss.item())
                data = str(epoch + 1) + ' ' + str(i + 1) + ' ' + str(loss.item()) + '\n'
                log.write(data)
        print("save model...")
        torch.save(net.state_dict(), weightFile)
        torch.save(net.state_dict(), "data/model\{}_model_iter_{}_{}_loss_{:.2f}.pkl".format(time.strftime('%y%m%d%H'), epoch, i, loss.item()))  # current is model.pkl
        print("epoch:", epoch + 1, "step:", i + 1, "loss:", loss.item())



if __name__ == "__main__":
    main()

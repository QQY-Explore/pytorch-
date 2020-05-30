Python版本：Python3.7.0，但是没有太大影响，
CUDA版本：cuda_10.1.243_426.00_win10
CUDNN版本：v7.6.5
pytorch版本：torch-1.5.0+cu101-cp37-cp37m-win_amd64
spider.py：从网站上爬取数据，在程序里是爬取67页数据，推荐改为68页，因为在处理数据时有一个类别少一个数据，但是对程序无太大影响，
get_train_and_test_data.py：将爬虫获得的数据二八差分成训练数据和测试数据，因为类别长度不同，所以每个类别都取首尾的字作为类别。
data\articles：此目录下为保存的网上下载数据，训练数据，测试数据
data\modelL此目录保存训练生成的pkl
data\pkl此目录保存训练所得pkl
data\txt此目录保存训练过程中一些txt文件

运行步骤：
1、spider.py
2、get_train_and_test_data.py
3、get_wordlists.py
4、sen2inds.py
5、train.py
6、test.py

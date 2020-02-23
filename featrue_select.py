import random
import os
import os.path
import numpy as np
from sklearn import ensemble
from util import DataPre as dp

from numpy import array
from scipy.sparse import csr_matrix
grd = ensemble.RandomForestClassifier(n_estimators=30)
training_file = 'train.txt'
traindata_dir = './INSPEC_Data/INSPEC_train'
valdata_dir = './INSPEC_Data/INSPEC_validation'
tf_name = None

def check_data(data, tag, qid, type):
    for item in data:
        if len(item) > 3 and item[0] and item[1] and item[2]:
            pt = item[0] + item[1] + item[2]
            with open('./' + str(type) + '.txt', 'a') as f:
                c = 1
                f.write(str(tag) + ' ' + 'qid:' + str(qid) + ' ')
                for val in pt:
                    f.write(str(c) + ':' + str(val) + ' ')
                    c += 1
                f.write('\n')
            print(str(len(pt)) + str(pt))

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        return(files)
tf_name = os.listdir(os.path.join(traindata_dir))
# data = dp('./INSPEC_Data/INSPEC_train/Vp9AaLm_jQ9Q0U90W1S.xlsx').load()

for item in tf_name:
    if item[0] =='V':
        data = dp(os.path.join(traindata_dir, item)).load()
        type = os.path.splitext(item)[0]
        neo_len = len(data[1])
        pos_len = len(data[0])
        print(pos_len)
        if neo_len != 0:
            for i in range(round((pos_len / neo_len) * 0.7)):
                pos_train = random.sample(data[0], neo_len)
                neo_train = random.sample(data[1], round(neo_len * 0.7))
                qid = round(random.random() * 10000)
                check_data(neo_train, 1, qid, type)
                check_data(pos_train, 0, qid, type)





# print(data[1][0][0:3])
# a = [0]*len(pos_train)
# b = [1]*len(neo_train)

# train = np.hstack([array()])
# grd.fit(array(neo_train+pos_train),array(b+a))
# print(grd.feature_importances_)

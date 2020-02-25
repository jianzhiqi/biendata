import random
import os
import os.path
import numpy as np
from numpy import array
from scipy.sparse import csr_matrix

from sklearn import ensemble
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import r2_score
from collections import defaultdict

from util import DataPre as dp
grd = ensemble.RandomForestClassifier(n_estimators=30)
training_file = 'train.txt'
traindata_dir = './INSPEC_Data/INSPEC_train'
valdata_dir = './INSPEC_Data/INSPEC_validation'
train = []
label = []
tf_name = None



def write_file(data, tag, qid, type):
    for item in data:
        if len(item) >= 3 and isinstance(item[0],list) and isinstance(item[1],list) and isinstance(item[2],list):
            print(item[0])
            print(item[1])
            print(item[2])

            pt = item[0] + item[1] + item[2]
            train.append(pt)
            label.append(tag)

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
# tf_name = os.listdir(os.path.join(traindata_dir))
tf_name = ['VpWAaLm_jQU999p9zWB.xlsx']
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
                write_file(neo_train, 1, qid, type)
                write_file(pos_train, 0, qid, type)





# print(data[1][0][0:3])
# a = [0]*len(pos_train)
# b = [1]*len(neo_train)

# train = np.hstack([array()])
t = array(train)
t[np.isnan(t)] = 0
grd.fit(t,array(label))
print(grd.feature_importances_)

rf = RandomForestRegressor()
scores = defaultdict(list)

# crossvalidate the scores on a number of different random splits of the data
for train_idx, test_idx in ShuffleSplit(len(X), 100, .3):
    X_train, X_test = train[train_idx], train[test_idx]
    Y_train, Y_test = label[train_idx], label[test_idx]
    r = rf.fit(X_train, Y_train)
    acc = r2_score(Y_test, rf.predict(X_test))
    for i in range(train.shape[1]):
        X_t = X_test.copy()
        np.random.shuffle(X_t[:, i])
        shuff_acc = r2_score(Y_test, rf.predict(X_t))
        scores[names[i]].append((acc - shuff_acc) / acc)
print("Features sorted by their score:")
print(sorted([(round(np.mean(score), 4), feat) for feat, score in scores.items()], reverse=True))

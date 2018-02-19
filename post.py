from sklearn import preprocessing
from sklearn.cluster import DBSCAN
import numpy as np


def cosine(A, B):
    num = np.dot(A, B)
    denom = np.linalg.norm(A) * np.linalg.norm(B)
    cos = num / denom
    return cos


def get_dist_mat():
    fp = open('./data/stat.txt', 'r')
    count_list = []
    for line in fp.readlines():
        items = map(float, line.strip('\n').split(','))
        count_list.append(items)

    mat = np.array(count_list)
    mat0 = preprocessing.normalize(mat)
    n = mat.shape[0]
    ans = np.zeros((n, n))
    for i in range(n):
        for k in range(n):
            ans[i][k] = 1 - cosine(mat0[i], mat0[k])
    return ans


X = get_dist_mat()
print X
db = DBSCAN(eps=0.2, min_samples=5, metric='precomputed').fit(X)
labels = db.labels_
print labels


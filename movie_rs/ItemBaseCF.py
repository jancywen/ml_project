# -*- coding: utf-8 -*-

import math
class ItemBaseCF(object):

    def __init__(self, train_file, test_file):
        self.train_file = train_file
        self.test_file = test_file
        self.readData()

    # 读取数据
    def readData(self):
        self.train = dict()
        with open(self.train_file) as f:
            for line in f:
                user, item, score, _ = line.strip().split('\t')
                self.train.setdefault(user, {})
                self.train[user][item] = int(score)

        self.test = dict()
        with open(self.train_file) as f:
            for line in f:
                user, item, score, _ = line.strip().split('\t')
                self.test.setdefault(user, {})
                self.test[user][item] = int(score)

    # 物品间相似度
    def itemSimilarity(self):
        C = dict()
        N = dict()

        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1

                C.setdefault(i, {})
                for j in items.keys():
                    if i == j:
                        continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1

        self.W = dict()
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j, cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))

        # return self.W

    def Recommend(self, user, K=3, N=10):
        rank = dict()
        action_item = self.train[user]

        for item, score in action_item.items():
            for j, wj in sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[0: K]:
                if j in action_item.keys():
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj

        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N])


if __name__ == "__main__":
    cf = ItemBaseCF('./ml-100k/u.data', './ml-100k/u.data')
    cf.itemSimilarity()
    print(cf.Recommend('3'))

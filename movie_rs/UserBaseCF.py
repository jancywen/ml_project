# -*- coding: utf-8 -*-
import math
from scipy.spatial import distance

class UserBaseCF(object):

    def __init__(self, train_file, test_file):
        self.tran_file = train_file
        self.test_file = test_file
        self.readData()


    def readData(self):

        self.train = dict()
        with open(self.tran_file) as f:
            for line in f:
                user, item, score, _ = line.strip().split('\t')
                self.train.setdefault(user, {})
                self.train[user][item] = int(score)

        self.test = dict()
        with open(self.test_file) as f:
            for line in f:
                user, item, score, _ = line.strip().split('\t')
                self.test.setdefault(user, {})
                self.test[user][item] = int(score)


    def UserSimilarity(self):
        self.item_users = dict()

        for user, items in self.train.items():
            for i in items.keys():
                if i not in self.item_users:
                    self.item_users[i] = set()
                self.item_users[i].add(user)

        C = dict()
        N = dict()

        for i, users in self.item_users.items():
            for u in users:
                N.setdefault(u, 0)
                N[u] += 1

                C.setdefault(u, {})
                for v in users:
                    if u == v:
                        continue
                    C[u].setdefault(v, 0)
                    C[u][v] += 1

        self.W = dict()
        for u, related_users in C.items():
            self.W.setdefault(u, {})
            for v, cuv in related_users.items():
                self.W[u][v] = cuv / math.sqrt(N[u] * N[v])


        self.Euc = dict()
        for u, related_users in C.items():
            self.Euc.setdefault(u, {})
            for v, cuv in related_users.items():
                pass

        return self.W


    def Recommend(self, user, K=3, N=10):
        rank = dict()
        action_item = self.train[user].keys()

        for v, wuv in sorted(self.W[user].items(), key=lambda x: x[1], reverse=True)[0: K]:
            for i, rui in self.train[v].items():
                if i in action_item:
                    continue
                rank.setdefault(i, 0)
                rank[i] += wuv * rui

        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N])


if __name__ == '__main__':
    cf = UserBaseCF('', '')
    cf.UserSimilarity()
    print(cf.Recommend('3'))

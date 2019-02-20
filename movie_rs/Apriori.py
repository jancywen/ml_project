# -*- coding: utf-8 -*-


from numpy import *


def loadDataSet():
    """
    生成原始数据, 用于测试
    :return:
    """
    return[[1, 3, 4],
           [2, 3, 5],
           [1, 2, 3, 5],
           [2, 5]]


def createC1(dataSet):
    """
    遍历数据集,建立 1- 项集
    :param dataSet:
    :return:
    """
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()

    return map(frozenset, C1)


# def forzenset(dataset):
#     """
#
#     :param dataset:
#     :return:
#     """

def scanD(D, Ck, minSupport):
    """

    :param D:
    :param Ck:
    :param minSupport:
    :return:
    """
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1

    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support

    return retList, supportData




def generateRules(L, supportData, minConf = 0.7):
    """

    :param L:
    :param supportData:
    :param minConf:
    :return:
    """

    bigRuleList = []

    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)

    D = map(set, dataSet)

    L1, supportData = scanD(D, C1, minSupport)

    # for l1 in L1:

    L = [L1]
    k = 2

    while (len(L[k-2]) > 0):

        Ck = aprioriGen(L[k-2], k)

        Lk, supK = scanD(D, Ck, minSupport)

        supportData.update(supK)

        L.append(Lk)

        k += 1
    return L, supportData


def aprioriGen(Lk, k):
    """

    :param Lk:
    :param k:
    :return:
    """
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
            else:
                pass
    return retList

def generateRules(L, supportData, minConf=0.7):
    """

    :param L:
    :param supportData:
    :param minConf:
    :return:
    """

    bigRuleList = []

    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)

    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)

    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if len(freqSet) > (m+1):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)

        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)




if __name__ == "__main__":
    dataSet = loadDataSet()
    L, supportData = apriori(dataSet, minSupport=0.5)

    rules = generateRules(L, supportData, minConf=0.5)
    print(rules)

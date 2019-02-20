# -*- coding: utf-8 -*-
import numpy as np

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q',  's', 't', 'm']]
    return simpDat


def loadMoviceLines():
    movices = {}
    ret = []
    with open('./ml-100k/u1.base') as f:
        for line in f.readlines():
            uid, mid, _, _ = line.strip().split('\t')
            if uid not in movices:
                movices[uid] = []
            movices[uid].append(mid)

    for _, v in movices.items():
        ret.append(v)
    return ret

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def createTree(dataSet, minSup=3):
    """
    创建树
    :param dataSet:
    :param minSup: 最小支持度
    :return:
    """
    # 头指针表,存储每个元素项出现的频度
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    # 删除不频繁项
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del(headerTable[k])

    freqItemSet = set(headerTable.keys())

    if len(freqItemSet) == 0: return None, None

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():

        localD = {}

        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
        updateTree(orderedItems, retTree, headerTable, count)

    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    """
    更新树
    :param items:
    :param inTree:
    :param headerTable:
    :param count:
    :return:
    """
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    """
    查找前缀路径  获取条件模式基
    :param basePat:
    :param treeNode:
    :return:
    """
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    """
    查找频繁项集
    :param inTree:
    :param headerTable:
    :param minSup:
    :param preFix:
    :param freqItemList:
    :return:
    """
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda x: x[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)

        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


    if myCondTree != None:
        myCondTree.disp(1)


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}


    def inc(self, numOccur):
        self.count += numOccur


    def disp(self, ind=1):
        print(" "*ind, self.name, " ", self.count)
        for child in self.children.values():
            child.disp(ind+1)



if __name__ == "__main__":

    # simpDat = loadSimpDat()
    # print(simpDat)
    simpDat = loadMoviceLines()[:10]
    initSet = createInitSet(simpDat)
    print(initSet)

    myFPtree, myHeaderTab = createTree(initSet, 5)
    myFPtree.disp()


    # pre_path_x= findPrefixPath('x', myHeaderTab['x'][1])
    # pre_path_y = findPrefixPath('y', myHeaderTab['y'][1])


    freqItems = []
    mineTree(myFPtree, myHeaderTab, 5, set([]), freqItems)
    print('*#'*20)
    print(freqItems)


    with open('./result_fp', 'w') as f:
        for l in freqItems:
            li = []
            for ll in l:

                li.append(str(ll))
            f.write('&&'.join(li) + '\r\n')

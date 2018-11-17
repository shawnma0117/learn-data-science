#!/usr/bin/python
#coding: utf-8


def loadDataSet():
    '''
    输入：无
    功能：产生简单的数据集
    输出：dataset
    '''
    return [['A','C','D'],['B','C','E'],['A','B','C','E'],['B','E']]  #每条是一个交易，每个交易里面的数字代表商品


def createC1(dataset):
    '''
    输入：数据集
    功能：构建1-项集。即所有独立的商品。
    '''
    C1 = []
    for transction in dataset:
        #print transction
        for item in transction:
            if not [item] in C1:  # 保证商品不重复
                C1.append([item]) # 使用列表作为C1元素是因为后续需要使用集合操作
    C1.sort()
    return  map(frozenset,C1) # 用frozenset是为了保证可以作为字典的key去查询support



def scanDataSet(DataSet,Ck,minSupport=0.5):
    '''
    输入：DataSet应为每条记录是set类型数据（被用于判断是否是其子集操作），Ck中的每个项集为frozenset型数据（被用于字典关键字）
         Ck为候选频繁项集，minSupport为判断是否为频繁项集的最小支持度（认为给定）
    功能：从候选项集中找出支持度support大于minSupport的频繁项集
    输出：频繁项集集合returnList,以及频繁项集对应的支持度support
    '''
    subSetCount = {} #
    for transction in DataSet:#取出数据集dataset中的每行记录
        for subset in Ck:#取出候选频繁项集Ck中的每个项集
            if subset.issubset(transction):#判断Ck中项集是否是数据集每条记录数据集合中的子集
                if not subSetCount.has_key(subset): # 这个项集是否是第一次出现
                    subSetCount[subset] = 1
                else:
                    subSetCount[subset] += 1
    numItem = float(len(DataSet))
    returnList =[]
    returnSupportData = {}
    for key in subSetCount:
        support = subSetCount[key]/numItem
        if support >= minSupport:
            returnList.insert(0,key)
            returnSupportData[key] = support
    return returnList,returnSupportData


# In[175]:


def createCk(Lk,k):
    '''
    根据输入的集合列表，创建k-项集
    '''
    returnList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2];L2 = list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1 == L2:
                '''
                只需取前k-2个元素相等的候选频繁项集即可组成元素个数为k+1的候选频繁项集！！
                比如：k=3时，{A,B}|{A,C} = {A,B,C};与{A,B}|{B,C} = {A,B,C}一样，因此无需重复append
                '''
                returnList.append(Lk[i] | Lk[j])    
    return returnList


def apriori(dataset,minSupport = 0.5):
    C1 = createC1(dataset)
    DataSet = map(set,dataset)
    L1,returnSupportData = scanDataSet(DataSet,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        #由上一层的频繁项集，形成下一层没有重复的频繁项集，下一层候选频繁项集中元素个数会比上一时刻的多1
        Ck = createCk(L[k-2],k)
        #从候选频繁项集中选出支持度大于minsupport的频繁项集Lk
        Lk,supportLk = scanDataSet(DataSet,Ck,minSupport)
        #将该频繁项集及其支持度添加到returnSupportData字典中记录，其中频繁项集为关键字，支持度为关键字所对应的项
        returnSupportData.update(supportLk)
        #将频繁项集添加到列表L中记录
        L.append(Lk)
        #逐一增加频繁项集中的元素个数
        k += 1
    return L, returnSupportData  #返回所有频繁项集，和其support数值



#------------------关联规则生成函数--------------#
def generateRules(L,supportData,minConference = 0.7):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset(item) for item in freqSet] # H就是等待评估的后件
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConference)
    return bigRuleList

#用来计算所有2项频繁项的confidence
def calculationConf(freqSet, H, supportData,brl,minConference=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet - conseq]
        if conf >= minConference:
            print freqSet-conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq) # 将符合标准的后件保存
    return prunedH 

#用来计算所有2项以上的频繁项的confidence
def rulesFromConseq(freqSet, H, supportData, brl, minConference):
    m = len(H[0])
    while (len(freqSet) > m):  # 当频繁项的长度等于后件的长度，停止
        H = calculationConf(freqSet,H,supportData,brl,minConference) #Hm即为prunedH
        if (len(H)>1):  # 如果满足最小confidence的后件个数大于1，把后件中的元素的个数+1，循环。如:本来是b,e->c,接下来计算b->c,e
            H = createCk(H, (m+1)) #利用函数createCk生成包含m+1个元素的后件
            m+=1
        else:
            break

if __name__ == '__main__':
    #dataset=loadDataSet()
    dataset = input("请输入订单信息：")
    print "您购买的商品是：",dataset
    L,returnSupportData = apriori(dataset,minSupport=0.5) 
    rule = generateRules(L,returnSupportData,minConference=0.5)


import re
import PRA
import numpy as np
def getData(file1='',file2=''):
    classifier = PRA.PRA('p.txt')
    data,label = PRA.setData('q.txt')
    result = classifier.predict_proba(data)
    file = open('测试集.txt','r',encoding='utf-8')
    lines = file.readlines()
    question = []
    num = 0
    i =0
    for r in result:
        if (float(r[0])<0.8)&(float(r[1])<0.8):
            num+=1
            question.append(lines[i])
        elif (float(r[0])>0.8)&(float(r[1])>0.8):
            num+=1
            question.append(lines[i])
        i+=1
    return num,question
def worker(question=[],anwser=[]):
    i = np.random.randint(0,100)
    if i < 70:
        return anwser
    else:
        if anwser==1:
            return 0
        else:
            return 1

def most(label):
    dic = {}
    for l in label:
        keys = dic.keys()
        if l not in keys:
            dic[l] = 1
        else:
            num = dic[l]
            dic[l] = num+1
    keys = dic.keys()
    k = list(keys)
    max = dic[k[0]]
    index  = k[0]
    for key in keys:
        if max<dic[key]:
            max = dic[key]
            index = key
    return index
def crowd(questions,anwsers):
    label = []
    for question,anwser in zip(questions,anwsers):
        l = []
        for i in range(10):
            l.append(worker(question,anwser))
        label.append(most(l))
    return label
def test_crowd(question):
    anwser = []
    que = []
    for q in question:
        q = q.strip().split(' ')
        if q[3]=='type':
            anwser.append(1)
        if q[3]=='subClassOf':
            anwser.append(0)
        ques = q[1]+' '+q[5]
        que.append(ques)
    num=0
    label = crowd(que,anwser)
    for i,j in zip(anwser,label):
        if i!=j:
            num+=1
    return num
if __name__ == '__main__':
    num,question = getData()
    n = test_crowd(question)
    print(n)
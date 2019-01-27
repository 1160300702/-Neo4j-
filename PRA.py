import re
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
def setData(inputfile):
    file = open(inputfile, 'r', encoding='utf-8')
    lines = file.readlines()
    q = re.compile("\s+")
    data = []
    label = []
    j = 1
    number = len(lines)
    for line in lines:
        d = []
        line = line.split("   ")
        for l in line:
            l = l.split(":")
            if (len(l) == 1):
                continue
            l[1] = q.sub('', l[1])
            d.append(float(l[1]))
        data.append(d)
        if j > number / 2:
            label.append(0)
        else:
            label.append(1)
        j += 1
    data = np.array(data)
    label = np.array(label)
    return data,label
def PRA(inputfile):
    data,label = setData(inputfile)
    classifier = LogisticRegression(multi_class='ovr', penalty='l2', class_weight='balanced')  # 使用类，参数全是默认的

    classifier.fit(data, label)  # 训练分类模型(Fit the model according to the given training data)
    return classifier
if __name__=='__main__':
    classifier = PRA('p.txt')
    data,label = setData('q.txt')
    result = classifier.predict(data)
    num = 0
    for i,j in zip(label,result):
        if i!=j:
            num+=1
    print(num)



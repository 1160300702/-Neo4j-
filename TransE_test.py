from numpy import *
import operator
class Test():
    def __init__(self, entityList, entityVectorList, relationList ,relationVectorList, tripleListTest):
        self.entityList = {}
        self.relationList = {}
        for name, vec in zip(entityList, entityVectorList):
            self.entityList[name] = vec
        for name, vec in zip(relationList, relationVectorList):
            self.relationList[name] = vec
        self.tripleListTest = tripleListTest
    def relation_predict(self):
        anwser = []
        testlist = []
        predict = []
        for list in self.tripleListTest:
            l = []
            l.append(list[0])
            l.append(list[1])
            testlist.append(l)
            anwser.append(list[2])
        for list in testlist:
            start = list[0]
            end = list[1]
            start_Verctor = self.get_entity_Vector(start)
            end_Vector = self.get_entity_Vector(end)
            keys = self.relationList.keys()
            distances = []
            for key in keys:
                relation_Vector = self.relationList[key]
                distances.append(self.distance(start_Verctor,end_Vector,relation_Vector))
            min = distances[0]
            for dis in distances:
                if min>dis:
                    min = dis
            index = distances.index(min)
            keys = self.relationList.keys()
            i = 0
            for key in keys:
                if(i==index):
                    relation = key
                    break
                i+=1
            predict.append(relation)
        j = 0
        print(len(anwser))
        for anw,pre in zip(anwser,predict):
            if anw==pre:
                j+=1
        print(j)
    def distance(self,h,t,r):
        h = array(h)
        t = array(t)
        r = array(r)
        s = h + r - t
        return linalg.norm(s)

    def get_entity_Vector(self,entity):
        keys = self.entityList.keys()
        if entity in keys:
            return self.entityList[entity]
    def get_relation_Vector(self,relation):
        keys = self.relationList.keys()
        if relation in keys:
            return self.relationList[relation]
def openD(dir, sp=" "):
        # triple = (head, tail, relation)
        num = 0
        list = []
        with open(dir, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                triple = line.strip().split(sp)
                if (len(triple) < 3):
                    continue
                l = []
                l.append(triple[0])
                l.append(triple[2])
                l.append(triple[1])
                list.append(tuple(l))
                num += 1
        #print(num)
        return num, list
def loadData(str):
    fr = open(str,'r',encoding='utf-8')
    sArr = [line.strip().split("\t") for line in fr.readlines()]
    datArr = [[float(s) for s in line[1][1:-1].split(", ")] for line in sArr]
    nameArr = [line[0] for line in sArr]
    return datArr, nameArr
if __name__ == '__main__':
    entityVector,entitylist=loadData('data/entityVector.txt')
    testnum,testlist = openD('data/test.txt')
    relationVector,relationlist = loadData('data/relationVector.txt')
    test = Test(entitylist,entityVector,relationlist,relationVector,testlist)
    test.relation_predict()
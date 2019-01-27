import re
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "2648361987"))
#反例
def main(inputfile,outputfile):
    f = open(outputfile, 'w', encoding='utf-8')
    file = open("特征集.txt",'r',encoding='utf-8')
    temple = {}
    lines = file.readlines()
    j = 0
    q = re.compile("'")
    p = re.compile("\s+")
    for line in lines:
        line = line.split(" ")
        s = ''
        for i in range(len(line)):
            if(line[i]=='\n'):
                continue
            if float(i)%2!=0:
                line[i] = q.sub('',line[i])
                line[i] = p.sub('',line[i])
                #print(line[i])
                line[i] = line[i].split('=')
                line[i] = line[i][1]
                #print(line[i])
                s = s+' '+line[i]
        value = temple.values()
        if(s in value):
            continue
        temple[j] = s
        j+=1
    file.close()
    f1 = open(inputfile,'r',encoding='utf-8')
    lines = f1.readlines()
    j = 0
    values = temple.values()
    '''for line in lines:
        if(j==0):
            line = p.sub('',line)
            start = line
            j+=1
            continue
        if(j==1):
            j+=1
            continue
        if(j==2):
            line = p.sub('',line)
            end = line
            j=3
            i = 0
            for value in values:
                # print(value)
                value = value.split(" ")
                value = value[1:]
                # print(value)
                with driver.session() as session:
                    # print(value)
                    print(start, end, value)
                    session.read_transaction(get_P_init, i, start, end, value, f)
                i += 1
            f.writelines("\n")
            print()
            continue
        if(j==3):
            j = 0
            continue
    exit()'''
    c = re.compile("'")
    values = temple.values()
    for line in lines:
        line = line.split(" ")
        start = line[1]
        start = c.sub('\\\'',start)
        end = line[len(line)-1]
        end = p.sub("",end)
        end = c.sub('\\\'',end)
        #print(start,end)
        i = 0
        for value in values:
            #print(value)
            value = value.split(" ")
            value = value[1:]
            #print(value)
            with driver.session() as session:
                #print(value)
                print(start,end,value)
                session.read_transaction(get_P_init,i,start,end,value,f)
            i+=1
        f.writelines("\n")
        print()
def get_P_init(tx,num,start,end,path,file):
    s = 'MATCH p=(n:Word{name})'.format( name='{name:\'' + start + '\'}')
    q = '-[:{relation}]->'.format(relation = path[0])
    l = ['a','b','c','d','e','f','g','h','k','l','j','o']

    for i in range(len(path)-1):
        q = q+'({st})-[:{relation}]->'.format(st=l[i],relation=path[i+1])
    t = '(m:Word{name_1}) RETURN p'.format(name_1='{name:\'' + end + '\'}')
    s = s+q+t
    print(s)
    j = 0
   # print(s)
    for record in tx.run(s):
        j = j+1
    if j==0:
        file.writelines(str(num)+":-0.5   ")
    else:
        with driver.session() as session:
            p = session.read_transaction(get_P,num,start,end,path)
        print(p,end='  ')
        file.writelines(str(num)+':'+str(p-0.5)+"   ")

def get_P(tx,num,start,end,path):
    dict_p = {}
    s = 'MATCH (n:Word{name})'.format(name='{name:\'' + start + '\'}')
    t = '(m:Word{name_1}) RETURN m'.format(name_1='{name:\'' + end + '\'}')
    r = '(m) RETURN m'
    p = 0
    r0 = path[0]
    e = s+'-[{relation}]->'.format(relation=r0)+r
    n = 0
    for record in tx.run(e):
        n+=1
        dict_p[record['m']['name']] = 1
    Eq = n
    key = dict_p.keys()
    for k in key:
        dict_p[k] = float(dict_p[k]/Eq)
    if(len(path)>2):
        for i in range(len(path)-2):
            dict_p_2 = {}
            #print(dict_p)
            r1 = path[i+1]
        #计算接下来的e''
            key = dict_p.keys()
            for k in key:
                dict_p_1 = {}
                s = 'MATCH (n:Word{name})'.format(name='{name:\'' + k + '\'}')
                r = '(m) RETURN m'
                e = s+'-[{relation}]->'.format(relation=r1)+r
                n = 0
                for record in tx.run(e):
                    n += 1
                    dict_p_1[record['m']['name']] = 1
                Eq = n
                l = dict_p_1.keys()
                for m in l:
                    dict_p_1[m] = float(1/Eq)*dict_p[k]
                    #print(dict_p_1)
                #dict_p_1[record['m']['name']]=float(1/Eq)*dict_p[k]
                if(dict_p_2=={}):
                    dict_p_2=dict_p_1
                else:
                    laozi = dict_p_1.keys()
                    fuzi = dict_p_2.keys()
                    for lao in laozi:
                        if lao in fuzi:
                            dict_p_2[lao] = dict_p_2[lao]+dict_p_1[lao]
                        else:
                            dict_p_2[lao] = dict_p_1[lao]
            dict_p = dict_p_2
        #print(dict_p)
        r2 = path[len(path)-1]
        dict_p_1 = {}
        keys = dict_p.keys()
        for k in keys:
            dict_p_1[k] = 0
            for record in tx.run(e):
                dict_p_1[record['m']['name']] = 1
            e = s + '-[{relation}]->'.format(relation=r2) + r
            n = 0
            for record in tx.run(e):
                n += 1
            Eq = n
            if Eq == 0:
                l = dict_p_1.keys()
                for m in l:
                    dict_p_1[m] = 0
            else:
                l = dict_p_1.keys()
                for m in l:
                    dict_p_1[m] = float(dict_p_1[m] / Eq) * dict_p[k]
            dict_p[k] = dict_p_1
        # print(dict_p)
        values = dict_p.values()
        for value in values:
            for v in value.values():
                p = p + v
        return p
    if(len(path)==1):
        key = dict_p.keys()
        if end in key:
            p = dict_p[end]
        return p
    if len(path)==2:
        r1 = path[1]
        s = 'MATCH (n:Word{name})'.format(name='{name:\'' + start + '\'}')
        t = '(m:Word{name_1}) RETURN n'.format(name_1='{name:\'' + end + '\'}')
        e = s+'-[{relation}]->'.format(relation=r1)+t
        dict_p_1={}
        keys = dict_p.keys()
        for k in keys:
            dict_p_1[k] = 0
            for record in tx.run(e):
                dict_p_1[k] = 1
            e = s + '-[{relation}]->'.format(relation=r1) + r
            n = 0
            for record in tx.run(e):
                n += 1
            Eq = n
            l = dict_p_1.keys()
            for m in l:
                dict_p_1[m] = float(dict_p_1[m] / Eq) * dict_p[k]
            dict_p[k] = dict_p_1
       # print(dict_p)
        #print(dict_p)
        values = dict_p.values()
        for value in values:
            for v in value.values():
                p = p+v
        return p

if __name__=='__main__':
    #main('训练集.txt','p.txt')
    main('测试集.txt','q.txt')

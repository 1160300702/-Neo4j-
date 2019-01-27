import re
from neo4j import GraphDatabase
import numpy as np
import crowdSourcing
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","2648361987"))
def add_relation(tx, view,des,relation):
    s = 'MERGE (a)-[:'
    s1 = ']->(b)'
    str = '{0} {1} {2}'.format(s, relation, s1)
    tx.run("MERGE (a:Word {name:$name}) "
           "MERGE (b:Word {name:$name_1})" +
           str,
           name=view, name_1=des)
def add_node(tx,names):
    s = 'MERGE (a:Word{name:$name})'
    tx.run(s,name=names)
def search(tx,names):#查询一个节点和与之相连的所有节点，以文字形式展示
    s = 'MATCH (a:Word{name:$name})-[r]->(b) RETURN a,b,r'
    for record in tx.run(s,name=names):
        s1 = str(record['a']['name'])
        s2 = str(record['b']['name'])
        r = str(record['r'])
        r = r.strip().split(' ')
        r = r[len(r)-2]
        r = r.strip().split('=')
        r = r[1]
        r = r[1:len(r) - 1]
        print(s1+'-'+'['+r+']'+'->'+s2)
def search_deep(tx,names,number):
    s = 'MATCH p=(n:Word{name})-[*1..{num}]->(m) RETURN NODES(p),RELATIONSHIPS(p)'.format(num=number,
                                                                                                       name='{name:\'' + names + '\'}')
    for record in tx.run(s):
        j = len(record['NODES(p)'])
        if j < len(record['RELATIONSHIPS(p)']):
            j = len(record['RELATIONSHIPS(p)'])
        for i in range(j):
            if (i < len(record['NODES(p)'])):
                #file.writelines(record['NODES(p)'][i]['name'] + " ")
                 print(record['NODES(p)'][i]['name'],end='')
            if (i < len(record['RELATIONSHIPS(p)'])):
                relation = str(record['RELATIONSHIPS(p)'][i])
                relation = relation.split(' ')
                relation = relation[len(relation) - 2]
                #file.writelines(relation + " ")
                relation = relation.strip().split('=')
                relation = relation[1]
                print('-'+'['+relation[1:len(relation)-1]+']'+'->',end='')
        #file.writelines("\n")
        print()
    #查询一个节点和与之相连的number层的所有路径，以文字形式表示

def worker(node1,node2,anwsers,relation):
    i = np.random.randint(0, 100)
    if i<70:
        return  anwsers
    else:
        return ~anwsers
def inference(node1,node2,relation,anwsers):
    l = []
    for i in range(10):
        l.append(worker(node1,node2,anwsers,relation))
    anwser = crowdSourcing.most(l)
    return anwser#采用众包推理得出两个节点之间是否有某种关系
#删除节点以及与该节点相关的关系
def delete_node(tx,names):
    s = 'MATCH (n:Word{name:$name}) DETACH DELETE n'
    tx.run(s,name = names)
def add_property(tx,property_name,property,names):
    s = 'MATCH (n {name:$name}) SET n += {propertys} RETURN n'
    s = s.format(propertys = '{'+property_name+':'+str(property)+'}')
    tx.run(s,name = names)
def create_graph(fileName=''):
    if fileName=='':
        return
    f = open(fileName, "r", encoding="utf-8")
    lines = f.readlines()
    i = 0
    q = re.compile("\n")
    p = re.compile('<')
    z = re.compile('>')
    j = 0
    for line in lines:
        line = q.sub("", line)
        line = line.split(' ')
        #print(line)
        start = line[0]
        end = line[2]
        relation = line[1]
        relation = relation.split('#')
        relation = relation[1]
        start = start.split('/')
        start = start[len(start)-1]
        start = z.sub('',start)
        end = end.split('/')
        end = end[len(end)-1]
        end = z.sub('',end)
        relation = z.sub('',relation)
        #print(start,relation,end)
        with driver.session() as session:
            session.write_transaction(add_relation, start, end, relation)
            #session.write_transaction(add_relation,line[2],line[0],line[1])
        j+=1
#删除两个节点之间的关系
def delete_relation(tx,relation,name1,name2):
    s = 'MATCH (a:Word{name_1})-[{relations}]->(b:Word{name_2}) DELETE r'.format(name_1 = '{name:'+'\''+name1+'\''+'}',relations = 'r:'+relation,name_2='{name:'+'\''+name2+'\''+'}')

    print(s)
    tx.run(s,name_1=name1,name_2=name2,relations = relation)
def menu():
    print('Welcome to Knowledge Graph System!')
    print('Here is the menu:')
    print('0:get the help')
    print('1:add node')
    print('2:add relation in two nodes')
    print('3:delete node')
    print('4:delete relation')
    print('5:inference relation between two nodes')
    print('6:add property to a node')
    print('7:create a graph from a file')
    print('8:search a node with the nodes that it can reach')
    print('9:search a node and the path to the nodes it can reach')
    print('10:exit')
if __name__ == '__main__':
    while(True):
        menu()
        print('Please input your order')
        order = int(input())
        if order == 0:
            menu()
        elif order == 1:
            name = input('Please input the name of the node')
            with driver.session() as session:
                session.write_transaction(add_node,name)
            print('add successsfully')
        elif order == 2:
            name1,name2,relation = input('请输入添加关系的头结点、尾节点以及关系，请依序输入')
            with driver.session() as session:
                session.write_transaction(add_relation,name1,name2,relation)
        elif order == 3:
            name = input('请输入需要删除节点的名称')
            with driver.session() as session:
                session.write_transaction(delete_node,name)
        elif order == 4:
            relation,name1,name2 = input('请输入需要删除的关系,以及关系的头结点和尾节点')
            with driver.session() as session:
                session.write_transaction(delete_relation,relation,name1,name2)
        elif order == 5:
            name1,name2,relation,anwser = input('请输入需要推理的头结点和尾节点，关系以及正确答案0或1')
            anwser = int(anwser)
            anw = inference(name1,name2,relation,anwser)
            if anw == 1:
                print('存在该关系')
            else:
                print('不存在')
        elif order == 6:
            property_name,property,name = input('请输入要添加的属性名称、属性值、节点')
            with driver.session() as session:
                session.write_transaction(add_property,property_name,property,name)
        elif order == 7:
            filename = input('请输入合理的文件名称')
            create_graph(filename)
        elif order == 8:
            name = input('请输入需要查询的节点的名称')
            with driver.session() as session:
                session.write_transaction(search,name)
        elif order == 9:
            name,number = input('请输入需要查询的节点和查询的深度')
            number = int(number)
            with driver.session() as session:
                session.write_transaction(search_deep,name,number)
        elif order == 10:
            break


    '''with driver.session() as session:
       #session.read_transaction(search_deep,'作家',3)
        #session.read_transaction(search,'作家')
        #session.write_transaction(delete_relation,'subClassOf','作家','人物')
        session.write_transaction(add_relation,'作家','人物','subClassOf')
        session.read_transaction(search,'作家')'''

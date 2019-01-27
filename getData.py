from neo4j import GraphDatabase
import re
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "2648361987"))
def nodes(tx,relation,file1,file2,number):
    #q = re.compile("''dsa")
    s = "MATCH (n:Word)-[r:"+relation+"]->(m:Word) RETURN count(n)"
    st = "MATCH (n:Word)-[r:"+relation+"]->(m:Word) RETURN m,n LIMIT "+str(number)
    i = 0
    for record in tx.run(st):
        if i>4*number/5:
            file2.writelines("start: "+record['n']['name']+" "+"relation: "+relation+" "+"end: "+record['m']['name']+"\n")
        else:
            file1.writelines(
                "start: " + record['n']['name'] + " " + "relation: " + relation + " " + "end: " + record['m'][
                    'name'] + "\n")
            i += 1
def search_path(tx,l,start,end,file):
    if(l==1):
        s = 'MATCH p=(n:Word{name})-[*1]->(m:Word{name_1}) RETURN NODES(p),RELATIONSHIPS(p)'.format(name='{name:\''+start+'\'}',name_1='{name:\''+end+'\'}')
    else:
        s = 'MATCH p=(n:Word{name})-[*1..{num}]->(m:Word{name_1}) RETURN NODES(p),RELATIONSHIPS(p)'.format(num = l,name='{name:\''+start+'\'}',name_1='{name:\''+end+'\'}')
    #print(s)
    for record in tx.run(s):
        j = len(record['NODES(p)'])
        if j<len(record['RELATIONSHIPS(p)']):
            j = len(record['RELATIONSHIPS(p)'])
        for i in range(j):
            if(i<len(record['NODES(p)'])):
                file.writelines(record['NODES(p)'][i]['name']+" ")
                #print(record['NODES(p)'][i]['name'])
            if(i<len(record['RELATIONSHIPS(p)'])):
                relation = str(record['RELATIONSHIPS(p)'][i])
                relation = relation.split(' ')
                relation = relation[len(relation)-2]
                file.writelines(relation+" ")
                #print(relation[6:9])
        file.writelines("\n")
        #print("#################")
def all_nodes(tx,relation,file,l):
    j = 0
    s = "MATCH (n:Word)-[r:" + relation + "]->(m:Word) RETURN m,n"
    for record in tx.run(s):
        j+=1
        if j>4000:
            break
        with driver.session() as session:
            session.read_transaction(search_path,l,record['n']['name'],record['m']['name'],file)
def getTemple(file,l,relation):
    with driver.session() as session:
        session.read_transaction(all_nodes,relation,file,l)
def getData(tx,outputfile,relation,number):
    file = open(outputfile,'w',encoding='utf-8')
    st = "MATCH (n:Word)-[r:" + relation + "]->(m:Word) RETURN m,n LIMIT " + str(number)
    for record in tx.run(st):
            file.writelines(
                "start: " + record['n']['name'] + " " + "relation: " + relation + " " + "end: " + record['m'][
                    'name'] + "\n")
if __name__ == '__main__':
    file = open('训练集.txt','w',encoding='utf-8')
    file1 = open('测试集.txt','w',encoding='utf-8')
    with driver.session() as session:
        session.read_transaction(nodes, 'type', file,file1,500)
        session.read_transaction(nodes,'subClassOf',file,file1,500)
    f = open("特征集.txt", 'w', encoding='utf-8')
    getTemple(f,3,'type')
    with driver.session() as session:
        session.read_transaction(getData,'test.txt','type',2000)
        session.read_transaction(getData,'test_s.txt','subClassOf',2000)
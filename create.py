import re
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","2648361987"))
def add_relation(tx, view,des,relation):
    s = 'MERGE (a)-[:'
    s1 = ']->(b)'
    # relation = relation[1:len(relation)]
    print(relation)
    '''relation = re.split(":",relation)
    m = ""
    for r in relation:
        m = m+" "+r'''
    str = '{0} {1} {2}'.format(s, relation, s1)
    tx.run("MERGE (a:Word {name:$name}) "
           "MERGE (b:Word {name:$name_1})" +
           str,
           name=view, name_1=des)


def chuli(fileName):
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
        if j>10000:
            break


if __name__ == '__main__':
    chuli('data/instp.txt')
    chuli('data/taxon.txt')
    chuli('data/inssp.txt')

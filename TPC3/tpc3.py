import sys
import re
from tabulate import tabulate
from collections import Counter
import json

def exercicio1():
    i=0
    count = 0
    anos = list()
    frequencias = list()

    #extrai as datas de todos os processos
    file1 = open('processos.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        count += 1
        linha = line.split("::")
        if len(line)>1:
            data = linha[1]
            ano = data.split("-")[0]
            anos.append(int(ano))

    #calcula a frequência de processos por ano 
    for ano in range(min(anos),max(anos)):
        conta = anos.count(ano)
        frequencias.append((ano,conta))
        i+=1
        ano+=1
    
    print(tabulate(frequencias,tablefmt="pretty"))
    
def exercicio2():
    er=re.compile(r'([^0-9.]*)', re.I)
    nomes = list()

    #extrai os nomes e ano de todos os processos
    file1 = open('processos.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        linha = line.split("::")
        if len(line)>1:
            data = linha[1]
            ano = data.split("-")[0]
            for a in linha:
                if re.fullmatch(er,a) and len(a)>1:nomes.append((int(ano),a))

    res = list(zip(*nomes))
    inf = int(min(res[0])) #limite inferior séculos
    sup = int(max(res[0])) #limite superior séculos
    inf=int(round(inf/100,0))*100
    sup=int(round(sup/100,0))*100

    #0->17,1->18... cada indice é uma lista de tuplos (nomes próprios,apelido)
    frequencias = list() 
    i=inf
    while(i<=sup):
        primeiros=list() #primeiros nomes por seculo
        ultimos=list() #ultimos nomes por seculo
        for a,b in nomes:
            first=b.split()[0] #nome próprio
            last=b.split()[-1] #apelido
            if(a>=i and a<=(i+100)):
                primeiros.append((first))
                ultimos.append((last))
        frequencias.append((primeiros,ultimos))
        i=i+100

    #ordenar por ocorrencias e obter os 5 mais usados
    final=list()
    for a,b in frequencias:
        p=dict()
        u=dict()
        for x in a:
            n=a.count(x)
            p[x]=n
        for y in b:
            n=b.count(y)
            u[y]=n
        
        p=sorted(p.items(), key=lambda x: x[1], reverse=True)[:5]
        u=sorted(u.items(), key=lambda x: x[1], reverse=True)[:5]
        final.append((p,u))
        
    #imprimir tabela final
    r = list()
    l=int(inf/100+1)
    for a,b in final:
        r.append((l,a,b))
        l+=1
    print(tabulate(r,tablefmt="pretty"))

def exercicio3():
    er=re.compile(r'(Ti(o|a))|(Irmao)|(Prim(o|a))|(Pai)|(Filho)|(Mae)|(Net(o|a))|(Av(o|a))|(Irma)', re.I)
    r = list()

    #extrai os tipos de relaçao de todos os processos para r
    file1 = open('processos.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        linha = line.split("::")
        if len(line)>1:
            a = linha[5].split(",")
            del a[0]
            if len(a)>0:
                for x in a:
                    c=x.split(".")
                    if re.match(er,c[0]) :r.append(c[0])

    #criar dicionario com (tipo de relacao,número de ocorrencias)
    res=dict()
    for a in r:
        c = r.count(a)
        res[a]=c
    
    #imprimir tabela final ordenada por ordem alfabética
    r=sorted(zip(res.keys(),res.values()))
    print(tabulate(r,tablefmt="pretty"))

def exercicio4():
    er=re.compile(r'(\n)', re.I)
    file1 = open('processos.txt', 'r')
    Lines = file1.readlines()[:20] #so guarda as primeiras 20 linhas

    r=dict()
    i=0
    for line in Lines:
        linha = line.split("::")
        #remover campos vazios
        linha = list(filter(None, linha))
        #remove campos com "\n"
        for a in linha:
            if re.match(er,a):linha.remove(a)
        if len(line)>1:
            r[i]=linha
            i+=1
    
    #cria json
    with open("resultado.json", "w") as outfile:
        json.dump(r, outfile)


def main():
    exercicio1()
    exercicio2()
    exercicio3()
    exercicio4()
    return 0

if __name__ == "__main__":
    main()

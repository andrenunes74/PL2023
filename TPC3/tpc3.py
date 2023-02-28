import sys
import re
from tabulate import tabulate

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
    
def main():
    exercicio1()
    return 0

if __name__ == "__main__":
    main()
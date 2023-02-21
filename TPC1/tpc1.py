import re
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


#lista de strings pra guardar informaçao lida
#distribuicões sao apenas uma lista de tuplos ou mesmo um dicionário
def ponto1(lista):
    i = 1    
    with open('/Users/andrenunes/Desktop/UNI/2semestre/PL/PL2023/TPC1/myheart.csv') as file:
        data = file.read().splitlines()

    while(i<len(data)):
        lista.append(data[i])
        #print(data[i])
        i+=1
    
    print("Total de entradas:"+str(len(lista)))

def ponto2(data):
    homens = 0
    mulheres = 0
    totalH = 0
    totalM = 0
    i=0

    while(i<len(data)):
        if(re.search("\d+,M,\d+,\d+,\d+,1",data[i])): homens+=1
        if(re.search("\d+,F,\d+,\d+,\d+,1",data[i])): mulheres+=1
        if(re.search("M",data[i])): totalH+=1
        if(re.search("F",data[i])): totalM+=1
        i+=1

    print("Percentagem de homens doentes: " + str(round((homens/totalH*100),2))+"%")
    print("Percentagem de mulheres doentes: " + str(round((mulheres/totalM*100),2))+"%")

def ponto3(lista):
    idades = [0] * 10
    total = [0] * 10
    i=1

    while(i<len(lista)):
        if(re.search("3[0-4],.,\d+,\d+,\d+,1",lista[i])):idades[0]+=1
        if(re.search("3[5-9],.,\d+,\d+,\d+,1",lista[i])):idades[1]+=1
        if(re.search("4[0-4],.,\d+,\d+,\d+,1",lista[i])):idades[2]+=1
        if(re.search("4[5-9],.,\d+,\d+,\d+,1",lista[i])):idades[3]+=1
        if(re.search("5[0-4],.,\d+,\d+,\d+,1",lista[i])):idades[4]+=1
        if(re.search("5[5-9],.,\d+,\d+,\d+,1",lista[i])):idades[5]+=1
        if(re.search("6[0-4],.,\d+,\d+,\d+,1",lista[i])):idades[6]+=1
        if(re.search("6[5-9],.,\d+,\d+,\d+,1",lista[i])):idades[7]+=1
        if(re.search("7[0-4],.,\d+,\d+,\d+,1",lista[i])):idades[8]+=1
        if(re.search("7[5-9],.,\d+,\d+,\d+,1",lista[i])):idades[9]+=1
        if(re.search("3[0-4],.,\d+,\d+,\d+,\d",lista[i])):total[0]+=1
        if(re.search("3[5-9],.,\d+,\d+,\d+,\d",lista[i])):total[1]+=1
        if(re.search("4[0-4],.,\d+,\d+,\d+,\d",lista[i])):total[2]+=1
        if(re.search("4[5-9],.,\d+,\d+,\d+,\d",lista[i])):total[3]+=1
        if(re.search("5[0-4],.,\d+,\d+,\d+,\d",lista[i])):total[4]+=1
        if(re.search("5[5-9],.,\d+,\d+,\d+,\d",lista[i])):total[5]+=1
        if(re.search("6[0-4],.,\d+,\d+,\d+,\d",lista[i])):total[6]+=1
        if(re.search("6[5-9],.,\d+,\d+,\d+,\d",lista[i])):total[7]+=1
        if(re.search("7[0-4],.,\d+,\d+,\d+,\d",lista[i])):total[8]+=1
        if(re.search("7[5-9],.,\d+,\d+,\d+,\d",lista[i])):total[9]+=1
        i+=1
    
    lis = zip(idades,total)
    x = 30
    r = list()
    for a,b in lis:
        x+=5
        r.append(round((a/b*100),2))

    xpoints = np.array([30,35,40,45,50,55,60,65,70,75])
    ypoints = np.array(r)

    plt.plot(xpoints, ypoints)
    plt.xlabel("Idades")
    plt.ylabel("Percentagem de doentes")   
    plt.show()

    labels = list()
    for label in xpoints:
        aux = label + 4
        labels.append("["+str(label)+"-"+str(aux)+"]")
    
    sizes = ypoints
    explode = [0.3]*len(xpoints)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.xlabel("Idades")
    plt.ylabel("Percentagem de doentes")    
    plt.show()

    print(" Idades | Percentagem de doentes")
    print(tabulate(zip(labels,ypoints),tablefmt="pretty"))

def ponto4(lista):
    i=1
    col = list()
    do = list()
    while(i<len(lista)):
        mylist = lista[i].split(",")
        i+=1
        if(mylist[5]=='1'):
            col.append(mylist[3])

    contador=0
    lim=0
    j=0
    final = [0]*40

    while(contador<len(col)):
        for a in col:
            if(lim<=int(a)<=lim+10):
                contador+=1
                final[j]+=1

        lim+=10
        j+=1

    z=0         
    s = sum(final)
    x = list()   
    y = list()
    for a in final:
        if((a/s*100)>0):
            x.append("["+str(z)+"-"+str(z+10)+"]")
            y.append(str(round((a/s*100),2)))
            z+=10
    
    labels = x
    sizes = y
    explode = [0.3]*len(x)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.xlabel("Níveis de colestrol")
    plt.ylabel("Percentagem de doentes")  
    plt.show()

    print("Nvl.colestrol | %.doentes ")
    print(tabulate(zip(labels,y), tablefmt="pretty"))

    
def main():
    lista = list()
    print("Exercício 1:--------------------------------")
    ponto1(lista)
    print("Exercício 2:--------------------------------")
    ponto2(lista)
    print("Exercício 3:--------------------------------")
    ponto3(lista)
    print("Exercício 4:--------------------------------")
    ponto4(lista)

if __name__ == "__main__":
    main()
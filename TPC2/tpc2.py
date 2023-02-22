import sys
import re

def main():
    soma = 0
    flag = 0

    print("--------------------------------------------------------------------------------------")
    print("||||          Soma todas as sequências de dígitos que encontra num texto          ||||")
    print("|||| :q -> sair | Off -> desliga contador | On -> liga contador | = -> soma atual ||||")
    print("||||                         Insira uma entrada de texto:                         ||||")
    print("--------------------------------------------------------------------------------------")

    for line in sys.stdin:
        if re.search(":q",line): break
        if re.search("Off",line): flag = 1
        if re.search("On",line): flag = 0
        if re.search("=",line): print("Soma atual:" + str(soma))
        if re.search(".*\d+.*",line) and flag == 0:
            i=0
            while(i<len(line)):
                if line[i].isdigit(): soma+=int(line[i])
                i+=1

    print("Resolvido! Soma:" + str(soma))

if __name__ == "__main__":
    main()
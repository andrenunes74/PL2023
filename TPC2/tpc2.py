import sys
import re

def main():
    soma=0
    flag=0
    on=re.compile(r'on', re.I)
    off=re.compile(r'off', re.I)

    file1 = open(str(sys.argv[1]), 'r')
    Lines = file1.readlines()
    for line in Lines:
        i=0
        flag=0
        numero=''
        while(i<len(line)):
            if line[i].isdigit() and line[i+1].isdigit() and flag==0:numero=numero+line[i]
            if line[i].isdigit() and not(line[i+1].isdigit()) and flag==0 and len(numero)!=0:soma+=int(numero)
            if line[i]=='=':print(soma)
            if i>=2:
                if re.match(on,line[i-1]+line[i]):flag=0
                if re.match(off,line[i-2]+line[i-1]+line[i]):flag=1
            i+=1
        
    print("Soma total: " + str(soma))

if __name__ == "__main__":
    main()
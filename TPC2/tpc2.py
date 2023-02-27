import sys
import re

def main():
    soma=0
    flag=0
    on=re.compile(r'on', re.I)
    off=re.compile(r'off', re.I)

    for line in sys.stdin:
        i=0
        flag=0
        while(i<len(line)):
            if line[i].isdigit() and flag==0:soma+=int(line[i])
            if line[i]=='=':print(soma)
            if i>=2:
                if re.match(on,line[i-1]+line[i]):flag=0
                if re.match(off,line[i-2]+line[i-1]+line[i]):flag=1
            i+=1
        if line[0]+line[1]==":q":break

if __name__ == "__main__":
    main()
import re
import sys
import shutil

def isNumber(str):
	if re.match(r"\d+\.*\d*", str): return True
	else: return False

def isList(str):
	if re.match(r'^\[(\d+,)*\d+\]$', str): return True
	else: return False

def isCSV(str):
	if re.match(r'\w*/*\w+\.csv', str): return True
	else: return False

def isValid(header):
	regex = r'^([\w ]+,)+[\w ]+'
	match = re.search(r'{(?P<min>\d+)(,(?P<max>\d+))?}(::(?P<func>\w+))?',header)
	
	if match and match.group('max') and match.group('min') and match.group('func'):
		regex += r'{\d+,\d+}' + r'::(sum|media)'
		for _ in range(0,int(match.group('max'))):
			regex += r','
	elif match and match.group('max') and match.group('min'):
		regex += r'{\d+,\d+}'
		for _ in range(0,int(match.group('max'))):
			regex += r','
	elif match and match.group('min') and match.group('func'):
		regex += r'{\d+}' + r'::(sum|media)'
		for _ in range(0,int(match.group('min'))):
			regex += r','
	elif match and match.group('min'):
		regex += r'{\d+}'
		for _ in range(0,int(match.group('min'))):
			regex += r','
	else: pass
	
	regex += r'$'
	if re.match(regex,header): return True
	else: return False
	
def groupNameWord(word):
	return r'(?P<'+word+r'>(((\".*\")*[\w ]+(\".*\")*))+),'

def groupNameInt2Args(word,min,max):
	res = r''
	for i in range(1,min+1):
		if i == max:
			res+=r'(?P<'+word+str(i)+r'>\d+)'
		else:
			res+=r'(?P<'+word+str(i)+r'>\d+),'
	
	for i in range(min+1,max+1):
		if i == max:
			res+=r'(?P<'+word+str(i)+r'>\d+)?'
		else:
			res+=r'(?P<'+word+str(i)+r'>\d+)?,'
	return res

def groupNameInt1Arg(word,min):
	res = r''
	for i in range(1,min+1):
		if i == min:
			res+=r'(?P<'+word+str(i)+r'>\d+)'
		else:
			res+=r'(?P<'+word+str(i)+r'>\d+),'
	return res

def buildRegex(header):
	pattern = re.compile(r'((?P<nameP>\w+){(?P<min>\d+)(,(?P<max>\d+))?}(::(?P<func>\w+))?)|(?P<name>\w+),?')

	listName = []
	regex = r'^'
	tup = tuple()
	flag = 2

	for match in re.finditer(pattern,header):
		name = match.group('name')
		if name:	
			listName.append(name)

	for match in re.finditer(pattern,header):
		name = match.group('nameP')
		minimum = match.group('min')
		maximum = match.group('max')
		func = match.group('func')
		if name and minimum and maximum and func:
			tup = tuple((name,minimum,maximum,func))
			listName.append(tup)
			flag = 0
		elif name and minimum and maximum:
			tup = tuple((name,minimum,maximum))
			listName.append(tup)
			flag = 0
		elif name and minimum and func:
			tup = tuple((name,minimum,minimum,func))	
			listName.append(tup)
			flag = 0
		elif name and minimum:
			tup = tuple((name,minimum))
			listName.append(tup)
			flag = 1

	for name in listName:
		if isinstance(name,str):
			regex+=groupNameWord(name)
		elif isinstance(name,tuple) and flag == 0:
			regex+=groupNameInt2Args(name[0],int(name[1]),int(name[2]))
		elif isinstance(name,tuple) and flag == 1:
			regex+=groupNameInt1Arg(name[0],int(name[1]))
			
	aux = [] 	
	if flag != 2:
		aux = list(tup)
	else:
		aux.append('')
	regex += r'$'
	regex = re.sub(r',\$', r'$', regex)
	aux[0] = regex

	return aux

def collapseItems(list,limit,function):
	i = 0
	limit = int(limit)
	aux = []
	name = ''
	for item in reversed(list):
		if i == limit:
			break
		else:
			aux.append(item)
			i = i + 1
	aux2 = []
	for item in aux:
		if item[1] is not None: 
			aux2.append(int(item[1]))
			name = item[0]
	name = name.rstrip(name[-1])
	value = 0
	if function == 'media':
		value = sum(aux2) / len(aux2)
	elif function == 'sum':
		value = sum(aux2)
		 
	i = 0
	newlist = []	
	for item in list:
		if i == len(list)-limit:
			break
		else:
			newlist.append(item)
			i = i + 1
	newlist.append((name,str(value)))	 
	return newlist

def dicItemToJson(item):
	jsonItem = ''
	if (item[1] and isNumber(item[1])) or item[1] and isList(item[1]):
		jsonItem = '\t\t"' + item[0] + '": ' + item [1] + ',\n'
	elif item[1]:
		jsonItem = '\t\t"' + item[0] + '": "' + item [1] + '",\n'
	return jsonItem

def dicToJsonLine4Args(dic,function,max):
	jsonLine = '\t{\n'
	list = dic.items()
	list = collapseItems(list,max,function)
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t},\n'
	return jsonLine

def dicToJsonLineLast4Args(dic,function,max):
	jsonLine = '\t{\n'
	list = dic.items()
	list = collapseItems(list,max,function)
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t}\n'
	return jsonLine

def dicListToJsonStr4Args(dicList,function,max):
	jsonStr = '[\n'
	size = len(dicList)
	i = 1
	for dic in dicList:
		if i == size: 
			jsonStr = jsonStr + dicToJsonLineLast4Args(dic,function,max)
		else:
			jsonStr = jsonStr + dicToJsonLine4Args(dic,function,max)
			i = i+1
	jsonStr = jsonStr + ']'
	return jsonStr

def toListStr(list):
	res = '['
	for item in list:
		res = res + str(item) + ','
	res = res + ']'
	res = re.sub(r',]', "]", res)
	return res

def collapseItems3Args(list,limit):
	i = 0
	limit = int(limit)
	aux = []
	name = ''
	for item in reversed(list):
		if i == limit:
			break
		else:
			aux.append(item)
			i = i + 1
			
	aux2 = []
	for item in aux:
		if item[1]: 
			aux2.append(int(item[1]))
			name = item[0]
			
	name = name.rstrip(name[-1])
	value = toListStr(aux2)
	i = 0
	newlist = []	
	for item in list:
		if i == len(list)-limit:
			break
		else:
			newlist.append(item)
			i = i + 1
	newlist.append((name,str(value)))	 
	return newlist

def dicToJsonLine3Args(dic,max):
	jsonLine = '\t{\n'
	list = dic.items()
	list = collapseItems3Args(list,max)
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t},\n'
	return jsonLine

def dicToJsonLineLast3Args(dic,max):
	jsonLine = '\t{\n'
	list = dic.items()
	list = collapseItems3Args(list,max)
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t}\n'
	return jsonLine

def dicListToJsonStr3Args(dicList,max):
	jsonStr = '[\n'
	size = len(dicList)
	i = 1
	for dic in dicList:
		if i == size: 
			jsonStr = jsonStr + dicToJsonLineLast3Args(dic,max)
		else:
			jsonStr = jsonStr + dicToJsonLine3Args(dic,max)
			i = i+1
	jsonStr = jsonStr + ']'
	return jsonStr

def collapseItems2Args(list,limit):
	i = 0
	limit = int(limit)
	aux = []
	name = ''
	for item in reversed(list):
		if i == limit:
			break
		else:
			aux.append(item)
			i = i + 1
			
	aux2 = []
	for item in aux:
		if item[1]: 
			aux2.append(int(item[1]))
			name = item[0]
			
	name = name.rstrip(name[-1])
	value = toListStr(aux2)
	i = 0
	newlist = []	
	for item in list:
		if i == len(list)-limit:
			break
		else:
			newlist.append(item)
			i = i + 1
	newlist.append((name,str(value)))	 
	return newlist

def dicToJsonLine2Args(dic,max):
	jsonLine = '\t{\n'
	list = dic.items()
	list = collapseItems2Args(list,max)
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t},\n'
	return jsonLine

def dicToJsonLineLast2Args(dic,max):
	jsonLine = '\t{\n'
	list = dic.items()
	list = collapseItems3Args(list,max)
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t}\n'
	return jsonLine

def dicListToJsonStr2Args(dicList,min):
	jsonStr = '[\n'
	size = len(dicList)
	i = 1
	for dic in dicList:
		if i == size: 
			jsonStr = jsonStr + dicToJsonLineLast2Args(dic,min)
		else:
			jsonStr = jsonStr + dicToJsonLine2Args(dic,min)
			i = i+1
	jsonStr = jsonStr + ']'
	return jsonStr

def dicToJsonLine1Arg(dic):
	jsonLine = '\t{\n'
	list = dic.items()
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t},\n'
	return jsonLine

def dicToJsonLineLast1Arg(dic):
	jsonLine = '\t{\n'
	list = dic.items()
	for item in list:
		jsonLine = jsonLine + dicItemToJson(item)
	jsonLine = jsonLine + '\t}\n'
	return jsonLine

def dicListToJsonStr1Arg(dicList):
	jsonStr = '[\n'
	size = len(dicList)
	i = 1
	for dic in dicList:
		if i == size: 
			jsonStr = jsonStr + dicToJsonLineLast1Arg(dic)
		else:
			jsonStr = jsonStr + dicToJsonLine1Arg(dic)
			i = i+1
	jsonStr = jsonStr + ']'
	return jsonStr


def main():
	args = sys.argv[1:]
	infile = open(args[0],"r",encoding = "utf8")
	
	if isCSV(args[0]):
		print("Converting " + args[0] + "...\n")
		header = infile.readline()
		
		if isValid(header):
			regexList = buildRegex(header)
			pattern = re.compile(regexList[0])
			patternReplace = re.compile(r',\n\t}')
			dicList = []
			jsonStr = ''
			for line in infile.readlines():
				for match in re.finditer(pattern,line):
					dic = match.groupdict()
					dicList.append(dic)
					
			if len(regexList) == 4:		
				jsonStr = dicListToJsonStr4Args(dicList,regexList[3],regexList[2])
			elif len(regexList) == 3: 
				jsonStr = dicListToJsonStr3Args(dicList,regexList[2])
			elif len(regexList) == 2:
				jsonStr = dicListToJsonStr2Args(dicList,regexList[1])		
			elif len(regexList) == 1:
				jsonStr = dicListToJsonStr1Arg(dicList)
				
			jsonStr = re.sub(patternReplace, "\n\t}", jsonStr)
			outname = re.sub(r'\.csv',r'.json',args[0])
			outfile = open(outname, "w",encoding = "utf8")
			outfile.write(jsonStr)
			outfile.close()
			x = outname.split("/")
			shutil.move(outname, "results/"+x[1])
			print("Converted to " + "results/"+x[1])
		else:
			print('Error in header')
	else:
		print('File is not a .csv')
		
	infile.close()

if __name__ == "__main__":
    main()
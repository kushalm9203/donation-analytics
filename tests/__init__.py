import pickle

with open('testData.txt', 'rb') as f:
	ptr = 0
	obj = ["dates", "recvId", "zipcode", "other", "donor"]
	objDict = {}
	i = 0
	objLst = []
	for line in f:
		objLst.append(line)
		# objLst = objDict.get(obj[ptr], [])
		# objLst.append(line)
		# objDict[obj[ptr]] = objLst
		# i += 1
		# if i == 3:
		# 	ptr += 1
		# 	i = 0

	with open('data.pkl', 'wb') as fOut:
		pickle.dump(objLst, fOut)






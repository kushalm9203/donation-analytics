import sys, os
import heapq
from collections import OrderedDict, deque
from datetime import datetime
import math
from config import inputPerc, inputCont, reqFields, outputRepDonors as outFile
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../tests")


def processPolitContrib():
	""" Main function that processes the data."""
	perc = readReqPercentile(inputPerc)	
	transDonDict = {}		# donor, zipcode -> receiver, year
	transRecvDict = {}		# receiver, year, zipcode -> amount

	# Store indices of the required fields
	# positions = getFieldNums()	
	positions = [0, 7, 10, 13, 14, 15]
	with open(inputCont, 'rb') as f_in:
		# f_in.next()			# skip the headers
		for line in f_in:
			try:
				try:
					recv, don, zipcode, tDate, tAmt = readAndCheckInput(line, positions) 

				# Skip record if invalid or not required
				except (ValueError, IndexError, TypeError) as e:
					continue

				donorDetails = transDonDict.get((don, zipcode))	

				# If new donor add to map; or if old, and current transaction
				# occurs in time before the stored transaction, replace 
				# stored with current transaction.		
				if not donorDetails or donorDetails[0] >= tDate.year:	 
					transDonDict[(don, zipcode)] = [tDate.year, recv]	

				# If old donor and current transaction occurs in time  
				# after stored transaction, it's a repeat donor.
				#
				# Add current transaction to the receiver's list of 
				# transactions with repeat donors from the zipcode 
				# for the year.
				else:
					updateRecvDict(transRecvDict, recv, tDate.year, zipcode, tAmt)

					# Get running percentile, total amount, number of transactions for receiver
					recvDetails = getRecvDetails(transRecvDict, recv, tDate.year, zipcode, perc)
					outputRepeatDonors(recvDetails, recv, tDate.year, zipcode)

			# Catch a malformed string in the record		
			except ValueError as e:	
				continue
				
def readReqPercentile(inputPerc):
	""" Read the percentile value from the input file percentile.txt."""
	with open(inputPerc, 'rb') as f_p:
		p = int(f_p.readline().rstrip())
		if 0 <= p <= 100:
			return p
		raise ValueError('input file contains invalid percentile value!')				

def getFieldNums():
	""" Get the positions of the required fields by reading the very first line."""
	fieldDict = {key: -1 for key in reqFields}
	with open(inputCont, 'rb') as f_in:
		fields = f_in.readline().rstrip().split('|')
		return [pos for pos in range(len(fields)) if fields[pos] in reqFields]

def readAndCheckInput(line, positions):	
	""" Parse a record from the input file and verify that the record is valid and required.""" 
	fieldElements = line.rstrip().split('|')
	recvId = fieldElements[positions[0]]
	donorName = fieldElements[positions[1]]
	zipCode = fieldElements[positions[2]][:5]
	transDate = datetime.strptime(fieldElements[positions[3]], "%m%d%Y")
	transAmt = int(fieldElements[positions[4]])
	indiv = not bool(fieldElements[positions[5]])
	if not (len(zipCode) >= 5 and donorName and transAmt and recvId and transDate <= datetime.now()): 
		raise ValueError 
	if not indiv:
		raise TypeError
	return recvId, donorName, zipCode, transDate, str(transAmt)

class Node:
	""" Each node of BST holding the amount of the transaction."""
	def __init__(self, ele, isRoot):
		self.ele = ele
		self.childNodes = 1
		self.left = None
		self.right = None
		self.totalAmt = None
		self.numTrans = None

		# If root, keep track of the amount and number of transactions for the
		# receiver with repeat donors.
		if isRoot:				
			self.totalAmt = ele
			self.numTrans = 1

def updateRecvDict(transRecvDict, recv, year, zipcode, amt):
	""" Update the value field of receiver's entry in the dictionary with the new transaction details."""
	root = transRecvDict.get((recv, year, zipcode))
	if not root:
		transRecvDict[(recv, year, zipcode)] = Node(amt, True) 
		return 
	insertNode(root, Node(amt, False))
	root.numTrans += 1
	root.totalAmt = float(root.totalAmt) + float(amt)
	return

def insertNode(root, newNode):
	""" Insert the node representing the new transaction's amount into the BST."""
	if not root:
		return None
	if newNode.ele <= root.ele:
		n = insertNode(root.left, newNode)
		if not n:
			root.left = newNode
	else:
		n = insertNode(root.right, newNode)
		if not n:
			root.right = newNode
	root.childNodes += 1
	return root

def getRecvDetails(transRecvDict, recv, year, zipcode, perc):
	""" Read the required details of the receiver's entry from the dictionary."""
	if (recv, year, zipcode) not in transRecvDict:
		return [int(round(round(float(transAmt), 2))), 1, float(transAmt)]
	root = transRecvDict[(recv, year, zipcode)]

	# Position of the node based on the required percentile 
	k = math.ceil(float(perc)/100 * root.numTrans)
	percAmt = getkth(root, k)
	if float(root.totalAmt).is_integer():
		root.totalAmt = int(root.totalAmt)
	return [int(round(round(float(percAmt), 2))), root.numTrans, int(root.totalAmt)]


def getkth(node, k):
	""" Get the kth smallest node from the BST."""
	if node.left:
		l = node.left.childNodes
	else:
		l = 0
	if l >= k:
		return getkth(node.left, k)
	if l + 1 == k:
		return node.ele
	else:
		return getkth(node.right, k - l - 1)

def outputRepeatDonors(recvDetails, recv, year, zipcode):
	""" Print the required details of transaction in output file."""
	outLine = (recv, zipcode, str(year), str(recvDetails[0]), str(recvDetails[2]), str(recvDetails[1]) + '\n')
	with open(outFile, 'a') as f_out:
		f_out.write("|".join(outLine))



processPolitContrib()











# def checkConstraints(d):
# 	try:
# 		dtFormat = datetime.strptime(d, "%m%d%Y")
# 	except ValueError:
# 		return False
# 	if not (recv and amt) or oth:
# 		return False
# 	if len(zipCode) < 5:
# 		return False

# def processPolitContrib():
# 	perc = readReqPercentile()	
# 	transDonDict = {}	# dictionary to map the donors to the filer (receiver) id and year
# 	transRecvDict = {}	# dictionary to map the filer (receiver) along with year, zipcode to transaction amounts
# 	positions = getFieldNums()	# dictionary to store positions of required fields
# 	with open(inputCont, 'rb') as f_in:
# 		f_in.next()
# 		for line in f_in:
# 			try:
# 				recv, don, zipcode, tDate, tAmt = readAndCheckInput(line)
# 			except ValueError, IndexError:
# 				continue

# 			recvData = None
# 			donorDetails = transDonDict.get((don, zipcode))
# 			if not donorDetails or donorDetails[0] >= tDate.year:
# 				transDonDict[(don, zipcode)] = [tDate.year, recv]
# 			else:
# 				updateRecvDict(transRecvDict, recv, tDate.year, zipcode, tAmt)
# 				recvDetails = getRecvDetails(transRecvDict, recv, tDate.year, zipcode, perc)
# 				outputRepeatDonors(recvDetails, recv, tDate.year, zipcode)
				
				
			
			# if (donorName, zipCode) in transDonDict:
			# 	if transDonDict[(donorName, zipCode)][0] < transDate.year:
			# 		recvData = updateRecvDataFindPerc(recvId, transDate.year, zipCode,  transRecvDict, transAmt)
			# 	else:
			# 		transDonDict[(donorName, zipCode)] = [transDate.year, recvId]
			# else:
				# transDonDict[(donorName, zipCode)] = [transDate.year, recvId]
			


		# f_in.next()
		# for line in f_in:
		# 	try:
		# 		fieldElements = line.rstrip().split('|')
		# 		recvId = fieldElements[fieldDict['CMTE_ID']]
		# 		donorName = fieldElements[fieldDict['NAME']]
		# 		zipCode = fieldElements[fieldDict['ZIP_CODE']][:5]
		# 		transDate = datetime.strptime(fieldElements[fieldDict['TRANSACTION_DT']], "%m%d%Y")
		# 		transAmt = fieldElements[fieldDict['TRANSACTION_AMT']]
		# 		indiv = not bool(fieldElements[fieldDict['OTHER_ID']])
		# 		if not (indiv and donorName and transAmt and recvId): continue 
		# 	except:
		# 		continue
			

# for trans in transactions:
# 	print trans
# 	currDon, currZip = trans[1:3]
# 	currTransDate = trans[3]
# 	currRecv = trans[0]
# 	currAmt = trans[4]
# 	donorDetails = donorDict[(currDon, currZip)]
# 	if donorDetails[0][0].year != donorDetails[-1][0].year:
# 		if currTransDate.year != donorDetails[0][0].year:								
# 			recvData = recvDict.get((currRecv, currTransDate.year, currZip), [])
# 			percAmt = updateRecvDataFindPerc(recvData, perc, currAmt)
# 			recvDict[(currRecv, currTransDate.year, currZip)] = recvData
# 			with open(absPath + '../output/repeat_donors.txt', 'a') as f_out:
# 				f_out.write("|".join((currRecv, currZip, str(currTransDate.year), percAmt, str(recvData[0]), str(recvData[1]) + "\n")))





# 	
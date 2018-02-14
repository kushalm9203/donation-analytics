import pytest
import pickle
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from config import currPath, inputCont
from donationanalytics import *

def setupTestData():
	with open('data.pkl', 'rb') as fIn:
		data = pickle.load(fIn)
		return data

testData = setupTestData()

def test_readReqPercentile():
	i = 0
	percLst = (50, 70, 105, -3)
	for num in percLst:
		i += 1
		with open('inputPerc' + str(i) + '.txt', 'wb') as fPerc:
			fPerc.write(str(num))
	for i in xrange(2):
		assert percLst[i] == readReqPercentile('inputPerc' + str(i+1) + '.txt')
	for i in xrange(2, 4):
		with pytest.raises(ValueError):
			readReqPercentile('inputPerc' + str(i+1) + '.txt')
class TestreadAndCheckInput:
	def test_readAndCheckInputSuccess(self):	
		a, b, c, d, e = readAndCheckInput(testData[0], [0, 7, 10, 13, 14, 15])
		assert a == "C00384516" 
		assert b == "SABOURIN, JOE"
		assert c == "02895"
		assert d == datetime.strptime("01312016", "%m%d%Y")
		assert e == "484"

	def test_readAndCheckInputMonthInvalid(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[1], [0, 7, 10, 13, 14, 15])

	def test_readAndCheckInputIncompleteDate(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[2], [0, 7, 10, 13, 14, 15])

	def test_readAndCheckInputIncompleteZipcode(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[3], [0, 7, 10, 13, 14, 15]) 

	def test_readAndCheckInputOtherPresent(self):
		with pytest.raises(TypeError):
			readAndCheckInput(testData[4], [0, 7, 10, 13, 14, 15]) 	

	def test_readAndCheckInputIncorrectRecord(self):
		with pytest.raises(IndexError):
			readAndCheckInput(testData[5], [0, 7, 10, 13, 14, 15]) 	

	def test_readAndCheckInputEmptyDonor(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[6], [0, 7, 10, 13, 14, 15]) 

	def test_readAndCheckInputEmptyAmt(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[7], [0, 7, 10, 13, 14, 15]) 

	def test_readAndCheckInputEmptyRecv(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[8], [0, 7, 10, 13, 14, 15]) 

	def test_readAndCheckInputFutureDate(self):
		with pytest.raises(ValueError):
			readAndCheckInput(testData[9], [0, 7, 10, 13, 14, 15])


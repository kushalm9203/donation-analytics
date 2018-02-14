import os

currPath = os.path.dirname(__file__)
inputPerc = currPath + '/../input/percentile.txt'
inputCont = currPath + '/../input/itcont.txt'
outputRepDonors = currPath + '/../output/repeat_donors.txt'
reqFields = set(('CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID'))
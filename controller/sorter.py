from collections import defaultdict
import sys

inFile = sys.argv[1]

ourD = defaultdict(list)
towrite = open("scalicaDumps/scalicaDumps.txt", 'w+')
with open (inFile, 'r') as inf:
	next(inf)
	for line in inf:
		string = line.split('\t')
		ourD[string[0]].append(string[1])


	for key in ourD:
		keyString = str(key) + "\t"

		toPrint = ", ".join(ourD[key])

		keyString += toPrint
		keyString = keyString.replace("\n", "").replace("\r", "")
		#print(keyString)
		towrite.write(keyString + "\n")
inf.close()
towrite.close()

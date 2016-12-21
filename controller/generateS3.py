
from random import randint
import sys

def generateFriends(users, maxFriends):
	rec=open('recommendations.txt', 'w')

	for i in range(users):
		friends=str(i)+" "
		size=randint(9, maxFriends)
		for x in range(size):
			friends+=str(randint(0, users))
			if(x != size-1):
				friends+=', '
		rec.write(friends+"\n")

	rec.close()

def main():
	args=sys.argv
	size=len(args)

	if(size<3):
		print("ERR missing arguments --ids --maxFriends")
		return

	if not args[1].isdigit() or not args[2].isdigit():
		print("ERR incorrect format")

	users=int(args[1])
	if(users<10 or users>500):
		print("ERR number of users shoule be between 10-500")
		return

	maxFriends=int(args[2])
	if(maxFriends<10 or maxFriends>100):
		print("ERR max should be between 10-100")
		return

	generateFriends(users, maxFriends)

main()

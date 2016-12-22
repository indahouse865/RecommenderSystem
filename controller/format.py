import sys
from collections import defaultdict
import re
#import boto

in1 = "./" + sys.argv[1]
in2 = "./" + sys.argv[2]
in3 = "./" + sys.argv[3]

#AWSAccessKeyId=AKIAJGYMLHBD4XHWBP2A
#AWSSecretKey=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

#BUCKET = 'recommenderdump'

#conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
#buck = conn.get_bucket(BUCKET)

#theD = defaultdict(list)
#writer = open("formatted.txt", "w+"):
    
#for key in buck.list(prefix='root/outputsrecSys1/', delimiter='/'):
#    if key.startswith("part-r-"):
#        argX = str(key)
#        f

def repRemove(x):
    x = x.strip()
    string = x.split('\t')
    first = string[0]
    if (len(string) > 1):
        lst = string[1].split(', ')
        unicL = []
        for ele in lst:
            if first == ele:
                lst.remove(ele)
            if ele not in unicL:
                unicL.append(ele)
        news = first + "\t"
        news += ", ".join(unicL)
        return news
    else:
        return x
        
        

    

writer = open("recommendations.txt", "w+")

with open (in1, 'r') as inn:
    for line in inn:
        line1 = line.replace("[", "]")
        line1 = line1.replace("]", " ")
        line1 = line1.replace(" ,", ",")
        line2 = repRemove(line1)
        writer.write(line2 + "\n")
#in1.close()

with open (in2, 'r') as inn2:
    for line in inn2:
        line1 = line.replace("[", "]")
        line1 = line1.replace("]", " ")
        line1 = line1.replace(" ,", ",")
        line2 = repRemove(line1)
        writer.write(line2 + "\n")
#in2.close()

with open (in3, 'r') as inn3:
    for line in inn3:
        line1 = line.replace("[", "]")
        line1 = line1.replace("]", " ")
        line1 = line1.replace(" ,", ",")
        line2 = repRemove(line1)
        writer.write(line2 + "\n")
#in3.close()
writer.close()



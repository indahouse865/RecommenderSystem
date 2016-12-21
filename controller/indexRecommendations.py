
from datetime import datetime
import redis
import re

recommendDB=redis.StrictRedis(host='localhost', port=6379, db=0)

def main():
  try:
    rec=open('recommendations.txt','r')
    for line in iter(rec):
      arr=re.findall('\d+', line)
      key=arr[0]
      arr=arr[1:]
      #print(key, arr[1:])
      recommendDB.set(key, arr)
    rec.close()
  except IOError:
    err=open('reports/Upload-Recommendations.txt', 'w')
    err.write(str(datetime.now())+'\nFailed To Open Recommendations File\n')
    err.close()

main()

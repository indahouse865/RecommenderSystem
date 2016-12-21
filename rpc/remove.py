
from __future__ import print_function
from datetime import datetime

import random
import time
import sys

import grpc
import scalica_pb2

err=open('reports/Remove-Errors.txt', 'w')

def RemoveRecommendation(stub, user, remove):
  queryInput=scalica_pb2.RemoveInfo(userId=user, removeId=remove)

  try:
    nothing = stub.RemoveRecommendation(queryInput)

  except Exception as e:
    err.write(str(datetime.now())+"\nERR: Connecting To RPC Server\n"+str(e)+"\n")
  return

def run():
  args=sys.argv
  size=len(args)

  if(size<3):
    err.write(str(datetime.now())+"\nERR: Not Enough Arguments Entered\n")
    return

  userId=args[1]
  removeId=args[2]
  if not userId.isdigit() or not removeId.isdigit():
    err.write(str(datetime.now())+"\nERR: Malformed Ids Is NAN\n")
    return

  userId=int(userId)
  removeId=int(removeId)
  if(userId < 0 or removeId < 0):
    err.write(str(datetime.now())+"\nERR: Non Id < 0\n")
    return

  channel = grpc.insecure_channel('localhost:50051')
  stub = scalica_pb2.RecommenderStub(channel)
  RemoveRecommendation(stub, userId, removeId)
  err.close()

if __name__ == '__main__':
  run()

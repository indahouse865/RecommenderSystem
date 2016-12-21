
from __future__ import print_function
from datetime import datetime

import random
import time
import sys

import grpc
import scalica_pb2

err=open('/home/ubuntu/scalica/rpc/reports/Client-Errors.txt', 'w')

def GetRecommendations(stub, user):
  userInput=scalica_pb2.UsersInfo(userId=user)

  try:
    recommendations = stub.GetRecommendations(userInput)

    if not recommendations:
      return

    print(recommendations)
    return recommendations

  except Exception as e:
    err.write(str(datetime.now())+"\nERR: Connecting To RPC Server\n"+str(e)+"\n")

  return

def run():
  args=sys.argv
  size=len(args)

  if(size<2):
    err.write(str(datetime.now())+"\nERR: No UserId Argument Entered\n")
    return

  userId=args[1]
  if not userId.isdigit():
    err.write(str(datetime.now())+"\nERR: Malformed UserId Is NAN\n")
    return

  userId=int(userId)
  if(userId<0):
    err.write(str(datetime.now())+"\nERR: Non User Id < 0\n")
    return

  channel = grpc.insecure_channel('localhost:50051')
  stub = scalica_pb2.RecommenderStub(channel)
  GetRecommendations(stub, userId)
  err.close()

if __name__ == '__main__':
  run()

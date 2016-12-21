
from concurrent import futures
from datetime import datetime

import time
import math
import grpc
import redis

import scalica_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
err=open('reports/Server-Errors.txt', 'w')
recommendDB=redis.StrictRedis(host='localhost', port=6379, db=0)

class RecommenderServicer(scalica_pb2.RecommenderServicer):
  def GetRecommendations(self, request, context):
    userId=request.userId

    if userId < 0:
      err.write(str(datetime.now())+"\nUserId is not valid client RPC should have checked this: unusual error\n")
      return scalica_pb2.UsersRecommendations(recommendations="")

    #grab the list based on the id
    recommendations=recommendDB.get(userId)
    print(recommendations)

    if not recommendations:
      return scalica_pb2.UsersRecommendations(recommendations="")

    return scalica_pb2.UsersRecommendations(recommendations=list(recommendations))

  def RemoveRecommendation(self, request, context):
    userId=request.userId
    removeId=request.removeId

    if (userId < 0 or removeId < 0):
      err.write(str(datetime.now())+"\nIds are not valid client RPC should have checked this: unusual error\n")
      return scalica_pb2.Nothing()

    remove=recommendDB.srem(userId, removeId)
    print(remove)

    return scalica_pb2.Nothing()

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  scalica_pb2.add_RecommenderServicer_to_server(RecommenderServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()

  start='\n'+str(datetime.now())+'\nSTARTING SERVER\n============================\n'
  print(start)
  err.write(start)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    stop=str(datetime.now())+'\nERR! SERVER CRASH\n'
    print(stop)
    err.write(stop)
    err.close()
    server.stop(0)

if __name__ == '__main__':
  serve()

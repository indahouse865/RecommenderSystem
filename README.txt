Reccomender System in Scalica

Access the site at: http://52.15.170.236:8000/micro/

Our project is entirely housed in the scalica folder

To login with any user:
username: userx      where x is almost any number from 1-200
password: password Leslie and David Zhu

redis - Our code for the implementation of redis used to cache recommendations for fetching - Michael

rpc - Defining our gRPC to handle fetching of recommendations when a user logs in - Micahel

controller - Our controller node that handles getting data to/from S3, formatting data before and after EMR, as well as invoking EMR periodically, and finally sending the recommendations to redis - Micahel and David Estrich

web - Has all the Django for the scalica app, the most changed file is web/scalica/micro/views, allowing users to see their recommendations Leslie and David Zhu

systems.java - The code for our Map Reduce program, which is in a jar on s3 and gets called by our aws cli commands. - David Estrich

env - simply the environment of scalica provided by Professor Yair

cron job - runs the scalica contrller.sh file every Saturday at 11:55pm - Michael

Other recources:

Amazon EC2 instance to host web app, controller, redis, and rpc

S3 buckets to house following list, map reduce jar, and EMR output - David E

Amazon Elastic Map Reduce - Created via aws cli code to run a map reduce job with hadoop using our jar file, and a formatted input file - David E

General distribution of tasks -

Michael Laucella - Create RPC for communication between service and recommendations, implement redis, create scalicaController.sh

David Estrich - Set up and manage all AWS infastructure. Implement Map Reduce and generating aws cli commands for controller node.

David Zhu - Register users and make connections between users, create powerpoint

Leslie Manrique - Implement changes in view file, register users and make connections

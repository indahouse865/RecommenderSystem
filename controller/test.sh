
aws s3 cp s3://recommenderdump/outputsrecSys/part-r-00000 part0
aws s3 cp s3://recommenderdump/outputsrecSys/part-r-00001 part1
aws s3 cp s3://recommenderdump/outputsrecSys/part-r-00002 part2

#aws s3 rm s3://recommenderdump/outputsrecSys --recursive

#python format.py part0 part1 part2
#python indexRecommendations.py  

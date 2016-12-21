#!/bin/bash

echo "Starting map reduce: $(date)"

#crash script if any error occurs at any point
set -e

cd scalica/controller

#if folder doesnt exist make it
if [ ! -d scalicaDumps ];
    then mkdir scalicaDumps
fi

echo "Dumping DB"

#sorted db dump
mysql -D scalica -u root -ppassword -e 'SELECT followee_id, follower_id FROM micro_following WHERE 1 ORDER BY followee_id' > ./scalicaDumps/scalicaDump.txt

echo "Preprocessing Info"

#format data for mapreduce
python preprocess.py scalicaDumps/scalicaDump.txt 
rm scalicaDumps/scalicaDump.txt

echo "Uploading To S3"

#send the db dump to s3
aws s3 sync ./scalicaDumps s3://recommenderdump/scalicaDumps

clusterId=$(aws emr create-cluster --auto-scaling-role EMR_AutoScaling_DefaultRole --applications Name=Hadoop --ec2-attributes '{"KeyName":"Scalica2","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-361f217c","EmrManagedSlaveSecurityGroup":"sg-d167b3b8","EmrManagedMasterSecurityGroup":"sg-df67b3b6"}' --service-role EMR_DefaultRole --enable-debugging --release-label emr-5.2.0 --log-uri 's3n://aws-logs-628208298039-us-east-2/elasticmapreduce/' --steps \
'[{"Args":["recSys.systems","s3://recommenderdump/scalicaDumps/scalicaDumps.txt","s3://recommenderdump/outputsrecSys/"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"s3://recommenderdump/recSys.jar","Properties":"","Name":"Custom JAR"}]' --name 'My cluster' --instance-groups \
'[{"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"InstanceGroupType":"MASTER","InstanceType":"m4.large","Name":"Master - 1"},{"InstanceCount":2,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"InstanceGroupType":"CORE","InstanceType":"m4.large","Name":"Core - 2"}]' --scale-down-behavior TERMINATE_AT_INSTANCE_HOUR \
--auto-terminate --region us-east-2)

#print the cluster id
echo "Cluster Running: $clusterId"

#wait for the cluster to complete
aws emr wait cluster-running --cluster-id $clusterId
echo "Process Complete Transferring Files"

#copy the output files from the mapreduce bucket after verifying existence
aws s3api wait object-exists --bucket recommenderdump --key outputsrecSys/part-r-00000
aws s3 cp s3://recommenderdump/outputsrecSys/part-r-00000 part0

aws s3api wait object-exists --bucket recommenderdump --key outputsrecSys/part-r-00001
aws s3 cp s3://recommenderdump/outputsrecSys/part-r-00001 part1

aws s3api wait object-exists --bucket recommenderdump --key outputsrecSys/part-r-00002
aws s3 cp s3://recommenderdump/outputsrecSys/part-r-00002 part2

echo "Deleting S3 Files"

#delete the bucket
aws s3 rm s3://recommenderdump/outputsrecSys --recursive

echo "Uploading New Files To DB"

#merge the files and upload the data to redis
python merge.py part0 part1 part2
python indexRecommendations.py 

echo "Backingup Mapreduce Output Files"

#store the last set of output for backup
mv part* backupOutput
cp recommendations.txt backupOutput

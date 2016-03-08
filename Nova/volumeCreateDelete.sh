#!/bin/bash 

# Simply executes a loop 
#  create a volume
#  check volume is available
#  delete the volume
# default size is 1 GB

NUMLOOPS=2
#NUMLOOPS=200
VOLUME_SIZE=1
CREATE_SLEEP=10
echo "Running for $NUMLOOPS"

function get_vdq_status {
  ssh -q $1 "sudo virsh dumpxml $2 |grep -C1 vdq"
}

function wait_for_state {
  desired_state=$1
  volume_name=$2
#  attachState=`cinder  list | grep volume_name | awk '{ print $4 }'`
  echo desired_state=$1 volume_name=$2 
  #echo desired_state=$1 volume_name=$2 attachState=$attachState
  sleep $CREATE_SLEEP

  return

  echo initial state=$attachState
  ssh -q $2 "sudo virsh dumpxml $3 |grep -C1 vdq"

  counter=0
  while [[ "$counter" -lt $numRetries && "$attachState" != "$desired_state" ]]
  do
    sleep 1
    counter=$((counter + 1))
    attachState=`cinder --insecure list | grep $volNum | awk '{ print $4 }'`
    echo "Sleeping on iteration $counter + attachState = $attachState"
    if [ $counter -gt 7 ]
    then
      ssh -q $2 "sudo virsh dumpxml $3 |grep -C1 vdq"
    fi
  done;

  if [ $counter -eq $numRetries ]
  then
    echo "ERROR Max retries reached - volume appears to be STUCK"
    ssh -q $2 "sudo virsh dumpxml $3 |grep -C1 vdq"
    sleep 2
    exit -1
  fi
  echo final state=$attachState
  ssh -q $2 "sudo virsh dumpxml $3 |grep -C1 vdq"
  sleep 1
}

x=1
while [ $x -le $NUMLOOPS ]
do
  echo "--------------------"
  echo " Starting Iteration $i"
  date

  VOLUME_NAME="testCreate$x"
  # Attach and detach to instance 1
  echo creating $VOLUME_NAME size=$VOLUME_SIZE
  cinder create --display_name $VOLUME_NAME $VOLUME_SIZE
  wait_for_state available $VOLUME_NAME
  echo deleting $VOLUME_NAME 
  cinder delete $VOLUME_NAME
  #wait_for_state deleted
  sleep 2

  echo " Completed Iteration $i"
  echo "--------------------"
  x=$(( $x + 1 ))
done;

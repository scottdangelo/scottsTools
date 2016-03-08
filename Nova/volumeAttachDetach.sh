#!/bin/bash 

# Reproducer for Bock-2620
# Assumes 2 pre-created instances
# and 1 pre-created volume
# Simply executes a loop 
# + attach the vol to instance1
# + detach the vol from instance1
# + attach the vol to instance 2
# + detach the vol from instance2

# TBD
# No retries currently built in but it waits a generous 30s for operations to complete

vmOneId=$VMONEID
vmTwoId=$VMTWOID
vmOne=$VMONE_SSH_ALIAS
vmTwo=$VMTWO_SSH_ALIAS
vmOneVirshShort=$VMONE_VIRSH_NUM
vmTwoVirshShort=$VMTWO_VIRSH_NUM

volNum=$VOLUME_ID

# Allowing 20 loops of 1s to attach / detach
numRetries=50

function get_vdq_status {
  ssh -q $1 "sudo virsh dumpxml $2 |grep -C1 vdq"
}

function wait_for_state {
  desired_state=$1
  echo desired_state=$1
  attachState=`cinder --insecure list | grep $volNum | awk '{ print $4 }'`
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

for i in {1..10000}
do
  echo "--------------------"
  echo " Starting Iteration $i"
  date

  # Attach and detach to instance 1
  nova --insecure volume-attach $vmOneId $volNum /dev/vdq
  wait_for_state in-use $vmOne $vmOneVirshShort
  nova --insecure volume-detach $vmOneId $volNum
  wait_for_state available $vmOne $vmOneVirshShort


  # Attach and detach to instance 2
  nova --insecure volume-attach $vmTwoId $volNum /dev/vdq
  wait_for_state in-use $vmTwo $vmTwoVirshShort
  nova --insecure volume-detach $vmTwoId $volNum
  wait_for_state available $vmTwo $vmTwoVirshShort


  # Adding a sleep as a tight loop is dometimes failing with /dev/vdq is busy
  sleep 10

  echo " Completed Iteration $i"
  echo "--------------------"
done;

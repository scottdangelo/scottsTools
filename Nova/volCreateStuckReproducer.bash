gfahy@gfahy-HP-Z400-Workstation:~/BockMonitor$ cat bock_2620_repro_controller.sh
#!/bin/bash -x

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

vmOneId=cfb3c8e0-1d52-4eec-a6ec-17328f3b2f52
vmTwoId=5e841ba9-4ce7-482e-bc2c-5caaa217110c
vmOneIp=15.184.74.49
vmTwoIp=15.184.74.62

volNum=a004c785-ffda-44e7-bdb8-dd97d262f827

# 30s should be plenty time for an attach / detach operation to complete
stepDelay=30


for i in {1..100}

do
  echo "--------------------"
  echo " Starting Iteration $i"
  date

  # Attach and detach to instance 1
  nova --insecure volume-attach $vmOneId $volNum /dev/vdc
  sleep $stepDelay
  nova --insecure volume-detach $vmOneId $volNum
  sleep $stepDelay


  # Attach and detach to instance 2
  nova --insecure volume-attach $vmTwoId $volNum /dev/vdc
  sleep $stepDelay
  nova --insecure volume-detach $vmTwoId $volNum
  sleep $stepDelay


  echo " Completed Iteration $i"
  echo "--------------------"
done;

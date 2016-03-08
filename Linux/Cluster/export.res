resource export {
        device /dev/drbd0;
        disk /dev/vdb1;
        meta-disk internal;
        on natty1 {
                address 192.168.122.100:7788;
        }
        on natty2 {
                address 192.168.122.101:7788;
        }
        syncer {
                rate 10M;
        }
}

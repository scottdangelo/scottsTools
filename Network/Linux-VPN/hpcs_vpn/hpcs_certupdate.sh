#!/bin/sh

SCRIPTPATH=$(dirname $(readlink -f $0))

echo "Updating VPN endpoint SSL certs..."

echo " - Updating for US East (useast.vpn.hpcloud.net)"
openssl s_client -connect useast.vpn.hpcloud.net:443 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -outform der > $SCRIPTPATH/ssl-useast.crt

echo " - Updating for US West (uswest.vpn.hpcloud.net)"
openssl s_client -connect uswest.vpn.hpcloud.net:443 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -outform der > $SCRIPTPATH/ssl-uswest.crt

echo "Done."

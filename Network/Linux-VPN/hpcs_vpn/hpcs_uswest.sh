#!/bin/sh

SCRIPTPATH=$(dirname $(readlink -f $0))

python $SCRIPTPATH/juniperncprompt.py --nc-path $SCRIPTPATH --cert $SCRIPTPATH/ssl-uswest.crt --login-path /dana-na/auth/url_1/login.cgi --realm 2FA remote.aw2.hpcloud.net

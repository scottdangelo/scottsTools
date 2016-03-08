#!/usr/bin/env python

import getpass
import gettext
import os
import paramiko
from paramiko import SSHException
import re
import sys

from bock.util import mixin_logging, bock_script_logging_options
from bock.vdm.clientiface import VDMClient

from nova import context
from nova import db
from nova import flags
from nova import utils

class SSHConnection(object):
    def __init__(self, name, user=None, password=None):
        self.name = name
        self.ssh = None
        self.stdin = None
        self.stdout = None
        self.stderr = None
        if user:
            self.user = user
        else:
            self.user = getpass.getuser()
        self.password = password

    def connect(self, verbose=False, port=22, password_prompt=getpass.getpass):
        if verbose:
            print "Connection to host '%s'" % (self.name)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if not self.password:
            try:
                self.ssh.connect(self.name, 22, self.user)
                return
            except SSHException as e:
                # We need a password
                self.password = password_prompt("Key based logon did not work, please provide password for %s@%s: "
                                                % (self.user, self.name), stream=sys.stderr)

        self.ssh.connect(self.name, 22, self.user, password=self.password)

    def exec_command(self, cmd):
        if not self.ssh:
            raise Exception("exec_command: not connected")
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return (stdin, stdout, stderr)


FLAGS = flags.FLAGS
utils.default_flagfile()
FLAGS(sys.argv)

user = os.environ["USER"]
if user == "root":
    user = os.environ["SUDO_USER"]

password = getpass.getpass("please provide password for %s@*: " % (user), stream=sys.stderr)

ctxt = context.get_admin_context()

for volid in sys.argv[1:]:
    if not re.match("^[0-9a-h-]+$", volid):
        continue

    print "Examining volume %s" % volid

    vol = db.volume_get(ctxt, volid)
    print "   - Volume %s status %s instanceID %s" % (vol.id, vol.status, vol.instance_id)

    if vol.status != "error-detaching":
        print "This tool only currently supports volumes in 'error-detaching' - skipping volume %s" % vol.id
        continue

    instance = vol.instance

    if instance is None:
        print "Instance %s no longer in DB - please raise a BOCK ticket for this volume" % (vol.instance_id)
        continue

    print "   - Instance %s status %s host %s" % (instance.id, instance.vm_state, instance.host)

    # Need to ask bock for the top level device name of this volume...
    vdm = vol.provider_location

    client = VDMClient()
    vd = client.get_volume_vd_id(vdm, vol.name)

    print "   - vdm: %s VD: %s" % (vdm, vd)

    parts = client.get_components(vol.name, vdm)

    if len(parts) != 1:
        print "Volume %s is a COW volume and not supported by this tool - please raise a BOCK ticket"
        continue

    bv = parts[0]["vol_name"]

    print "   - Checking for /dev/mapper/%s on host %s" % (bv, instance.host)

    conn = SSHConnection(instance.host, user=user, password=password)
    conn.connect()
    stdin, stdout, stderr = conn.exec_command("ls /dev/mapper")
    stdout = stdout.readlines()

    if len(stdout) < 1:
        print "An error occured processing volume %s, please raise a BOCK ticket"
        continue

    found = False
    for line in stdout:
        if bv in line:
            found = True
            break

    if found:
        print "   - Detaching volume from compute host"
        stdin, stdout, stderr = conn.exec_command("sudo bocktool --detach --volumes %s --vdm %s" % (vol.name, vdm))
        stdout = stdout.readlines()

        print "   - Checking detach worked"
        stdin, stdout, stderr = conn.exec_command("ls /dev/mapper")
        stdout = stdout.readlines()

        if len(stdout) < 1:
            print "An error occured processing volume %s (second step), please raise a BOCK ticket"
            continue

        found = False
        for line in stdout:
            if bv in line:
                found = True
                break

        if found:
            print "Could not detach volume %s from compute host, please raise a BOCK ticket" % vol.id
            continue

    print "   - Clearing status of volume %s" % vol.name

    db.volume_update(ctxt, vol.id, {'status': 'available'})

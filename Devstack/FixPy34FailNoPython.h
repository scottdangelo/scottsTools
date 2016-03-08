See this:
 netifaces.c:1:20: fatal error: Python.h: No such file or directory
     #include <Python.h>
                        ^
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

    ----------------------------------------
Command "/opt/stack/cinder/.tox/py34/bin/python3.4 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-9jy1tclj/netifaces/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-vehykqgx-record/install-record.txt --single-version-externally-managed --compile --install-headers /opt/stack/cinder/.tox/py34/include/site/python3.4/netifaces" failed with error code 1 in /tmp/pip-build-9jy1tclj/netifaces

ERROR: could not install deps [-r/opt/stack/cinder/test-requirements.txt, oslo.versionedobjects[fixtures]]; v = InvocationError('/opt/stack/cinder/.tox/py34/bin/pip install -r/opt/stack/cinder/test-requirements.txt oslo.versionedobjects[fixtures] (see /opt/stack/cinder/.tox/py34/log/py34-1.log)', 1)
_______________________________________________________________ summary _______________________________________________________________
ERROR:   py34: could not install deps [-r/opt/stack/cinder/test-requirements.txt, oslo.versionedobjects[fixtures]]; v = InvocationError('/opt/stack/cinder/.tox/py34/bin/pip install -r/opt/stack/cinder/test-requirements.txt oslo.versionedobjects[fixtures] (see /opt/stack/cinder/.tox/py34/log/py34-1.log)', 1)

Fix with this:
sudo apt-get install python3-dev

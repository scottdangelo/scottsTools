#!/usr/bin/python

AUTH_URL="http://192.168.122.93:5000/v2.0"
#OS_CACERT=
#OS_IDENTITY_API_VERSION=2.0
#OS_NO_CACHE=1
PASS="abc123"
#OS_PROJECT_NAME=demo
#OS_REGION_NAME=RegionOne
TENANT="demo"
USER="demo"
#OS_VOLUME_API_VERSION=2


# use v2.0 auth with http://example.com:5000/v2.0/
from cinderclient import client
from cinderclient import api_versions
from keystoneauth1 import loading as ks_loading
import nova.conf

CONF = nova.conf.CONF
_SESSION = None

if not _SESSION:
    _SESSION = ks_loading.load_session_from_conf_options(
        CONF, nova.conf.cinder.cinder_group.name)


url = None
endpoint_override = None

auth = context.get_auth_plugin()
service_type, service_name, interface = CONF.cinder.catalog_info.split(':')

service_parameters = {'service_type': service_type,
		  'service_name': service_name,
		  'interface': interface,
		  'region_name': CONF.cinder.os_region_name}

if CONF.cinder.endpoint_template:
    url = CONF.cinder.endpoint_template % context.to_dict()
    endpoint_override = url
else:
    url = _SESSION.get_endpoint(auth, **service_parameters)

print "Url: %s\n" % url

nt = client.Client('3.3',USER, PASS, TENANT, AUTH_URL)
#vol = nt.volumes.create(name="test-vol", size=1)
#print vol.id
version = api_versions.APIVersion("3.1")
ret_version = client.api_versions.discover_version(nt,version)
print "version: %s" % ret_version
nt.volumes.list()

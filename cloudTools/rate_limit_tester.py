#!/usr/bin/env python
#
# Usage:
#  To avoid entering at the prompt, export OS_TENANT_NAME, OS_PROJECT_ID,
#  and AUTH_TOKEN
#
#  To do HTTP GET (cinder list) with 30 threads:
#  ./rate_limit_tester.py -e aw2_2_apigee_4_2 -p 30 list-volumes
#
#  To test a specific endpoint, HTTP PUT (cinder rename ...)
#  ./rate_limit_tester.py -e aw2_2_apigee_4_2 -s cinder_api_1 rename-volumes
#
#  To remove all volumes for a tenant..This Is Dangerous! Use With Caution!
#  ./rate_limit_tester.py -e aw2_2_apigee_4_2 remove-all-volumes

import argparse
import logging
import multiprocessing
import os
import requests
import sys
import json
import time

log = logging.getLogger(__name__)

SLEEP_FOR_DELETE = 40


class RateLimitTester(object):
    """
    Tool for testing rate limits
    """
    stb_apigee_4_2 = {'ext_lb': 'region-a.geo-1.block.stb.aw1.hpcloud.net',
                      'apigee_1': '15.184.17.27:8776',
                      'apigee_2': '15.184.17.29:8776',
                      'apigee_3': None,
                      'int_lb':
                      'region-a.geo-1.block-internal.stb.aw1.hpcloud.net:8776',
                      'cinder_api_1':
                      'cr-stbaz1-api0001.systestb.hpcloud.net:8776',
                      'cinder_api_2':
                      'cr-stbaz2-api0001.systestb.hpcloud.net:8776',
                      'identity': 'cs.systest2.aw1.hpcloud.net'
                      }
    stb_apigee_4_14_04 = {'ext_lb': 'region-a.geo-1.block.stb.aw1.hpcloud.net',
                          'apigee_1': '15.184.35.217:8776',
                          'apigee_2': '15.184.35.236:8776',
                          'apigee_3': '15.184.35.226:8776',
                          'int_lb':
                          'region-a.geo-1.block-internal.stb.aw1.hpcloud.net:8776',
                          'cinder_api_1':
                          'cr-stbaz1-api0001.systestb.hpcloud.net:8776',
                          'cinder_api_2':
                          'cr-stbaz2-api0001.systestb.hpcloud.net:8776',
                          'identity': 'cs.systest2.aw1.hpcloud.net'
                          }

    ae1_2_apigee_3_8 = {'ext_lb': 'region-b.geo-1.block.hpcloudsvc.com',
                        'apigee_1': '10.22.121.103:8776',
                        'apigee_2': '10.22.121.111:8776',
                        'apigee_3': None,
                        'int_lb':
                        'region-b.geo-1.block-internal.hpcloudsvc.com:8776',
                        'cinder_api_1':
                        'cr-ae1-2az1-api0001.useast.hpcloud.net:8776',
                        'cinder_api_2':
                        'cr-ae1-2az2-api0001.useast.hpcloud.net:8776',
                        'identity': 'region-b.geo-1.identity.hpcloudsvc.com'
                        }
    ae1_2_apigee_4_2 = {'ext_lb': 'region-b.geo-1.block.hpcloudsvc.com',
                        'apigee_1': '10.22.230.37:8776',
                        'apigee_2': '10.22.233.30:8776',
                        'apigee_3': None,
                        'int_lb':
                        'region-b.geo-1.block-internal.hpcloudsvc.com:8776',
                        'cinder_api_1':
                        'cr-ae1-2az1-api0001.useast.hpcloud.net:8776',
                        'cinder_api_2':
                        'cr-ae1-2az2-api0001.useast.hpcloud.net:8776',
                        'identity': 'region-b.geo-1.identity.hpcloudsvc.com'
                        }

    aw2_2_apigee_4_2 = {'ext_lb': 'region-a.geo-1.block.hpcloudsvc.com',
                        'apigee_1': '10.8.115.180:8776',
                        'apigee_2': '10.8.115.199:8776',
                        'apigee_3': None,
                        'int_lb':
                        'region-a.geo-1.block-internal.hpcloudsvc.com:8776',
                        'cinder_api_1':
                        'cr-aw2-2az1-api0001.uswest.hpcloud.net:8776',
                        'cinder_api_2':
                        'cr-aw2-2az2-api0001.uswest.hpcloud.net:8776',
                        'identity': 'region-a.geo-1.identity.hpcloudsvc.com'
                        }

    aw2_2_apigee_3_8 = {'ext_lb': 'region-a.geo-1.block.hpcloudsvc.com',
                        'apigee_1': '15.185.16.204:8776',
                        'apigee_2': '15.185.16.232:8776',
                        'apigee_3': None,
                        'int_lb':
                        'region-a.geo-1.block-internal.hpcloudsvc.com:8776',
                        'cinder_api_1':
                        'cr-aw2-2az1-api0001.uswest.hpcloud.net:8776',
                        'cinder_api_2':
                        'cr-aw2-2az2-api0001.uswest.hpcloud.net:8776',
                        'identity': 'region-a.geo-1.identity.hpcloudsvc.com'
                        }

    def __init__(self, project_name, project_id, user_name, env,
                 use_endpoint):

        self.project_name = project_name
        self.project_id = project_id
        self.user_name = user_name
        self.token = None
        self.env = env
        self.use_endpoint = use_endpoint
        self.hosts = []
        self.delete_list = []

        self.headers = None

    def _get_headers(self):
        """ Fill in header info"""

        self.headers = {'X-Auth-Project-Id': self.project_name,
                        'User-Agent': 'python-cinderclient',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-Auth-Token': self.token}

    def _configure_logging(self, args):
        """This does a similar job to logging.basicConfig(),
        setting default log level of DEBUG for root logger
        and configuring handlers with appropriate formatters."""
        ch = logging.StreamHandler(stream=sys.stdout)

        log.setLevel(logging.DEBUG)
        # if -vvv provide DEBUG output for all libraries
        if args.verbose >= 3:
            logging.getLogger('').setLevel(logging.DEBUG)
        # if -vv provide DEBUG output for rate_limit_testser
        # but INFO for libraries
        elif args.verbose >= 2:
            logging.getLogger('').setLevel(logging.INFO)
            ch.setLevel(logging.DEBUG)
        elif args.verbose >= 1:
            ch.setLevel(logging.INFO)
        else:
            ch.setLevel(logging.WARNING)
        ch_format = logging.Formatter('%(message)s')
        ch.setFormatter(ch_format)
        logging.getLogger('').addHandler(ch)

    def _setup_env(self, ext_lb, apigee_1, apigee_2, apigee_3, int_lb,
                   cinder_api_1, cinder_api_2, identity):

        self.external_lb = ext_lb
        self.apigee_1 = apigee_1
        self.apigee_2 = apigee_2
        self.apigee_3 = apigee_3
        self.internal_lb = int_lb
        self.cinder_api_1 = cinder_api_1
        self.cinder_api_2 = cinder_api_2

        self.identity = identity

        if self.use_endpoint == 'all':
            self.hosts.append(self.cinder_api_1)
            self.hosts.append(self.cinder_api_2)
            self.hosts.append(self.internal_lb)
            self.hosts.append(self.apigee_1)
            self.hosts.append(self.apigee_2)
            if self.apigee_3:
                self.hosts.append(self.apigee_3)
            self.hosts.append(self.external_lb)
        elif self.use_endpoint is None:
            self.hosts.append(self.external_lb)
        else:
            self.hosts.append(getattr(self, self.env)[self.use_endpoint])

    def _set_token_from_password(self, password):
        """
        Get AUTH_TOKEN using API
        """
        url = ('https://%s:35357/v2.0/tokens' % self.identity)
        payload = {u'auth': {u'passwordCredentials':
                            {u'username': self.user_name,
                             u'password': password},
                             u'tenantName': self.project_name}}

        token_headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json'}

        req = requests.post(url, headers=token_headers,
                            data=json.dumps(payload), verify=False)
        log.debug(('URL:%s\nHeaders:\n%s\nPayload:\n%s\nResponse:\n%s\n\n')
                  % (url, token_headers, payload, req.text))

        return_json = json.loads(req.text)
        token = return_json["access"]["token"]["id"]
        log.debug('Token: %s\n' % token)

        self.token = token

    def _perform_request(self, verb, endpoint_host, payload=None,
                         current_vol=None):
        """
        perform the given request
        """
        host = endpoint_host

        # HTTP GET for list
        if verb is 'get':
            url = 'https://%s/v1/%s/volumes' % (host, self.project_id)

            r = requests.get(url, verify=False, headers=self.headers)

        # HTTP DELETE for delete
        elif verb is 'delete':
            url = 'https://%s/v1/%s/volumes/%s' % (host, self.project_id,
                                                   current_vol)
            r = requests.delete(url, verify=False, headers=self.headers)

        # HTTP PUT for rename
        elif verb is 'put':
            url = 'https://%s/v1/%s/volumes/%s' % (host, self.project_id,
                                                   current_vol)
            r = requests.put(url, headers=self.headers,
                             data=json.dumps(payload), verify=False)

        # HTTP POST for create
        elif verb is 'post':
            url = 'https://%s/v1/%s/volumes' % (host, self.project_id)

            r = requests.post(url, headers=self.headers,
                              data=json.dumps(payload), verify=False)

        log.warning('%s response code: %d', host, r.status_code)
        log.info(('URL:\n%s\nHeaders:\n%s\nPayload:\n%s\nResponse:\n%s\n') %
                 (url, self.headers, payload, r.text))
        return r.text, r.status_code

    def _list_volumes(self, host):
        """
        list the volumes for this project_name and project_id.
        Use https://<host>/v1/<project_id>/volumes with a GET
        """
        self._perform_request('get', host)

    def _create_volumes(self, host):
        """
        create a volume
        Use https://<host>/v1/<project_id>/volume with a POST
        """
        payload = {u'volume': {u'status': u'creating', u'user_id': None,
                   u'imageRef': None, u'availability_zone': u'az1',
                   u'attach_status': u'detached',
                   u'display_description': None, u'metadata': {},
                   u'source_volid': None, u'snapshot_id': None,
                   u'display_name': None, u'project_id': None,
                   u'volume_type': None, u'size': 1}}

        return self._perform_request('post', host, payload)

    def _create_volumes_for_delete(self, host):
        """
        create volume(s) and keep in a list for later delete
        """
        json_data = self._create_volumes(host)
        data = json.loads(json_data)
        volume = data["volume"]["id"]
        self.delete_list.append(volume)

        log.debug(("create_for_delete: json_data= %s\nvolume= %s\n") %
                 (json_data, volume))

    def _wait_for_creates(self, host):
        """
        Wait for volumes to be created,i.e. not in 'creating'
        """
        while True:
            ret, status = self._perform_request('get', host)
            if ret is not None and 'creating' in ret:
                time.sleep(2)
                continue
            break

    def _get_volumes(self, host):
        """
        get a list of volumes using HTTP GET
        """

        vols = []
        volumes, status = self._perform_request('get', host)
        volumes = str(volumes).strip()

        vol_list = volumes.split(",")
        for item in vol_list:
            if 'id' in item and not 'null' in item:
                foo = item.split(':')
                vols.append(foo[1])

        return vols

    def _delete_volumes(self, host, current_vol, delete_all=False):
        """
        delete the current volume
        If rate-limited and deleting all volumes,
        sleep SLEEP_FOR_DELETE seconds
        """

        current_vol = current_vol.replace('"', '').strip()
        ret, status = self._perform_request('delete', host,
                                            current_vol=current_vol)
        if delete_all:
            if status == '413':
                log.debug("sleeping for %s" % SLEEP_FOR_DELETE)
                time.sleep(SLEEP_FOR_DELETE)

    def _rename_volumes(self, host, current_vol):
        """
        rename volume name to "foo"
        """

        payload = {u'volume': {u'display_name': u'foo'}}
        current_vol = current_vol.replace('"', '').strip()
        self._perform_request('put', host, payload=payload,
                              current_vol=current_vol)


def main():
    parser = argparse.ArgumentParser(
        description='A tool for showing info about a volume')

    parser.add_argument("-e", "--environment",
                        required=True,
                        help="Environment to run in: stb_apigee_4_2, "
                        "stb_apigee_4_14_04, ae1_2_apigee_3_8, "
                        "ae1_2_apigee_4_2, aw2_2_apigee_3_8, "
                        "aw2_2_apigee_4_2")
    parser.add_argument('-a', '--all_endpoints',
                        help='run command on all enpoints',
                        action='store_true')
    parser.add_argument('-s', '--specific_endpoint',
                        help="run command on specific enpoint. One of: "
                        "ext_lb, apigee_1, apigee_2, apigee_3, int_lb, "
                        "cinder_api_1, cinder_api_2")
    parser.add_argument('-u', '--user_name',
                        default=os.environ.get('OS_USERNAME'),
                        help='hpcloud user name')
    parser.add_argument('-p', '--processes',
                        type=int,
                        default=1)
    parser.add_argument('-t', '--token',
                        default=os.environ.get('AUTH_TOKEN'),
                        help='hp auth token')
    parser.add_argument('-n', '--project_name',
                        default=os.environ.get('OS_TENANT_NAME'),
                        help='hpcloud project name')
    parser.add_argument('-i', '--project_id',
                        default=os.environ.get('OS_PROJECT_ID'),
                        help='hpcloud project ID')
    parser.add_argument('-w', '--password',
                        default=os.environ.get('OS_PASSWORD'),
                        help='hpcloud SSO password')
    parser.add_argument('-v', '--verbose',
                        help='provide verbose console output '
                        '(repeating increases detail)',
                        action='count')

    subparsers = parser.add_subparsers(
        dest="command",
        title="Available commands")

    subparsers.add_parser('list-volumes', help='GET for '
                          'https://<host>/v1/<tenant>/volumes')
    subparsers.add_parser('create-volumes', help='POST for '
                          'http://<host>/v1/<tenant>/volume')
    subparsers.add_parser('delete-volumes', help='DELETE for '
                          'http://<host>/v1/<tenant>/volumes/<volume>')
    subparsers.add_parser('rename-volumes', help='PUT for '
                          'http://<host>/v1/<tenant>/volumes/<volume>')
    subparsers.add_parser('remove-all-volumes', help='list all volumes '
                          'and then remove them all. BE CAREFUL! ALL VOLUMES '
                          'FOR THIS TENANT WILL BE REMOVED!')

    args = parser.parse_args()

    if not args.project_name:
        project_name = raw_input("Enter your project name: ")
    else:
        project_name = args.project_name

    if not args.project_id:
        project_id = raw_input("Enter your project ID: ")
    else:
        project_id = args.project_id

    if not args.user_name:
        user_name = raw_input("Enter your user name: ")
    else:
        user_name = args.user_name

    if args.specific_endpoint:
        use_endpoint = args.specific_endpoint
    elif args.all_endpoints:
        use_endpoint = 'all'
    else:
        use_endpoint = None

    env = args.environment
    tester = RateLimitTester(project_name, project_id, user_name,
                             env, use_endpoint)
    tester._configure_logging(args)

    if hasattr(tester, env):
        tester._setup_env(**getattr(tester, env))
    else:
        print "Unrecognised env: %s" % env
        exit(1)

    if args.password:
        password = args.password
        tester._set_token_from_password(password)
    elif not args.token:
        tester.token = raw_input("Enter your Auth Token: ")
    else:
        tester.token = args.token

    tester._get_headers()

    for host in tester.hosts:
        if 'list-volumes' in args.command:
            for i in xrange(1, args.processes + 1):
                p = multiprocessing.Process(target=tester._list_volumes,
                                            args=(host,))
                p.start()
        if 'create-volumes' in args.command:
            for i in xrange(1, args.processes + 1):
                p = multiprocessing.Process(target=tester._create_volumes,
                                            args=(host,))
                p.start()
        if 'delete-volumes' in args.command:
            # create volumes to delete
            for i in xrange(1, args.processes + 1):
                tester._create_volumes_for_delete(host)
            tester._wait_for_creates(host)
            # delete the volumes
            if len(tester.delete_list) > 0:
                for i in xrange(0, len(tester.delete_list)):
                    p = multiprocessing.Process(target=tester._delete_volumes,
                                                args=(host,
                                                      tester.delete_list[i]))
                    p.start()

        if 'rename-volume' in args.command:
            current_vols = tester._get_volumes(host)
            if len(current_vols) > 0:
                for i in xrange(0, len(current_vols)):
                    p = multiprocessing.Process(target=tester._rename_volumes,
                                                args=(host, current_vols[i]))
                    p.start()

        if 'remove-all-volumes' in args.command:
            answer = raw_input("Do you really want to delete all Volumes?"
                               " (Enter 'Yes' to destroy everything)")
            if answer != 'Yes':
                exit(0)
            # clear all volumes
            current_vols = tester._get_volumes(host)
            if len(current_vols) > 0:
                for i in xrange(0, len(current_vols)):
                    tester._delete_volumes(host, current_vols[i],
                                           delete_all=True)

if __name__ == '__main__':
    main()

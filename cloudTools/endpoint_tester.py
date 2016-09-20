#!/usr/bin/env python
#
# (C) Copyright 2013 Hewlett-Packard Development Company, L.P.
"""
 Usage:
  To avoid entering at the prompt, export OS_TENANT_NAME, OS_PROJECT_ID,
  and AUTH_TOKEN
  To avoid export-ing AUTH_TOKEN enter "-u <user_name> -p <passwd>"
  OR export OS_USERNAME and OS_PASSWORD

  To test endpoints:
    ./endpoint_tester.py  -e aw2_2_apigee_3_8
  For testing endpoints with one line output for Icinga:
    ./endpoint_tester.py  -m -e aw2_2_apigee_3_8

"""

import argparse
import logging
import os
import requests
import sys
import json

LOG = logging.getLogger(__name__)


class EndpointTester(object):
    """
    Tool for testing endpoints in a Cinder-based environment.
    The tool will start at the most internal endpoint and
    check each component of the environment:
    cinder_api -> internal_load_balancer -> apigee ->
    external_load_balancer
    """
    stb_apigee_4_14_07 = {'ext_lb': 'region-a.geo-1.block.stb.aw1.hpcloud.net',
                          'apigee_1': '15.184.35.217:8776',
                          'apigee_2': '15.184.35.236:8776',
                          'apigee_3': '15.184.35.226:8776',
                          'int_lb':
                          'region-a.geo-1.block-internal.stb.aw1.hpcloud.net:8776',
                          'cinder_api_1':
                          'cr-stbaz1-api0001.systestb.hpcloud.net:8776',
                          'cinder_api_2':
                          'cr-stbaz2-api0001.systestb.hpcloud.net:8776',
                          'cinder_api_3':
                          'cr-stbaz1-manage0001.systestb.hpcloud.net:8776',
                          'cinder_api_4':
                          'cr-stbaz1-volmanager0002.systestb.hpcloud.net:8776',
                          'cinder_api_5':
                          'cr-stbaz1-volmanager0003.systestb.hpcloud.net:8776',
                          'cinder_api_6':
                          'cr-stbaz1-volmanager0004.systestb.hpcloud.net:8776',
                          'cinder_api_7':
                          'cr-stbaz2-manage0001.systestb.hpcloud.net:8776',
                          'cinder_api_8':
                          'cr-stbaz2-volmanager0002.systestb.hpcloud.net:8776',
                          'cinder_api_9':
                          'cr-stbaz2-volmanager0003.systestb.hpcloud.net:8776',
                          'cinder_api_10':
                          'cr-stbaz2-volmanager0004.systestb.hpcloud.net:8776',
                          'admin_lb':
                          'region-a.geo-1.block-internal-admin.stb.aw1.hpcloud.net:8776',
                          'cinder_admin_api_1':
                          'cr-stbaz1-volmanager0001.systestb.hpcloud.net:8776',
                          'cinder_admin_api_2':
                          'cr-stbaz2-volmanager0001.systestb.hpcloud.net:8776',
                          'cinder_admin_api_3': None,
                          'identity': 'cs.systestb.hpcloud.net'
                          }

    ae1_2_apigee_4_14_07 = {'ext_lb': 'region-b.geo-1.block.hpcloudsvc.com',
                            'apigee_1': '10.22.122.11:8776',
                            'apigee_2': '10.22.122.12:8776',
                            'apigee_3': '10.22.122.13:8776',
                            'int_lb':
                            'region-b.geo-1.block-internal.hpcloudsvc.com:8776',
                            'cinder_api_1':
                            'cr-ae1-2az1-api0001.useast.hpcloud.net:8776',
                            'cinder_api_2':
                            'cr-ae1-2az2-api0001.useast.hpcloud.net:8776',
                            'cinder_api_3':
                            'cr-ae1-2az1-manage0001.useast.hpcloud.net:8776',
                            'cinder_api_4':
                            'cr-ae1-2az1-volmanager0002.useast.hpcloud.net:8776',
                            'cinder_api_5':
                            'cr-ae1-2az1-volmanager0003.useast.hpcloud.net:8776',
                            'cinder_api_6':
                            'cr-ae1-2az2-volmanager0002.useast.hpcloud.net:8776',
                            'cinder_api_7':
                            'cr-ae1-2az2-volmanager0003.useast.hpcloud.net:8776',
                            'cinder_api_8':
                            'cr-ae1-2az3-dbquorum0001.useast.hpcloud.net:8776',
                            'cinder_api_9':
                            'cr-ae1-2az3-mqquorum0001.useast.hpcloud.net:8776',
                            'cinder_api_10':
                            'cr-ae1-2az3-volmanager0008.useast.hpcloud.net:8776',
                            'admin_lb':
                            'region-b.geo-1.block-internal-admin.hpcloudsvc.com:8776',
                            'cinder_admin_api_1':
                            'cr-ae1-2az1-volmanager0001.useast.hpcloud.net:8776',
                            'cinder_admin_api_2':
                            'cr-ae1-2az2-volmanager0001.useast.hpcloud.net:8776',
                            'cinder_admin_api_3':
                            'cr-ae1-2az3-volmanager0001.useast.hpcloud.net:8776',
                            'identity': 'region-b.geo-1.identity.hpcloudsvc.com'
                            }

    aw2_2_apigee_4_14_07 = {'ext_lb': 'region-a.geo-1.block.hpcloudsvc.com',
                            'apigee_1': '10.9.239.108:8776',
                            'apigee_2': '10.9.239.109:8776',
                            'apigee_3': '10.9.239.110:8776',
                            'int_lb':
                            'region-a.geo-1.block-internal.hpcloudsvc.com:8776',
                            'cinder_api_1':
                            'cr-aw2-2az1-api0001.uswest.hpcloud.net:8776',
                            'cinder_api_2':
                            'cr-aw2-2az2-api0001.uswest.hpcloud.net:8776',
                            'cinder_api_3':
                            'cr-aw2-2az1-manage0001.uswest.hpcloud.net:8776',
                            'cinder_api_4':
                            'cr-aw2-2az1-volmanager0002.uswest.hpcloud.net:8776',
                            'cinder_api_5':
                            'cr-aw2-2az1-volmanager0003.uswest.hpcloud.net:8776',
                            'cinder_api_6':
                            'cr-aw2-2az2-manage0001.uswest.hpcloud.net:8776',
                            'cinder_api_7':
                            'cr-aw2-2az2-volmanager0002.uswest.hpcloud.net:8776',
                            'cinder_api_8':
                            'cr-aw2-2az2-volmanager0003.uswest.hpcloud.net:8776',
                            'cinder_api_9':
                            'cr-aw2-2az3-dbquorum0001.uswest.hpcloud.net:8776',
                            'cinder_api_10':
                            'cr-aw2-2az3-mqquorum0001.uswest.hpcloud.net:8776',
                            'admin_lb':
                            'region-a.geo-1.block-internal-admin.hpcloudsvc.com:8776',
                            'cinder_admin_api_1':
                            'cr-aw2-2az1-volmanager0001.uswest.hpcloud.net:8776',
                            'cinder_admin_api_2':
                            'cr-aw2-2az2-volmanager0001.uswest.hpcloud.net:8776',
                            'cinder_admin_api_3':
                            'cr-aw2-2az3-volmanager0001.uswest.hpcloud.net:8776',
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
                        'cinder_api_3':
                        'cr-aw2-2az1-manage0001.uswest.hpcloud.net:8776',
                        'cinder_api_4':
                        'cr-aw2-2az1-volmanager0002.uswest.hpcloud.net:8776',
                        'cinder_api_5':
                        'cr-aw2-2az1-volmanager0003.uswest.hpcloud.net:8776',
                        'cinder_api_6':
                        'cr-aw2-2az2-manage0001.uswest.hpcloud.net:8776',
                        'cinder_api_7':
                        'cr-aw2-2az2-volmanager0002.uswest.hpcloud.net:8776',
                        'cinder_api_8':
                        'cr-aw2-2az2-volmanager0003.uswest.hpcloud.net:8776',
                        'cinder_api_9':
                        'cr-aw2-2az3-dbquorum0001.uswest.hpcloud.net:8776',
                        'cinder_api_10':
                        'cr-aw2-2az3-mqquorum0001.uswest.hpcloud.net:8776',
                        'admin_lb':
                        'region-a.geo-1.block-internal.hpcloudsvc.com:8776',
                        'cinder_admin_api_1':
                        'cr-aw2-2az1-volmanager0001.uswest.hpcloud.net:8776',
                        'cinder_admin_api_2':
                        'cr-aw2-2az2-volmanager0001.uswest.hpcloud.net:8776',
                        'cinder_admin_api_3':
                        'cr-aw2-2az3-volmanager0001.uswest.hpcloud.net:8776',
                        'identity': 'region-a.geo-1.identity.hpcloudsvc.com'
                        }

    def __init__(self, project_name, project_id, user_name, env):

        self.project_name = project_name
        self.project_id = project_id
        self.user_name = user_name

        self.token = None
        self.headers = None
        self.env = env
        self.cinder_api_1 = None
        self.cinder_api_2 = None
        self.cinder_api_3 = None
        self.cinder_api_4 = None
        self.cinder_api_5 = None
        self.cinder_api_6 = None
        self.cinder_api_7 = None
        self.cinder_api_8 = None
        self.cinder_api_9 = None
        self.cinder_api_10 = None
        self.cinder_admin_api_1 = None
        self.cinder_admin_api_2 = None
        self.cinder_admin_api_3 = None
        self.admin_lb = None
        self.internal_lb = None
        self.apigee_1 = None
        self.apigee_2 = None
        self.external_lb = None
        self.identity = None
        self.endpoints = getattr(self, self.env)
        self.failed_names = []
        self.failed_nodes = []
        self.hosts = []

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

        logger = logging.getLogger('')
        LOG.setLevel(logging.DEBUG)
        # for Icinga monitoring, just print one-line summary
        if args.monitor_icinga:
            ch.setLevel(logging.ERROR)
        # if -vvv provide DEBUG output for all libraries
        elif args.verbose >= 3:
            logger.setLevel(logging.DEBUG)
            #logging.getLogger('').setLevel(logging.DEBUG)
        # if -vv provide DEBUG output for rate_limit_tester
        # but INFO for libraries
        elif args.verbose >= 2:
            logger.setLevel(logging.INFO)
            ch.setLevel(logging.DEBUG)
        elif args.verbose >= 1:
            ch.setLevel(logging.INFO)
        else:
            ch.setLevel(logging.WARNING)
        ch_format = logging.Formatter('%(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    def _setup_env(self, ext_lb, apigee_1, apigee_2, apigee_3, int_lb,
                   cinder_api_1, cinder_api_2, cinder_api_3, cinder_api_4,
                   cinder_api_5, cinder_api_6, cinder_api_7, cinder_api_8,
                   cinder_api_9, cinder_api_10, admin_lb, cinder_admin_api_1,
                   cinder_admin_api_2, cinder_admin_api_3, identity):
        """Setup endpoints for specific environment."""

        self.cinder_admin_api_1 = cinder_admin_api_1
        if self.cinder_admin_api_1:
            self.hosts.append(self.cinder_admin_api_1)
        self.cinder_admin_api_2 = cinder_admin_api_2
        if self.cinder_admin_api_2:
            self.hosts.append(self.cinder_admin_api_2)
        self.cinder_admin_api_3 = cinder_admin_api_3
        if self.cinder_admin_api_3:
            self.hosts.append(self.cinder_admin_api_3)
        self.admin_lb = admin_lb
        if self.admin_lb:
            self.hosts.append(self.admin_lb)
        self.cinder_api_1 = cinder_api_1
        self.hosts.append(self.cinder_api_1)
        self.cinder_api_2 = cinder_api_2
        self.hosts.append(self.cinder_api_2)
        self.cinder_api_3 = cinder_api_3
        if self.cinder_api_3:
            self.hosts.append(self.cinder_api_3)
        self.cinder_api_4 = cinder_api_4
        if self.cinder_api_4:
            self.hosts.append(self.cinder_api_4)
        self.cinder_api_5 = cinder_api_5
        if self.cinder_api_5:
            self.hosts.append(self.cinder_api_5)
        self.cinder_api_6 = cinder_api_6
        if self.cinder_api_6:
            self.hosts.append(self.cinder_api_6)
        self.cinder_api_7 = cinder_api_7
        if self.cinder_api_7:
            self.hosts.append(self.cinder_api_7)
        self.cinder_api_8 = cinder_api_8
        if self.cinder_api_8:
            self.hosts.append(self.cinder_api_8)
        self.cinder_api_9 = cinder_api_9
        if self.cinder_api_9:
            self.hosts.append(self.cinder_api_9)
        self.cinder_api_10 = cinder_api_10
        if self.cinder_api_10:
            self.hosts.append(self.cinder_api_10)
        self.internal_lb = int_lb
        self.hosts.append(self.internal_lb)
        self.apigee_1 = apigee_1
        self.hosts.append(self.apigee_1)
        self.apigee_2 = apigee_2
        self.hosts.append(self.apigee_2)
        self.apigee_3 = apigee_3
        if self.apigee_3:
            self.hosts.append(self.apigee_3)
        self.external_lb = ext_lb
        self.hosts.append(self.external_lb)
        self.identity = identity

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
        LOG.debug(('URL:%s\nHeaders:\n%s\nPayload:\n%s\nResponse:\n%s\n\n')
                  % (url, token_headers, payload, req.text))
        if 'unauthorized' in req.text:
            LOG.error('Invalid credentials: %s\n' % req.text)
            exit(1)

        return_json = json.loads(req.text)
        token = return_json["access"]["token"]["id"]
        LOG.debug('Token: %s\n' % token)
        self.token = token

        if self.project_id is None:
            project_id = return_json["access"]["token"]["tenant"]["id"]
            LOG.debug('Project id: %s\n' % project_id)
            self.project_id = project_id

    def _update_failed_lists(self, host):
        """
        determine point of failure
        """
        for key, value in self.endpoints.items():
            if value and host in value:
                self.failed_names.append(key)
                self.failed_nodes.append(value)
                return key

    def _test_endpoints(self):
        """
        list the volumes for this project_name and project_id.
        Use https://<host>/v1/<project_id>/volumes with a GET
        and perform with all enpoints
        """
        self._get_headers()

        for host in self.hosts:
            url = 'https://%s/v1/%s/volumes' % (host, self.project_id)
            req = requests.get(url, verify=False, headers=self.headers)
            if req.status_code is not 200:
                failed = self._update_failed_lists(host)
                LOG.warning('Got a problem with %s' % failed)
            LOG.warning('%s response code: %d', host, req.status_code)
            LOG.debug(('URL: %s\nHeaders:\n%s\nResponse:\n%s\n\n') %
                     (url, self.headers, req.text))

    def _print_report(self):
        """
        print summary of problems
        """
        report_string = ""
        if not self.failed_names:
            report_string += "All endpoints are OK"
        else:
            report_string += (("Problem(s) with %s on %s\n\n") %
                             ((', '.join(self.failed_names)),
                              (', '.join(self.failed_nodes))))
            if any("cinder_api" in s for s in self.failed_names):
                report_string += ("Issues with Cinder API. "
                                  "Contact the Bock team\n")
            elif any("int_lb" in s for s in self.failed_names):
                report_string += ("Cinder API is OK, but Internal Load "
                                  "Balancer is not. Contact the NET "
                                  "Engineering team\n")
            elif any("apigee" in s for s in self.failed_names):
                report_string += ("Cinder API is OK, but Apigee is not. "
                                  "Contact the SYS Engineering team\n")
            else:  # ext_lb in self.failed_names
                report_string += ("Cinder API and Apigee are OK, but External"
                                  " Load Balancer is not. Contact the NET "
                                  "Engineering team\n")
        print report_string


def main():
    """main"""

    parser = argparse.ArgumentParser(
        description='A tool for testing endpoints, from innermost to '
                    'outermost: Cinder-api -> internal Load Balancer -> '
                    'Apigee -> external Load Balancer')

    parser.add_argument("-e", "--environment",
                        required=True,
                        help="Environment to run in: stb_apigee_4_14_07, "
                        "ae1_2_apigee_4_14_07, aw2_2_apigee_3_8, "
                        "aw2_2_apigee_4_14_07")
    parser.add_argument('-t', '--token',
                        default=os.environ.get('AUTH_TOKEN'),
                        help='hp auth token')
    parser.add_argument('-n', '--project_name',
                        default=os.environ.get('OS_TENANT_NAME'),
                        help='hpcloud project name')
    parser.add_argument('-i', '--project_id',
                        default=os.environ.get('OS_PROJECT_ID'),
                        help='hpcloud project ID')
    parser.add_argument('-u', '--user_name',
                        default=os.environ.get('OS_USERNAME'),
                        help='hpcloud user name')
    parser.add_argument('-p', '--password',
                        default=os.environ.get('OS_PASSWORD'),
                        help='hpcloud SSO password')
    parser.add_argument('-m', '--monitor_icinga',
                        help='use for Icinga summary line only',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='provide verbose console output '
                        '(repeating increases detail)',
                        action='count')

    args = parser.parse_args()

    if not args.project_name:
        project_name = raw_input("Enter your project name: ")
    else:
        project_name = args.project_name

    if not args.project_id:
        project_id = None
    else:
        project_id = args.project_id

    if not args.user_name:
        user_name = raw_input("Enter your user name: ")
    else:
        user_name = args.user_name

    env = args.environment

    tester = EndpointTester(project_name, project_id, user_name,
                            env)
    tester._configure_logging(args)

    if hasattr(tester, env):
        tester._setup_env(**getattr(tester, env))
    else:
        LOG.error("Unrecognised env: %s" % env)
        exit(1)

    if args.password:
        password = args.password
        tester._set_token_from_password(password)
    elif not args.token:
        tester.token = raw_input("Enter your Auth Token: ")
    else:
        tester.token = args.token

    tester._test_endpoints()
    tester._print_report()

if __name__ == '__main__':
    main()

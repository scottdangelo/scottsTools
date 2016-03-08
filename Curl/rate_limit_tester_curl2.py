#!/usr/bin/env python
#
import argparse
import logging
import multiprocessing
import os
import requests
import sys
import time

log = logging.getLogger(__name__)

#PROJECT_NAME='CinderRateLimitTest'
#PROJECT_ID='10916888999775'
STB_HOSTS = [ '15.184.17.27:8776', '15.184.17.29:8776', 'region-a.geo-1.block.stb.aw1.hpcloud.net', 'region-a.geo-1.block-internal.stb.aw1.hpcloud.net:8776' ]


class RateLimitTester(object):
    """
    Tool for testing rate limits
    """

    def __init__(self, project_name, project_ID, token, hosts):

        self.project_name = project_name
        self.project_ID = project_ID
        self.token = token
        self.hosts = hosts

    def list_volumes(self, token, ):

        headers = {'X-Auth-Project-Id': self.project_name,
                   'User-Agent': 'python-cinderclient',
                   'Accept': 'application/json',
                   'X-Auth-Token': self.token }
#    hosts = [ '15.184.17.27:8776', '15.184.17.29:8776', 'region-a.geo-1.block.stb.aw1.hpcloud.net', 'region-a.geo-1.block-internal.stb.aw1.hpcloud.net:8776' ]
        #hosts = ['region-a.geo-1.block.stb.aw1.hpcloud.net']
        #hosts = [ '15.184.17.27:8776' ]
        for host in self.hosts:
            url = 'https://%s/v1/%s/volumes' % (host, self.project_ID)
            r = requests.get(url, verify=False, headers=headers)
            log.debug('%s response code: %d', host, r.status_code)
        #    log.debug('response text: %s', r.text)

def main():
        parser = argparse.ArgumentParser(
            description='A tool for showing info about a volume')
        parser.add_argument('-p', '--processes',
                            type=int,
                            default=1)
        parser.add_argument('-t', '--token',
                            default=os.environ.get('AUTH_TOKEN'),
                            help='hp auth token')
        parser.add_argument('-n', '--project_name',
                            default=os.environ.get('PROJECT_NAME'),
                            help='hpcloud project name')
        parser.add_argument('-i', '--project_ID',
                            default=os.environ.get('PROJECT_ID'),
                            help='hpcloud project ID')
        args = parser.parse_args()

        if not args.token:
            token = raw_input("Enter your Auth Token: ")
        else:
            token = args.token

        if not args.project_name:
            project_name = raw_input("Enter your project name: ")
        else:
            project_name = args.project_name

        if not args.project_ID:
            project_ID = raw_input("Enter your project ID: ")
        else:
            project_ID = args.project_ID

        log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(stream=sys.stdout)
        log_format = '%(process)d %(asctime)s: %(levelname)s - %(funcName)s - %(message)s'
        ch_format = logging.Formatter(log_format)
        ch.setFormatter(ch_format)
        log.addHandler(ch)

        tester = RateLimitTester(project_name, project_ID, token, STB_HOSTS)
        tester.list_volumes(token)

        #for i in xrange(1,args.processes + 1):
        #    p = multiprocessing.Process(target=list_volumes, args=(token,))
        #    p.start()

if __name__ == '__main__':
    main()

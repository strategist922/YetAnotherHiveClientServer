#!/usr/bin/env python

import sys
import argparse
import zmq
import json

def key_value(s):
        kvs = s.split("=")
        key = kvs[0].strip()
        val = kvs[1].strip()
        return (key, val)

parser = argparse.ArgumentParser(description='HiveClient tool as a client of hiveserver', add_help=False)
parser.add_argument('-h', metavar='<hostname>', type=str, required=False, help='Connecting to Hive Server on remote host', dest='host')
parser.add_argument('-p', metavar='<port>', type=int, required=False, help='Connecting to Hive Server on port number', dest='port')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', metavar='<quoted-query-string>', type=str, help='SQL from command line', dest='query')
group.add_argument('-f', metavar='<filename>', type=str, help='SQL from files', dest='script')
parser.add_argument('-d', '--define', metavar='<key=value>', type=key_value, action='append', help='Variable substitution to apply to hive commands. e.g. -d A=B or --define A=B', dest='define')
parser.add_argument('--hiveconf', metavar='<property=value>', type=key_value, action='append', help='Use value for given property', dest='hiveconf')
parser.add_argument('--hivevar', metavar='<key=value>', type=key_value, action='append', help='Variable substitution to apply to hive commands. e.g. --hivevar A=B', dest='hivevar')

args = parser.parse_args()

# -h option
host = args.host

# -p option
port = args.port

command = []
skip = False
for i in range(1, len(sys.argv)):
        tmp = sys.argv[i]
        if skip == True:
                skip = False
                continue
        if tmp == '-h' or tmp == '-p':
                skip = True
                continue
        command.append(tmp)

msg = json.dumps(command)

context = zmq.Context()
sock = context.socket(zmq.REQ)
addr = "tcp://" + host + ":" + str(port)
sock.connect(addr)

sock.send(msg)
rsp_str = sock.recv()

rsp = json.loads(rsp_str)

print "retcode:", rsp["retcode"]
print "stdout:" , rsp["stdout"]
print "stderr:", rsp["stderr"]

sock.close()
context.term()


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

def init_argument_parser():
	parser = argparse.ArgumentParser(description='HiveClient tool as a client of hiveserver', add_help=False)
	parser.add_argument('-h', metavar='<hostname>', type=str, required=False, help='Connecting to Hive Server on remote host', dest='host')
	parser.add_argument('-p', metavar='<port>', type=int, required=False, help='Connecting to Hive Server on port number', dest='port')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', metavar='<quoted-query-string>', type=str, help='SQL from command line', dest='query')
	group.add_argument('-f', metavar='<filename>', type=argparse.FileType('r'), help='SQL from files', dest='script')
	parser.add_argument('-d', '--define', metavar='<key=value>', type=key_value, action='append', help='Variable substitution to apply to hive commands. e.g. -d A=B or --define A=B', dest='define')
	parser.add_argument('--hiveconf', metavar='<property=value>', type=key_value, action='append', help='Use value for given property', dest='hiveconf')
	parser.add_argument('--hivevar', metavar='<key=value>', type=key_value, action='append', help='Variable substitution to apply to hive commands. e.g. --hivevar A=B', dest='hivevar')
	parser.add_argument('-r', metavar='0 or 1', type=int, default=0, help='Decides if the result contains stdout and stderr of hive server', dest='result')
	args = parser.parse_args()
	return args

# initialize argument parser
args = init_argument_parser()

# -h option
host = args.host

# -p option
port = args.port

# -f option
lines = args.script.readlines() if not args.script == None else None

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

result_flag = False if args.result == 0 else True
req = {"command": command, "script": lines, "result": result_flag}
req_str = json.dumps(req)

context = zmq.Context()
sock = context.socket(zmq.REQ)
addr = "tcp://" + host + ":" + str(port)
sock.connect(addr)

sock.send(req_str)
rsp_str = sock.recv()

rsp = json.loads(rsp_str)

print "retcode:", rsp["retcode"]
print "stdout:" , rsp["stdout"]
print "stderr:", rsp["stderr"]

sock.close()
context.term()

exit(rsp["retcode"])


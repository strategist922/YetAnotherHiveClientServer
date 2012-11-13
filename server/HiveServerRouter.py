#!/usr/bin/env python

import os
import json
import tempfile
import sys
import time
import logging
import ConfigParser
import subprocess
import threading
import zmq

class HiveServerRouterConfig:
        def __init__(self, path):
                self.config = ConfigParser.RawConfigParser()
                self.config.read(path)

        def dump(self):
                for section in self.config.sections():
                        for option in self.config.options(section):
                                print section, option, self.config.get(section, option)

        def get(self, section, option):
                if self.config.has_option(section, option):
                        return self.config.get(section, option)
                else:
                        return None

        def router_port(self):
                return self.get('router', 'port')

        def hive_servers_ports(self):
                servers = self.get('hive_servers', 'ports')
                if servers != None:
                        return servers.split(",")
                else:
                        return None


def make_command(command_list, port):
        result = ['hive', "-h", "localhost", "-p", port]
        for cmd in command_list:
                result.append(str(cmd))
        return result

def exec_command(req, port):
        command = make_command(req["command"], port)
        fp = tempfile.NamedTemporaryFile()
        if req["script"] != None:
                for line in req["script"]:
                        fp.write(line)
                command[command.index("-f") + 1] = fp.name
	logging.info("Hive command: " + ' '.join(command))
        task = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(out, err) = task.communicate()
	retcode = task.returncode
	return (retcode, out, err)


def worker_routine(worker_url, context, port):
        # exec hiveserver service with given port
        hiveserver_cmd = ["hive", "--service", "hiveserver", "-p", port]
	devnull = open('/dev/null', 'w')
        hiveserver = subprocess.Popen(hiveserver_cmd, stdout = devnull, stderr = devnull)

        worker = context.socket(zmq.REP)
        worker.connect(worker_url)

        while True:
                req_str = worker.recv()
		logging.info("Recv: " + req_str)
                req = json.loads(req_str)
                (retcode, out, err) = exec_command(req, port)
                rsp = {"retcode": retcode, "stdout": out, "stderr": err}
                rsp_str = json.dumps(rsp)
                worker.send(rsp_str)

        hiveserver.terminate()

def main():
	logging.basicConfig(format = "%(levelname)s:%(message)s", level = logging.INFO)
        logging.info("Start HiveServer Router")
        config = HiveServerRouterConfig("hsr.conf")
        router_port = config.router_port()
        if router_port == None:
                logging.error("No router port")
                sys.exit(1)

        url_worker = "inproc://workers"
        url_client = "tcp://*:" + router_port

        context = zmq.Context()

        clients = context.socket(zmq.ROUTER)
        clients.bind(url_client)

        workers = context.socket(zmq.DEALER)
        workers.bind(url_worker)

        ports = config.hive_servers_ports()
        if ports == None:
                logging.error("No hive server ports")
                sys.exit(1)

        for port in ports:
                thread = threading.Thread(target = worker_routine, args = (url_worker, context, port))
                thread.start()
        
        zmq.device(zmq.QUEUE, clients, workers)

        clients.close()
        workers.close()
        context.term()

if __name__ == "__main__":
        main()

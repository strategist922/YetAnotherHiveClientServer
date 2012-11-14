# Yet Another Hive Client and Server #

## Brief Introduction ##
Very simple hive client and server to work around concurrency problem of hive server (https://issues.apache.org/jira/browse/HIVE-80)

* Very simple implementation
* Very simple configuration
* Same command line argument with existing hive client


## Concurrent problem of hive server ##
HiveServer is buggy at concurrency. (https://issues.apache.org/jira/browse/HIVE-80)
Handling multiple job in single session has no problem, however, handling multiple sessions result in exception.
**YA-client/server** works around the above concurrent problem of hive server.


## Structure ##
<pre>
YA-hive-client ---\                  +--> HiveServer (Thrift service)
YA-hive-client ----\                 |--> HiveServer (Thrift service)
YA-hive-client -----> YA-hive-server +--> HiveServer (Thrift service)
...            ----/                 |--> HiveServer (Thrift service)
...            ---/                  |--> ...
</pre>


## Client ##
Command line option of YA-hive-client is very similar to hive client.


## Server ##
YA-hive-server routes requests of hive clients to hive server fairly. (round-robin)


## Getting Started ##
### Pre-requisited ###
zeromq (http://www.zeromq.org/) and its python-biding pyzmq
#### zeromq ####
1. Download source file (zeromq-*.tar.gz)
2. tar xvzf zeromq-*.tar.gz
3. cd zeromq-*
4. ./configure; make; make install

#### pyzmq ####
1. easy_install pyzmq


### YA-hive-server ###
**configuration file:** hsr.conf
<pre>
[router]
port: 5050

[hive_servers]
ports: 10001,10002,10003,10004,10005,10006,10007,10008,10009,10010
</pre>

**start server:** python HiveServerRouter.py

### YA-hive-client ###
python HiveClient.py --help

#### Response from server ####
JSON format
<pre>
{
	"retcode": 0,
	"stdout": "blah blah",
	"stderr": "blah blah"
}
</pre>

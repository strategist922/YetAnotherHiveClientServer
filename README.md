# Yet Another Hive Client and Server #

## Brief Introduction ##
Very simple hive client and server to work around concurrency problem of hive server (https://issues.apache.org/jira/browse/HIVE-80)

* Very simple implementation
* Very simple configuration
* Same command line argument with existing hive client


## Concurrent problem of hive server ##
HiveServer is buggy at concurrency. (https://issues.apache.org/jira/browse/HIVE-80)
There are some experiments including this (https://github.com/franklovecchio/hiveserver-loadtest).
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
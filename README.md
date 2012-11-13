Yet Another Hive Client and Server
==================================

Hive client and server to work around concurrency problem of hive server (https://issues.apache.org/jira/browse/HIVE-80)

Structure

YA-hive-client ---\                  +--> HiveServer (Thrift service)
YA-hive-client ----\                 |--> HiveServer (Thrift service)
YA-hive-client -----> YA-hive-server +--> HiveServer (Thrift service)
...            ----/                 |--> HiveServer (Thrift service)
...            ---/                  |--> ...

Client
Command line option of YA-hive-client is very similar to hive client.

Server
YA-hive-server routes requests of hive clients to hive server fairly. (round-robin)
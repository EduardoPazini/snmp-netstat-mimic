# SNMP Netstat Mimic

Lists IP addresses and ports being used by TCP and UDP applications for local server. It's implementation follows SNMP version 2c.

## Installation

You must have installed ``snmp`` on the manager machine as:

```console
$ sudo apt install snmp
```

and ``snmpd`` on the agent devices:

```console
$ sudo apt install snmpd
```

You will need to change the snmpd configuration file in /etc/snmp/snmpd.conf, add the following lines:

``
agentaddress udp:161,tcp:161,udp6:161,tcp6:161
``
``
rocommunity public
``
``
rwcommunity private
``

You can see/use my snmpd.conf, it's in the files in the directory.

## Usage

To list the established TCP and UDP connections on localhost, run

```console
$ python3 main.py
```

To list the established TCP connections on localhost, run

```console
$ python3 main.py -TCP
```

To list UDP connections on localhost, run

```console
$ python3 main.py -UDP
```

To list the established TCP and UDP connections on some agent host ``x.x.x.x``, run

```console
$ python3 main.py x.x.x.x
```

To list the established TCP connections on some agent host ``x.x.x.x``, run

```console
$ python3 main.py x.x.x.x -TCP
```

To list UDP connections on some agent host ``x.x.x.x``, run

```console
$ python3 main.py x.x.x.x -UDP
```

import os
import sys

from css import css


IP_LOCAL = '127.0.0.1'
TCP_OID = '.1.3.6.1.2.1.6.13'
UDP_OID = '.1.3.6.1.2.1.7.7'


def request(ip, protocolos):
    open('tcp.txt', 'w+').close()
    open('udp.txt', 'w+').close()
    
    for i in protocolos:
        request = 'snmpwalk -v 2c -c public ' + ip + ' '
        if i == 'UDP' or i == 'udp':
            request+= UDP_OID + ' >> udp.txt'
            os.system(request)
        elif i == 'TCP' or i == 'tcp':
            request+=TCP_OID + ' >> tcp.txt'
            os.system(request)
        else:
            print("Invalid Protocol")


def printResults(protocols):
    localIpUdp = [] 
    localPortUdp = [] 
    remoteIpUdp = []
    remotePortUdp = []

    with open('udp.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if(line.startswith('UDP-MIB::udpEndpointProcess.ipv4."')):
            newLine = line.split('UDP-MIB::udpEndpointProcess.ipv4."')[1]
            localIpUdp.append(newLine.split('.')[0] + '.' + newLine.split('.')[1] + '.' + newLine.split('.')[2] + '.' + newLine.split('.')[3][:-1])
            localPortUdp.append(newLine.split('.')[4])
            newLine = line.split('."')[2]
            remoteIpUdp.append(newLine.split('.')[0] + '.' + newLine.split('.')[1] + '.' + newLine.split('.')[2] + '.' + newLine.split('.')[3][:-1])
            newLine = line.split('".')[2]
            remotePortUdp.append(newLine.split('.')[0])
    
    localIpTcp = [] 
    localPortTcp = [] 
    remoteIpTcp = []
    remotePortTcp = []

    with open('tcp.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if(line.startswith('TCP-MIB::tcpConnState.') and line[-15:] == 'established(5)\n'):
            newLine = line.split('TCP-MIB::tcpConnState.')[1]
            splittedLine = newLine.split('.')
            localIpTcp.append(splittedLine[0] + '.' + splittedLine[1] + '.' + splittedLine[2] + '.' + splittedLine[3])
            localPortTcp.append(splittedLine[4])
            remoteIpTcp.append(splittedLine[5] + '.' + splittedLine[6] + '.' + splittedLine[7] + '.' + splittedLine[8])
            remotePortTcp.append(splittedLine[9].split(' ')[0])

    print(css.BOLD + "Aluno: Eduardo de Paula Pazini")
    head = "   Local IP\t     Local Port\t\t  Remote IP\t    Remote Port\n"
    fmt = "{b1:s}\t\t{b2:s}\t\t{b3:s}\t\t{b4:s}"

    for i in protocols:
        if(i == 'TCP' or i == 'tcp'):
            print(css.OKGREEN + "\n---------------------------------- TCP ---------------------------------\n"+ css.ENDC)
            print(css.BOLD + head + css.ENDC) 
            for item in range(len(localIpTcp)):
                print(fmt.format(b1=localIpTcp[item], b2=localPortTcp[item], b3=remoteIpTcp[item], b4=remotePortTcp[item]))
        if(i == 'UDP' or i == 'udp'):
            print(css.OKGREEN + "\n---------------------------------- UDP ----------------------------------\n"+ css.ENDC)
            print(css.BOLD + head + css.ENDC) 
            for item in range(len(localIpUdp)):
                if(remotePortUdp[item] != '0'):
                    print(fmt.format(b1=localIpUdp[item], b2=localPortUdp[item], b3=remoteIpUdp[item], b4=remotePortUdp[item]))


if __name__ == "__main__":
    if(len(sys.argv) == 1):
        ip = IP_LOCAL
        protocolos = ['TCP', 'UDP']
    elif(len(sys.argv) == 2):
        if '-' in sys.argv[1]:
            ip = IP_LOCAL
            protocolos = [sys.argv[1].split('-')[1]]
        else:
            ip = sys.argv[1]
            protocolos = ['TCP', 'UDP']
    else:
        ip = sys.argv[1]
        protocolos = [sys.argv[2].split('-')[1]]

    request(ip,protocolos)
    printResults(protocolos)

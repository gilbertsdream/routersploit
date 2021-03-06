import socket

from routersploit.core.exploit.exploit import Exploit
from routersploit.core.exploit.exploit import Protocol
from routersploit.core.exploit.option import OptBool
from routersploit.core.exploit.printer import print_status
from routersploit.core.exploit.printer import print_error
from routersploit.core.exploit.utils import is_ipv4
from routersploit.core.exploit.utils import is_ipv6


TCP_SOCKET_TIMEOUT = 8.0


class TCPCli(object):
    def __init__(self, tcp_target, tcp_port, verbosity=False):
        self.tcp_target = tcp_target
        self.tcp_port = tcp_port
        self.verbosity = verbosity

        self.peer = "{}:{}".format(self.tcp_target, self.tcp_port)

        if is_ipv4(self.tcp_target):
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif is_ipv6(self.tcp_target):
            self.tcp_client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            print_error("Target address is not valid IPv4 nor IPv6 address", verbose=self.verbosity)
            return None

        self.tcp_client.settimeout(TCP_SOCKET_TIMEOUT)

    def connect(self):
        try:
            self.tcp_client.connect((self.tcp_target, self.tcp_port))
            print_status(self.peer, "TCP Connection established", verbose=self.verbosity)
            return self.tcp_client

        except Exception as err:
            print_error(self.peer, "TCP Error while connecting to the server", err, verbose=self.verbosity)

        return None

    def send(self, data):
        try:
            return self.tcp_client.send(data)
        except Exception as err:
            print_error(self.peer, "TCP Error while sending data", err, verbose=self.verbosity)

        return None

    def recv(self, num):
        try:
            response = self.tcp_client.recv(num)
            return response
        except Exception as err:
            print_error(self.peer, "TCP Error while receiving data", err, verbose=self.verbosity)

        return None

    def recv_all(self, num):
        try:
            response = b""
            received = 0
            while received < num:
                tmp = self.tcp_client.recv(num - received)

                if tmp:
                    received += len(tmp)
                    response += tmp
                else:
                    break

            return response
        except Exception as err:
            print_error(self.peer, "TCP Error while receiving all data", err, verbose=self.verbosity)

        return None

    def close(self):
        try:
            self.tcp_client.close()
        except Exception as err:
            print_error(self.peer, "TCP Error while closing tcp socket", err, verbose=self.verbosity)

        return None


class TCPClient(Exploit):
    """ TCP Client exploit """

    target_protocol = Protocol.TCP

    verbosity = OptBool(True, "Enable verbose output: true/false")

    def tcp_create(self, target=None, port=None):
        tcp_target = target if target else self.target
        tcp_port = port if port else self.port

        tcp_client = TCPCli(tcp_target, tcp_port, verbosity=self.verbosity)
        return tcp_client

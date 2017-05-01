import dpkt
from dpkt.compat import compat_ord
import datetime
import socket


class pcap_reader:
    def __init__(self, filename):
        self.filename = filename

    def count_packets(self):
        counter = 0
        self.pcap = dpkt.pcap.Reader(open(self.filename))
        for ts in self.pcap:
            counter = counter + 1
        return counter

    def mac_addr(self, address):
        return ':'.join('%02x' % compat_ord(b) for b in address)

    def inet_to_str(self, inet):
        # First try ipv4 and then ipv6
        try:
            return socket.inet_ntop(socket.AF_INET, inet)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, inet)

    def read_packets(self):
        packets = []
        self.pcap = dpkt.pcap.Reader(open(self.filename))
        for ts, buf in self.pcap:
            timestamp =  str(datetime.datetime.utcfromtimestamp(ts))
            eth = dpkt.ethernet.Ethernet(buf)
            mac_src = self.mac_addr(eth.src)
            mac_dst = self.mac_addr(eth.dst)
            mac_type = eth.type
            if not isinstance(eth.data, dpkt.ip.IP):
                continue
            ip = eth.data
            ip_src = self.inet_to_str(ip.src)
            ip_dst = self.inet_to_str(ip.dst)
            ip_len = ip.len
            packet = {
                "ts": timestamp,
                "mac_src": mac_src,
                "mac_dst": mac_dst,
                "mac_type": mac_type,
                "ip_src": ip_src,
                "ip_dst": ip_dst,
                "ip_len": ip_len,
            }
            if ip.p == 6:
                # TCP Packet
                tcp = ip.data
                seq = tcp.seq
                src_port = tcp.sport
                dst_port = tcp.dport
                packet["seq"] = seq
                packet["src_port"] = src_port
                packet["dst_port"] = dst_port
                if dst_port == 80 and len(tcp.data) > 0:
                    http = dpkt.http.Request(tcp.data)
                    method = http.method
                    uri = http.uri
                    user_agent = http.headers['user-agent']
                    packet["app"] = "http"
                    packet["app_data"] = {
                        "method": method,
                        "uri": uri,
                        "user_agent": user_agent
                    }

            packets.append(packet)

        return packets

import time
from time import perf_counter as pc

from scapy.config import conf
from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import sr1
from scapy.supersocket import L3RawSocket


def traceroute(address, repeat, max_ttl,
               request_interval_in_seconds: int,
               timeout, packet_size: int):
    conf.L3socket = L3RawSocket
    visited = set()
    for i in range(1, max_ttl + 1):
        packet = IP(dst=address, ttl=i) / ICMP(seq=i) / (b'\xff' * packet_size)
        results = {}
        for j in range(repeat):
            start = pc()
            response = sr1(packet, verbose=False, timeout=timeout)
            end = pc()
            if (response and
                    response.getlayer(ICMP) and
                    response.getlayer(ICMP).type in {0, 11} and
                    response.getlayer(ICMP).code == 0):
                src_ip_address = response.getlayer(IP).src
                if src_ip_address in visited:
                    continue
                if src_ip_address not in results:
                    results[src_ip_address] = []
                results[src_ip_address].append((end - start) * 1000)
            time.sleep(request_interval_in_seconds)
        if not results:
            return
        result_line = f'{i}'
        for ip in results:
            visited.add(ip)
            result_line += f'  {ip}  '
            result_line += '  '.join(
                map(lambda x: f'{round(x, 3)} ms', results[ip]))
        print(result_line)

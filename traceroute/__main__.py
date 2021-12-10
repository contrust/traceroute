import argparse
import os
import socket
from functools import partial

from traceroute.main import traceroute


def parse_terminal_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'address',
        type=str,
        help='ipv4 address or domain for routing')
    parser.add_argument(
        '--timeout',
        type=partial(_positive_number, number_type=float),
        metavar='time_in_seconds',
        default=1,
        help='response timeout in seconds, 1 second by default'
    )
    parser.add_argument(
        '-r',
        '--repeat',
        metavar='number_of_requests',
        type=partial(_positive_number, number_type=int),
        default=3,
        help='number of requests for each ttl, 3 requests by default'
    )
    parser.add_argument(
        '-i',
        '--interval',
        metavar='time_in_seconds',
        type=partial(_positive_number, number_type=float),
        default=0,
        help='interval between requests in seconds, 0 by default'
    )
    parser.add_argument(
        '-t',
        '--ttl',
        metavar='max_ttl',
        type=partial(_positive_number, number_type=int),
        default=30,
        help='max ttl, 30 by default'
    )
    parser.add_argument(
        '-s',
        '--size',
        metavar='size',
        type=partial(_positive_number, number_type=int),
        default=60,
        help='icmp data size in bytes, 60 by default'
    )
    return parser.parse_args()


def _positive_number(string, number_type):
    try:
        number = number_type(string)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f'Can not cast {string} to {number_type}.')
    if number > 0:
        return number
    else:
        raise argparse.ArgumentTypeError(f"{string} is not positive number.")


def main():
    args_dict = vars(parse_terminal_arguments())
    address = args_dict['address']
    repeat = args_dict['repeat']
    ttl = args_dict['ttl']
    interval = args_dict['interval']
    timeout = args_dict['timeout']
    size = args_dict['size']
    try:
        traceroute(address, repeat, ttl, interval, timeout, size)
    except PermissionError:
        print('Please, run the programme with root privileges.')
    except socket.gaierror:
        print('You typed invalid address, check if it is correct.')


if __name__ == '__main__':
    main()

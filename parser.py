import argparse
from typing import List
from datetime import datetime, timedelta
import threading
import os
import mmap
import subprocess


# Alternative to subprocess approach for reading continuously written file which be memory efficient
def get_last_line(filename):
    """
    One of the ways how to handle reading from continuously written file.
    @param filename: File to process.
    @return: Returns last line of given using build-in library mmap.
    """
    with open(filename) as source:
        mapping = mmap.mmap(source.fileno(), 0, prot=mmap.PROT_READ)
    return mapping[mapping.rfind(b'\n', 0, -1)+1:]


def most_frequent(item_list: List):
    """
    Function that yields the most common item in the list.
    @param item_list: List of items.
    @return:
    """
    return max(set(item_list), key=item_list.count)


def convert_adjust_time(time_value: str, delta: int = 0, timestamp: bool = False) -> int:
    """
    Converts given ISO format/timestamp datetime and performing optional timedelta.
    @param time_value: ISO string / unix timestamp to convert.
    @param delta: Time delta in minutes.
    @param timestamp: Datetime is provided as unix timestamp.
    @return:
    """
    if timestamp:
        timestamp_adjusted = datetime.fromtimestamp(int(time_value[:10])) + timedelta(minutes=delta)
        return int(timestamp_adjusted.timestamp())
    elif not timestamp and isinstance(time_value, str):
        datetime_obj = datetime.fromisoformat(time_value.replace("Z", "+00:00"))
        datetime_obj_adjusted = datetime_obj + timedelta(minutes=delta)
        unix_obj = int(datetime_obj_adjusted.timestamp())
        return unix_obj
    else:
        raise ValueError('Wrong time format/type.')


def finite_parser(filename: str, host: str, init: str, end: str, timestamp: bool = False) -> List:
    """
    Implementation of parser which returns list of connected hostnames to given host during given period of time.
    @param filename: File to process.
    @param host: Host name string.
    @param init: Initial datetime, start of period.
    @param end: End datetime, end of period.
    @param timestamp: Datetime is provided as unix timestamp.
    @return: List of hostnames.
    """
    result = []
    # possible faint when using context manager, could ran into memory issue when selected too big of range
    with open(filename) as fp:
        line = fp.readline()
        while line:
            splitted = line.split(' ')
            # adjusting range to handle 5 minutes out of order possibility
            init_time = convert_adjust_time(init, -5, timestamp)
            end_time = convert_adjust_time(end, 5, timestamp)
            # odd length of timestamps inside input-file-1000.txt (13), valid length = 10, intention?
            data_time = int(str(splitted[0])[:10])
            if init_time <= data_time <= end_time:
                if host not in result and host == splitted[1]:
                    result.append(splitted[2].rstrip())
            line = fp.readline()

    return result


def infinite_parser(filename: str, hostname: str, log_period: int = 60):
    """
    Parsing infinite written log file and yields KPIs for given host during given timeframe.
    @param filename: File to process.
    @param hostname: Host name string.
    @param log_period: Period in minutes.
    """
    try:
        while True:
            start = datetime.now()
            connected = []
            received = []
            most_conn = []
            f = subprocess.Popen(['tail', '-Fn 1', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while datetime.now() - start < timedelta(minutes=log_period):
                line = f.stdout.readline().decode("utf-8")
                # print(line)
                splitted = line.strip().split(' ')
                if splitted[1] not in connected and hostname == splitted[1]:
                    connected.append(splitted[2])
                elif splitted[2] not in received and hostname == splitted[2]:
                    received.append(splitted[1])
                most_conn.append(splitted[1])
            result_most = most_frequent(most_conn)
            print(f'List of hostnames connected to hostname {hostname} in past {log_period} minutes: '
                  f'{connected} \n')
            print(f'List of hostnames which received connection from hostname {hostname} in past'
                  f' {log_period} minutes: {received} \n')
            print(f'Hostname that generated most connections in past {log_period} minutes: {result_most} \n')

    except KeyboardInterrupt:
        print('Indefinite logging parsing canceled.')


def log_parser(params):
    """
    Based of on user input performs finite or infinite log file parsing.
    @param params: "Set" of user input parameters.
    """
    if params.parse:
        print(finite_parser(params.file, params.hostname, params.init_datetime, params.end_datetime, params.timestamp))
    else:
        infinite_parser(params.file, params.hostname, params.logging_period)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script parsing given log file based on user input parameters.')

    parser.add_argument('file',
                        help='Filepath to log file.')
    parser.add_argument('--hostname', '-host', type=str,
                        help='Host name string')
    parser.add_argument('--parse', '-p', action='store_true',
                        help='If this switch is used, parsing will be done for given init_datetime <-> end_datetime '
                             'period.')
    parser.add_argument('--timestamp', '-t', action='store_true',
                        help='If this switch is used, timestamp will be expected as an input for given init_datetime'
                             ' <-> end_datetime period.')
    parser.add_argument('--init_datetime', '-init', type=str,
                        help='Initial datetime, in ISO format/unix timestamp, to process the log for given period.')
    parser.add_argument('--end_datetime', '-end', type=str,
                        help='End datetime, in ISO format/unix timestamp, to process the log for given period.')
    parser.add_argument('--logging_period', '-lp', type=int,
                        help='Logging period (in minutes) to change default 60min logging period. Debug/testing'
                             ' purposes.')

    args = parser.parse_args()
    log_parser(args)


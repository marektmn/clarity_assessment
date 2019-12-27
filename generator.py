from datetime import datetime
import random
from time import sleep
from typing import List
import argparse

# subset of hostnames from input-file-10000.txt
HOSTNAMES = ['Matina', 'Dmetri', 'Rehgan', 'Eron', 'Morrigan', 'Tailee', 'Jadon', 'Jarreth', 'Cerena', 'Kallan',
             'Markena', 'Nafeesa', 'Grantham', 'Zoeylynn', 'Liem', 'Alsatia', 'Anudeep', 'Suzu', 'Alyaa', 'Mystee',
             'Aselin', 'Taydon', 'Jewelee', 'Kadeshia', 'Raijon', 'Lasheena', 'Ayreanna', 'Vishan', 'Alizander',
             'Rishima', 'Naquesha', 'Averyanna', 'Zymari', 'Chaslyn', 'Kazim', 'Asianna', 'Maurita', 'Kypten',
             'Davionne']


def generate_log(filename: str, interval: float, hostnames: List):
    try:
        with open(filename, 'a') as f:
            while True:
                date = int(datetime.now().timestamp())
                random_hosts = random.sample(hostnames, 2)
                f.write(f'{date} {random_hosts[0]} {random_hosts[1]}\n')
                print(f'Writing {date} {random_hosts[0]} {random_hosts[1]}')
                sleep(interval)
                f.flush()  # THIS (pulls his hair)
    except KeyboardInterrupt:
        print("Done generating log!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script generating infinite log to process.')
    parser.add_argument('file',
                        help='Log file to process.')
    parser.add_argument('--interval', '-i', type=int, default=0.2,
                        help='Internal in seconds for which log entries will generated, default = 0.2s .')
    args = parser.parse_args()
    generate_log(args.file, args.interval, HOSTNAMES)

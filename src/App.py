#!/usr/bin/env python3

import asyncio
import random
import logging
import argparse

import Settings
import prometheus

from Peers import Peers
from datetime import datetime
from asyncio.streams import StreamReader, StreamWriter
from geoip_service import get_location_data


async def server(reader:StreamReader, writer:StreamWriter):
    try:
        ip, port = reader._transport.get_extra_info('peername')
        peer = (ip, port)
        Peers.add_peer(peer)
        connection_time = Peers.connections[peer]
        timestamp = connection_time.strftime('%Y-%m-%d %H:%M:%S')

        country_code, country = get_location_data(ip)

        logging.info(f'[{timestamp}] ACCEPT host={ip} port={port} country={country} country_code={country_code}')

        # prometheus logging
        prometheus.inc('connections_started')
        prometheus.inc('connections_per_ip', [ip, country_code])

        while True:
            writer.write(b'%x\r\n' % random.randint(0, 2 ** 32))
            connection_duration = Peers.get_connection_duration(peer)

            await asyncio.sleep(Settings.sleep_time)
            await writer.drain()

            prometheus.inc('connection_duration', [ip], Settings.sleep_time)

    except BrokenPipeError:
        # Peer disconnected
        Peers.remove_peer(peer)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f'[{timestamp}] CLOSE host={ip} port={port} time={connection_duration.total_seconds()}')

        prometheus.inc('connections_stopped')

    except Exception as e:
        logging.error('something bad happened')
        logging.error(str(e))


async def start_server(host, port):
    connection = await asyncio.start_server(server, host, port)
    async with connection:
        await connection.serve_forever()


def main():
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)

    parser = argparse.ArgumentParser(description='SSH Tarpit')
    parser.add_argument('--port', '-p', help=f'Set Port for the Tarpit (default {Settings.port})', default=Settings.port, type=int, action='store')
    parser.add_argument('--host', '-H', help=f'Set Host for the Tarpit (default {Settings.host})', default=Settings.host, type=str, action='store')
    parser.add_argument('--time', '-t', help=f'Set sleep time for ssh conenctions (default {Settings.sleep_time} in seconds)', default=Settings.sleep_time, type=float, action='store')
    parser.add_argument('--geoip', '-g', help=f'Set own Geoip Service. Pattern: http://domain/<ip>, (default {Settings.geoip_service})', default=Settings.geoip_service, type=str, action='store')
    args = parser.parse_args()

    Settings.sleep_time = args.time
    Settings.geoip_service = args.geoip

    asyncio.run(start_server(args.host, args.port))


if __name__ == '__main__':
    prometheus.start_server()
    main()

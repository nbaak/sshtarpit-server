#!/usr/bin/env python3

import asyncio
import random
import logging
import argparse
import settings
import errno

from countit_adapter import initialize
from peers import Peers
from delta_timer import DeltaTimer

from datetime import datetime
from asyncio.streams import StreamReader, StreamWriter
from geoip_service import get_location_data

countit = None


async def create_countit():
    global countit
    logging.info(f"creating countit object")
    countit = initialize()
    if countit.test_connection():
        logging.info(f"{str(countit)}")


async def server(reader:StreamReader, writer:StreamWriter):
    try:
        ip, port = reader._transport.get_extra_info('peername')
        peer = (ip, port)
        Peers.add_peer(peer)
        connection_time = Peers.connections[peer]
        dt = DeltaTimer()
        timestamp = connection_time.strftime('%Y-%m-%d %H:%M:%S')

        country_code, country = get_location_data(ip)

        logging.info(f'[{timestamp}] ACCEPT host={ip} port={port} country={country} country_code={country_code}')

        # countit logging
        countit.inc('connections_session', label="started", value=1)
        countit.inc('connections_per_ip', label=[ip, country_code], value=1)
        countit.inc('connections_per_country', label=[country_code, country], value=1)
        
        while True:
            writer.write(b'%x\r\n' % random.randint(0, 2 ** 32))
            connection_duration = Peers.get_connection_duration(peer)

            await asyncio.sleep(settings.sleep_time)
            await writer.drain()
            
            dtn = dt.delta_now()
            countit.inc('connections_duration', label=ip, value=dtn)
            # logging.info(f"[{timestamp}] ip={ip} is in here for another {dtn}s")

    except BrokenPipeError:
        # Peer disconnected
        Peers.remove_peer(peer)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f'[{timestamp}] CLOSE host={ip} port={port} time={connection_duration.total_seconds()}')

        countit.inc('connections_session', label='stopped', value=1)
        writer.close()
    
    except ConnectionResetError:
        # Peer disconnected
        Peers.remove_peer(peer)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"[{timestamp}] CLOSE (pipe broken) host={ip} port={port} time={connection_duration.total_seconds()}")
        # logging.info(f'[{timestamp}] CLOSE host={ip} port={port} time={connection_duration.total_seconds()}')

        countit.inc('connections_session', label='stopped', value=1)
        writer.close()
        
    except OSError as e:
        if e.errno == errno.EHOSTUNREACH:
            logging.info(f"[{timestamp}] CLOSE (host unreachable) host={ip} port={port} time={connection_duration.total_seconds()}")
        
        countit.inc('connections_session', label='stopped', value=1)
        writer.close()

    except Exception as e:
        logging.error('something bad happened')
        logging.error(str(e))
        Peers.remove_peer(peer)
        writer.close()


async def start_server(host, port):
    connection = await asyncio.start_server(server, host, port)
    async with connection:
        await connection.serve_forever()


def main():
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)

    parser = argparse.ArgumentParser(description='SSH Tarpit')
    parser.add_argument('--port', '-p', help=f'Set Port for the Tarpit (default {settings.port})', default=settings.port, type=int, action='store')
    parser.add_argument('--host', '-H', help=f'Set Host for the Tarpit (default {settings.host})', default=settings.host, type=str, action='store')
    parser.add_argument('--time', '-t', help=f'Set sleep time for ssh conenctions (default {settings.sleep_time} in seconds)', default=settings.sleep_time, type=float, action='store')
    parser.add_argument('--geoip', '-g', help=f'Set own Geoip Service. Pattern: http://domain/<ip>, (default {settings.geoip_service})', default=settings.geoip_service, type=str, action='store')
    args = parser.parse_args()

    settings.sleep_time = args.time
    settings.geoip_service = args.geoip
    
    asyncio.run(create_countit())
    asyncio.run(start_server(args.host, args.port))


if __name__ == '__main__':
    main()

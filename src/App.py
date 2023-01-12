#!/usr/bin/env python3

import asyncio
import random
import logging
import argparse

import Settings

from Peers import Peers
from datetime import datetime
from asyncio.streams import StreamReader, StreamWriter


async def server(reader:StreamReader, writer:StreamWriter):
    try:
        while True:
            ip, port = reader._transport.get_extra_info('peername')
            peer = (ip, port)
            if Peers.add_peer(peer):
                connection_time = Peers.connections[peer]
                timestamp = connection_time.strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f'[{timestamp}] ACCEPT host={ip} port={port}')
            
            writer.write(b'%x\r\n' % random.randint(0, 2 ** 32))

            await asyncio.sleep(Settings.sleep_time)
            await writer.drain()

    except BrokenPipeError:
        # Peer disconnected
        connection_duration = Peers.get_connection_duration(peer)

        Peers.remove_peer(peer)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'[{timestamp}] CLOSE host={ip} port={port} time={connection_duration.total_seconds()}')

    except Exception as e:
        logging.error('something bad happened')
        logging.error(e)


async def start_server(host, port):
    connection = await asyncio.start_server(server, host, port)
    async with connection:
        await connection.serve_forever()


def main():
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)

    parser = argparse.ArgumentParser(description="SSH Tarpit")
    parser.add_argument('--port', '-p', help=f"Set Port for the Tarpit (default {Settings.port})", default=Settings.port, type=int, action="store")
    parser.add_argument('--host', '-H', help=f"Set Host for the Tarpit (default {Settings.host})", default=Settings.host, type=str, action="store")
    parser.add_argument('--time', '-t', help=f"Set sleep time for ssh conenctions (default {Settings.sleep_time} in seconds)", default=Settings.sleep_time, type=float, action="store")
    args = parser.parse_args()

    Settings.sleep_time = args.time

    asyncio.run(start_server(args.host, args.port))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import asyncio
import random
import logging
import argparse

from Peers import Peers
from datetime import datetime


async def server(_reader, _writer):
    try:
        while True:
            peer = ':'.join(map(str, _reader._transport.get_extra_info('peername')))
            if Peers.add_peer(peer):
                connection_time = Peers.connections[peer]
                timestamp = connection_time.strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f'[{timestamp}] ACCEPT host={peer}')

            _writer.write(b'%x\r\n' % random.randint(0, 2 ** 32))

            await asyncio.sleep(3)
            await _writer.drain()

    except BrokenPipeError:
        connection_duration = Peers.get_connection_duration(peer)
        
        Peers.remove_peer(peer) # remove peer
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'[{timestamp}] CLOSE host={peer} time={connection_duration.total_seconds()}')

    except:
        logging.error('something bad happened')


async def start_server(port):
    connection = await asyncio.start_server(server, '0.0.0.0', port)
    async with connection:
        await connection.serve_forever()


def main():
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="SSH Tarpit")
    parser.add_argument('--port', '-p', help="Set Port for the Tarpit (default 22222)", default=22222, type=int, action="store")
    args = parser.parse_args()
    
    asyncio.run(start_server(args.port))


if __name__ == "__main__":
    main()

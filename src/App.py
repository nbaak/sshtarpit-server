#!/usr/bin/env python3

import asyncio
import random
import logging

from Peers import Peers


async def server(_reader, _writer):
    try:
        while True:
            peer = ':'.join(map(str, _reader._transport.get_extra_info('peername')))
            if Peers.add_peer(peer):
                logging.info(f'CONNECTED: {peer} at {Peers.connections[peer]}')

            _writer.write(b'%x\r\n' % random.randint(0, 2 ** 32))

            await asyncio.sleep(3)
            await _writer.drain()

    except BrokenPipeError:
        Peers.remove_peer(peer)
        duration = Peers.get_connection_duration(peer)
        logging.info(f'DISCONNECTED: {peer} - {duration}')

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
    # todo: argparser
    port = 22222

    asyncio.run(start_server(port))


if __name__ == "__main__":
    main()

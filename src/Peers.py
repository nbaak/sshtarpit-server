
import time


class Peers:

    connections = {}

    @classmethod
    def add_peer(cls, peer:str) -> bool:
        if peer not in cls.connections:
            cls.connections[peer] = time.time()
            return True
        return False

    @classmethod
    def remove_peer(cls, peer:str):
        if peer in cls.connections:
            cls.connections.pop(peer)

    @classmethod
    def get_connection_duration(cls, peer:str) -> float:
        return time.time() - cls.connections[peer]



import datetime


class Peers:

    connections = {}

    @classmethod
    def add_peer(cls, peer:str) -> bool:
        if peer not in cls.connections:
            cls.connections[peer] = datetime.datetime.now()
            return True
        return False

    @classmethod
    def remove_peer(cls, peer:str):
        if peer in cls.connections:
            cls.connections.pop(peer)

    @classmethod
    def get_connection_duration(cls, peer:str) -> float:
        return datetime.datetime.now() - cls.connections[peer]

    @classmethod
    def sort(cls):
        return sorted(cls.connections.items(), key=lambda p: p[1])

    @classmethod
    def number_open_connections(cls) -> int:
        return len(cls.connections)
        
        
        
        
        
        
        
        

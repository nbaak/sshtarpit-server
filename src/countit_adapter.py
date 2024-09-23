import logging
import settings
from countit_client import CountItClient


def initialize():
    # ceate connection
    global countit
    countit = CountItClient(server=settings.countit_server,
                                      port=settings.countit_port,
                                      token=settings.countit_secret)
    
    # create metrics
    try:
        cons = countit.add_metric("connections")
        cons_ip = countit.add_metric("connections_per_ip")
        cons_dur = countit.add_metric("connections_duration")
        
    except Exception as e:
        print(f"EXECPTION: {e}")
        
    return countit

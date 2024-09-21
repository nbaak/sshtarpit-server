

import settings
from countit_client import CountItClient

countit:CountItClient = CountItClient(server=settings.countit_server, 
                                      port=settings.countit_port, 
                                      token_file="countit.token")


def initialize():
    # create metrics
    countit.add_metric("connections")
    countit.add_metric("connections_per_ip")
    countit.add_metric("connection_duration")
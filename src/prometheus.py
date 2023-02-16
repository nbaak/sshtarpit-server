
import prometheus_client as prom
import Settings

metrics = {}


def initialize():
    metrics['connections_started'] = prom.Counter('connections_started', 'Total Connections started')
    metrics['connections_stopped'] = prom.Counter('connections_stopped', 'Total Connections stopped')
    metrics['connection_duration'] = prom.Counter('connection_time', 'Total Connection Time per ip', ['ip'])
    metrics['connections_per_ip'] = prom.Counter('connections_per_ip', 'Total Connections per Ip', ['ip', 'country_code'])


def inc(metric, labels=None, value=1):
    if metric in metrics and Settings.prometheus_enabled:
        if labels:
            metrics[metric].labels(*labels).inc(value)
        else:
            metrics[metric].inc(value)


def start_server():
    if Settings.prometheus_enabled:
        initialize()

        prom.start_http_server(Settings.prometheus_port)

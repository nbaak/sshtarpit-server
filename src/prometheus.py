
import prometheus_client as prom
import settings
import requests
from typing import Optional

metrics = {}


def initialize():
    metrics['connections_started'] = prom.Counter('connections_started', 'Total Connections started')
    metrics['connections_stopped'] = prom.Counter('connections_stopped', 'Total Connections stopped')
    metrics['connection_duration'] = prom.Counter('connection_time', 'Total Connection Time per ip', ['ip'])
    metrics['connections_per_ip'] = prom.Counter('connections_per_ip', 'Total Connections per Ip', ['ip', 'country_code'])


def inc(metric, labels=None, value=1):
    if metric in metrics and settings.prometheus_enabled:
        if labels:
            metrics[metric].labels(*labels).inc(value)
        else:
            metrics[metric].inc(value)


def start_server():
    if settings.prometheus_enabled:
        initialize()

        prom.start_http_server(settings.prometheus_port)


def get_prometheus_counter_value(prometheus_url:str, metric_name: str) -> Optional[float]:
    """
    Query Prometheus for the current value of a counter metric.
    
    Args:
        metric_name (str): The name of the Prometheus counter metric.
        
    Returns:
        Optional[float]: The value of the metric if found, otherwise None.
    """
    query_params = {
        'query': metric_name
    }
    
    try:
        response = requests.get(prometheus_url, params=query_params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        
        # Check if the response contains valid data
        if data["status"] == "success":
            result = data["data"]["result"]
            if result:
                # Return the value of the first result (assuming a single counter metric is queried)
                return float(result[0]["value"][1])
            else:
                print(f"Metric {metric_name} not found.")
                return None
        else:
            print(f"Prometheus query failed: {data['error']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None

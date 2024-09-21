from prometheus_client import start_http_server

start_http_server(8000)

def nope():
    
    import prometheus
    import time
    
    
    def simulate_metrics() -> None:
        """
        Simulate metric increments.
        """
        for _ in range(5):
            print("sending counter incs")
            prometheus.inc('connections_started')
            prometheus.inc('connections_stopped')
            prometheus.inc('connection_duration', labels=('192.168.1.1',), value=5)
            prometheus.inc('connections_per_ip', labels=('192.168.1.1', 'US'))
            time.sleep(2)
            
        print("counters incremented")
    
    
    def main(do_incremetns:bool=True) -> None:
        """
        Main function to start the Prometheus server, simulate metrics, and query values.
        """
        # Start the Prometheus metrics server
        # prometheus.start_server()
        print("Prometheus metrics server started")
        
        
        if do_incremetns:
            # Simulate some metric updates
            simulate_metrics()
            
            # Allow some time for metrics to be updated
            time.sleep(15)
    
        # Query and print counter values
        prometheus_url = "http://localhost:9090/api/v1/query"  # Adjust based on your Prometheus server
        query_result = prometheus.get_prometheus_counter_value(prometheus_url, 'connections_started')
        print(f"Connections started: {query_result}")
        print(f"Connections stopped: {prometheus.get_prometheus_counter_value(prometheus_url, 'connections_stopped')}")
        # print(f"Connection duration for 192.168.1.1: {prometheus.get_prometheus_counter_value(prometheus_url, 'connection_time{ip=\"192.168.1.1\"}')}")
        # print(f"Connections per IP 192.168.1.1: {prometheus.get_prometheus_counter_value(prometheus_url, 'connections_per_ip{ip=\"192.168.1.1\",country_code=\"US\"}')}")
    
    
    if __name__ == "__main__":
        main(do_incremetns=False)

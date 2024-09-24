import logging
import settings
from countit_client import CountItClient
import datetime


def get_countit_client() -> CountItClient:
    # ceate connection    
    return CountItClient(server=settings.countit_server,
                                      port=settings.countit_port,
                                      token=settings.countit_secret)


def initialize():
    countit = get_countit_client()
    
    # create metrics
    try:
        cs = countit.add_metric("connections_session", overwrite=True)
        cpi = countit.add_metric("connections_per_ip")
        cd = countit.add_metric("connections_duration")
        cpc = countit.add_metric("connections_per_country")
        
        logging.info(countit.metrics())
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logging.info(f"[{timestamp}] CREATED METRIC {cs}")
        logging.info(f"[{timestamp}] CREATED METRIC {cpi}")
        logging.info(f"[{timestamp}] CREATED METRIC {cd}")
        logging.info(f"[{timestamp}] CREATED METRIC {cpc}")
        
    except Exception as e:
        print(f"EXECPTION: {e}")
        
    return countit

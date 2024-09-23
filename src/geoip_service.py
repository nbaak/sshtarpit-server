# wrapper for Geoip Service

import requests
import settings


def get_location_data(ip:str):

    if settings.geoip_service:
        geoip_data = requests.get(f"{settings.geoip_service}/{str(ip)}").json()
        country_code = geoip_data['code']
        country = geoip_data['country']
        
        if country_code == "-":
            country_code = "unknown"
        if country == "-":
            country = "unknown"            
    else:
        country = 'unknown'
        country_code = 'unknown'

    return country_code, country



def test():
    ip = "92.206.197.156"
    print(get_location_data(ip))
    
    ip = "127.0.0.1"
    print(get_location_data(ip))


if __name__ == "__main__":
    test()
    
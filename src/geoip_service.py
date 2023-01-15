# wrapper for Geoip Service

import requests
import Settings


def get_location_data(ip:str):

    if Settings.geoip_service:
        geoip_data = requests.get(Settings.geoip_service + '/' + str(ip)).json()
        country_code = geoip_data['code'] if not '-' else 'unkown'
        country = geoip_data['country'] if not '-' else 'unkown'
    else:
        country = 'unknown'
        country_code = 'unknown'

    return country_code, country

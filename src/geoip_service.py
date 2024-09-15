# wrapper for Geoip Service

import requests
import settings


def get_location_data(ip:str):

    if settings.geoip_service:
        geoip_data = requests.get(settings.geoip_service + '/' + str(ip)).json()
        country_code = geoip_data['code'] if not '-' else 'unkown'
        country = geoip_data['country'] if not '-' else 'unkown'
    else:
        country = 'unknown'
        country_code = 'unknown'

    return country_code, country

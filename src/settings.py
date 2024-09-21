import env

env_vars = env.load('.env')

# Tarpit
host = "0.0.0.0"
port = 22222
sleep_time = 5

# Geoip
# default host is an docker internal host
geoip_service = env_vars.get("GEOIP_SERVER", None)

# Countit
countit_secret = env_vars.get("AUTH_TOKEN", None)
countit_server = env_vars.get("COUNTIT_SERVER", None)
countit_port = env_vars.get("COUNTIT_PORT", None)


# sshtarpit-server
SSH Tarpit Server inspired by skeeto's <a href="https://github.com/skeeto/endlessh">endlessh</a>


## Port Map
Ports and Services

- 3000: Grafana
- 22222: SSH (Tarpit)
- 22223: Geoip
- 22224: SSHTarpit

All Ports except 22222 are exposed to local (127.0.0.1).


## Why using a tarpit
There are many (mostly bots) people out there who try to connect to random servers on the internet. Mostly for harmful reasons. We can't stop them from doing so, but we can slow them down!


## Why building your own
I like to understand how things work and the best way to understand is to build it your self.
#!/bin/bash

docker compose build sshtarpit
docker compose stop
docker compose up

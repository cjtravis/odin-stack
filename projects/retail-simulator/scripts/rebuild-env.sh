#!/bin/bash

 docker-compose down --remove-orphans && sudo rm -rf ./data/postgres-data && docker-compose up --build

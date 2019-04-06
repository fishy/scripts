#!/bin/sh

if [ -z "$@" ]; then
  echo "Usage: $0 [service_name_1] [service_name_2] ..."
  exit -1
fi

for service in "$@"; do
  echo "Waiting for ${service} to start..."
  while true; do
    sleep 1
    /usr/sbin/service ${service} start
    if [ $? -eq 0 ]; then
      break
    fi
  done
done

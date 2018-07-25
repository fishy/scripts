#!/bin/sh

service=${1:-php7.2-fpm}

while true; do
  sleep 1
  /usr/sbin/service ${service} start
  if [ $? -eq 0 ]; then
    break
  fi
done

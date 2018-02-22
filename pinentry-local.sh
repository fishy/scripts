#!/bin/sh

if [ -z "$SSH_TTY" ]; then
  exec `which pinentry-gui` "$@"
else
  exec `which pinentry-tty` "$@"
fi

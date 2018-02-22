#!/bin/sh

if [ -z "$SSH_TTY" ]; then
  exec `which pinentry-mac` "$@"
else
  exec `which pinentry-curses` "$@"
fi

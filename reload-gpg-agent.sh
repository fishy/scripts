#!/bin/sh

gpgconf --kill gpg-agent && gpg-connect-agent reloadagent /bye

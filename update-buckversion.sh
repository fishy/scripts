#!/bin/sh

BUCKBIN=$(readlink `which buck`)
BUCKDIR=${BUCKBIN%bin/buck}

(cd ${BUCKDIR}; git rev-parse HEAD) >.buckversion

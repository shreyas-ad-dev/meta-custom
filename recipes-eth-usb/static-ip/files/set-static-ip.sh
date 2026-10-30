#!/bin/sh
if [ "$INTERFACE" = "eth0" ]; then
    ip link set eth0 up
    ip addr replace IP_ADDR_HERE dev eth0
fi

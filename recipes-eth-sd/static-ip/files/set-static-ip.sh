#!/bin/sh
ip link set eth0 up
ip addr replace IP_ADDR_HERE dev eth0
ip route flush dev eth0
ip route add SUB_NET_HERE dev eth0 src IP_ADDR_HERE 2>/dev/null || true

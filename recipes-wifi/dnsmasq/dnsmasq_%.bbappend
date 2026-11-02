FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

include conf/network-config.inc

SRC_URI += "file://dnsmasq.conf.in"

do_install:append() {
    install -d ${D}${sysconfdir}
    sed -e 's|@PI_HOTSPOT_DHCP_START@|${PI_HOTSPOT_DHCP_START}|g' \
        -e 's|@PI_HOTSPOT_DHCP_STOP@|${PI_HOTSPOT_DHCP_STOP}|g' \
        ${WORKDIR}/dnsmasq.conf.in > ${D}${sysconfdir}/dnsmasq.conf
    chmod 0644 ${D}${sysconfdir}/dnsmasq.conf
}

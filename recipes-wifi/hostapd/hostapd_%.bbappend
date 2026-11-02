FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

include conf/network-config.inc

SRC_URI += "file://hostapd.conf.in"

do_install:append() {
    install -d ${D}${sysconfdir}/hostapd
    sed -e 's|@PI_HOTSPOT_SSID@|${PI_HOTSPOT_SSID}|g' \
        -e 's|@PI_HOTSPOT_PSK@|${PI_HOTSPOT_PSK}|g' \
        ${WORKDIR}/hostapd.conf.in > ${D}${sysconfdir}/hostapd/hostapd.conf
    chmod 0600 ${D}${sysconfdir}/hostapd/hostapd.conf

}

FILES:${PN} += "${sysconfdir}/hostapd/hostapd.conf"

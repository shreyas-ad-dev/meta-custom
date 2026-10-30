FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

include conf/network-config.inc
SRC_URI += "file://wpa_supplicant.conf.in"

do_install:append() {
    install -d ${D}${sysconfdir}/wpa_supplicant
    sed -e 's|@WIFI_SSID@|${WIFI_SSID}|g' \
        -e 's|@WIFI_PSK@|${WIFI_PSK}|g' \
        ${WORKDIR}/wpa_supplicant.conf.in > ${D}${sysconfdir}/wpa_supplicant.conf
    # Install wpa_supplicant
    chmod 0600 ${D}${sysconfdir}/wpa_supplicant.conf
}

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://wpa_supplicant.conf"

do_install:append() {
    # Install wpa_supplicant
    install -m 0600 ${WORKDIR}/wpa_supplicant.conf ${D}${sysconfdir}/wpa_supplicant.conf
}

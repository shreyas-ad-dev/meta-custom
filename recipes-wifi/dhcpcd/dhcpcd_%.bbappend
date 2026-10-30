FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI += "file://dhcpcd.conf"

do_install:append() {
    # Install dhcpcd configuration
    install -m 0644 ${WORKDIR}/dhcpcd.conf ${D}${sysconfdir}/dhcpcd.conf
}

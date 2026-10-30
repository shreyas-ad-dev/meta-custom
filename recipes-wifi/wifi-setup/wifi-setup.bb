SUMMARY = "Automates Wi-Fi connection and routing via SysVinit"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://wifi-connect"

S = "${WORKDIR}"

inherit update-rc.d

INITSCRIPT_NAME = "wifi-connect"
INITSCRIPT_PARAMS = "defaults 98"

do_install() {
    # Install SysVinit script
    install -d ${D}${sysconfdir}/init.d
    install -m 0755 ${WORKDIR}/wifi-connect ${D}${sysconfdir}/init.d/wifi-connect
}

FILES:${PN} += "${sysconfdir}/init.d/wifi-connect"

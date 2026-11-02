SUMMARY = "Initializes virtual AP interface and starts hotspot services"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

include conf/network-config.inc

SRC_URI = "file://hotspot-init.sh.in"

S = "${WORKDIR}"

inherit update-rc.d

INITSCRIPT_NAME = "hotspot-init"
INITSCRIPT_PARAMS = "defaults 99"

do_install() {
    install -d ${D}${sysconfdir}/init.d
    sed -e 's|@PI_HOTSPOT_GATEWAY@|${PI_HOTSPOT_GATEWAY}|g'\
        ${WORKDIR}/hotspot-init.sh.in > ${D}${sysconfdir}/init.d/hotspot-init
    chmod 0755 ${D}${sysconfdir}/init.d/hotspot-init

}

FILES:${PN} += "${sysconfdir}/init.d/hotspot-init"

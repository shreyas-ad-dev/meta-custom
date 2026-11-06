SUMMARY = "Light strip HTTP Control Server"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://light_server.py \
           file://light_strip_fncns.py \
           file://light-server.init"

S = "${WORKDIR}"

inherit update-rc.d

INITSCRIPT_NAME = "light-server"
INITSCRIPT_PARAMS = "defaults 99"

RDEPENDS:${PN} = "python3-core python3-netserver python3-threading python3-rpi-ws281x"


do_install() {
    install -d ${D}${bindir}/scripts/light_server

    install -m 0755 ${WORKDIR}/light_server.py ${D}${bindir}/scripts/light_server
    install -m 0755 ${WORKDIR}/light_strip_fncns.py ${D}${bindir}/scripts/light_server

    install -d ${D}${sysconfdir}/init.d
    install -m 0755 ${WORKDIR}/light-server.init ${D}${sysconfdir}/init.d/light-server
}

FILES:${PN} += "${bindir}/scripts/light_server ${sysconfdir}/init.d/light-server"

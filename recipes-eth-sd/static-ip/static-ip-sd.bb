SUMMARY = "Forces static IP assignment on eth0 via SysVinit"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

include conf/network-config.inc

SRC_URI = " \
    file://set-static-ip.sh.in \
    file://static-ip \
"

S = "${WORKDIR}"

inherit update-rc.d

INITSCRIPT_NAME = "static-ip"
INITSCRIPT_PARAMS = "defaults 99"

do_install() {
    # Create /usr/local/bin inside the image rootfs
    install -d ${D}/usr/local/bin
    sed -e 's|@STATIC_IP_ETH0_SD@|${STATIC_IP_ETH0_SD}|g' \
        -e 's|@STATIC_SUBNET_ETH0_SD@|${STATIC_SUBNET_ETH0_SD}|g' \
        ${WORKDIR}/set-static-ip.sh.in > ${D}/usr/local/bin/set-static-ip.sh
    chmod 0755 ${D}/usr/local/bin/set-static-ip.sh

    # Create /etc/init.d and install SysVinit script
    install -d ${D}${sysconfdir}/init.d
    install -m 0755 ${WORKDIR}/static-ip ${D}${sysconfdir}/init.d/static-ip
}

FILES:${PN} += "/usr/local/bin/set-static-ip.sh ${sysconfdir}/init.d/static-ip"

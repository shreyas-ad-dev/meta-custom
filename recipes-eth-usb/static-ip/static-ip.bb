SUMMARY = "Forces static IP assignment on eth0 via udev"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    file://set-static-ip.sh \
    file://99-eth0-static.rules \
"

S = "${WORKDIR}"

do_install() {
    # Create /usr/local/bin inside the image rootfs
    install -d ${D}/usr/local/bin
    install -m 0755 ${WORKDIR}/set-static-ip.sh ${D}/usr/local/bin/set-static-ip.sh

    # Create /etc/udev/rules.d and install the rule
    install -d ${D}${sysconfdir}/udev/rules.d
    install -m 0644 ${WORKDIR}/99-eth0-static.rules ${D}${sysconfdir}/udev/rules.d/99-eth0-static.rules
}

FILES:${PN} += "/usr/local/bin/set-static-ip.sh ${sysconfdir}/udev/rules.d/99-eth0-static.rules"

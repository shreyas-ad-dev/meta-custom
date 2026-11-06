SUMMARY = "Touchscreen terminal and Keypad App"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://terminal_keypad.py \
           file://terminal_keypad_1.py"

S = "${WORKDIR}"

RDEPENDS:${PN} = "python3-core python3-misc python3-fcntl"


do_install() {
    install -d ${D}${bindir}/scripts/terminal_keypad

    install -m 0755 ${WORKDIR}/terminal_keypad.py ${D}${bindir}/scripts/terminal_keypad/
    install -m 0755 ${WORKDIR}/terminal_keypad_1.py ${D}${bindir}/scripts/terminal_keypad/
}

FILES:${PN} += "${bindir}/scripts/terminal_keypad"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://waveshare32b.dts"

do_patch:append() {
    install -m 0644 ${WORKDIR}/waveshare32b.dts ${S}/arch/arm/boot/dts/overlays/waveshare32b.dts
}

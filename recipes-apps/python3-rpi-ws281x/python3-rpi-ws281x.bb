SUMMARY = "Official Python wrapper for rpi_ws281x LED library"
HOMEPAGE = "https://github.com/rpi-ws281x/rpi-ws281x-python"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=9dcf340793a1d73c5211edc8238767dc"

SRC_URI = "file://rpi-ws281x-python"

S = "${WORKDIR}/rpi-ws281x-python/library"

inherit setuptools3

RDEPENDS:${PN} += "python3-core python3-io python3-ctypes"

require recipes-sato/images/core-image-sato.bb

SUMMARY = "Custom Sato Image for USB Boot (Udev Static IP)"

IMAGE_INSTALL:append = " udev-static-ip-support"


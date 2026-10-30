require recipes-sato/images/core-image-sato.bb

SUMMARY = "Custom Sato Image for SD card Boot (SysVinit Static IP)"

IMAGE_INSTALL:append = " \
    static-ip-sd \
    kernel-modules \
    linux-firmware-bcm43430 \
    wpa-supplicant \
    iw \
    dhcpcd \
    wifi-setup \
"

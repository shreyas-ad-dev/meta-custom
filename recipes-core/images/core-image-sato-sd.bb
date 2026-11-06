require recipes-sato/images/core-image-sato.bb

SUMMARY = "Custom Sato Image for SD card Boot (SysVinit Static IP)"

IMAGE_FEATURES += " package-management"

IMAGE_INSTALL:append = " \
    packagegroup-core-boot \
    packagegroup-base-wifi \
    packagegroup-base-bluetooth \
    kernel-modules \
    linux-firmware-bcm43430 \
    wpa-supplicant \
    iw \
    hostapd \
    dnsmasq \
    dhcpcd \
    wifi-setup \
    hotspot-init \
    static-ip-sd \
    python3 \
    python3-pip \
    python3-modules \
    python3-rpi-ws281x \
    terminal-keypad-app \
    light-server \
    evtest \
"


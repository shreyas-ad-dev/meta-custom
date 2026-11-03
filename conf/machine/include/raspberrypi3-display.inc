# Enable standard SPI bus driver
# KERNEL_DEVICETREE:append = " overlays/spi-bcm2835.dtbo overlays/waveshare32b.dtbo"

KERNEL_DEVICETREE:append = " overlays/waveshare32b.dtbo"

# ENABLE SPI and the display overlay in the target system config.txt
RPI_EXTRA_CONFIG += " \n \
dtparam=spi=on \n \
dtoverlay=waveshare32b \n \
"

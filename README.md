# Raspberry-Pi-High-Precision-AD-DA-Expansion-Board-codes
Raspberry Pi High-Precision AD/DA Expansion Board has example codes  from waveshare website, but it might not work. The DAC fails because the Bookworm OS blocks its SPI pins due to a library conflict, keeping the chip-select inactive and the output at 0 V. The code here solves that. + instruction of how to use it with raspberry pi + example code


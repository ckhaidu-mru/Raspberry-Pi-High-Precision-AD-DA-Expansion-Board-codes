# Raspberry-Pi-High-Precision-AD-DA-Expansion-Board-codes
Raspberry Pi High-Precision AD/DA Expansion Board has example codes  from waveshare website, but it might not work. The DAC fails because the Bookworm OS blocks its SPI pins due to a library conflict, keeping the chip-select inactive and the output at 0 V. The code here solves that. + instruction of how to use it with raspberry pi + example code

The example DAC code from waveshare failed for me because : 
- The system was running the newer Raspberry Pi OS Bookworm, which replaced the older GPIO driver with a stricter system called lgpio. This change affected how GPIO and SPI resources were managed by the operating system.
- The official Waveshare code attempted to use two libraries at the same time: RPi.GPIO and spidev. When the ADC code started, it claimed control of the SPI pins. When the DAC code later attempted to use the same pins, the operating system blocked access because the pins were already marked as busy.
- As a result, the DAC chip-select pin (GPIO 23) never activated. The DAC chip remained inactive and ignored all commands, which caused the LEDs to stay off and the output voltage to remain at 0 V.
- The issue was resolved by bypassing the problematic library and communicating directly with the hardware. This allowed the DAC to receive commands and operate correctly.

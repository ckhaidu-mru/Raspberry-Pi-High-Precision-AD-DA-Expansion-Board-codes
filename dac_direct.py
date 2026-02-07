import spidev
import time
import lgpio
import sys

# ==========================================
#              CONFIGURATION
# ==========================================
# Check the Yellow Jumper on your board!
# If VREF is connected to 5V, set this to 5.0
# If VREF is connected to 3.3V, set this to 3.3
VREF_VOLTAGE = 5.0

# The DAC Chip Select pin is GPIO 23 on this board
DAC_CS_PIN = 23
SPI_BUS = 0
SPI_DEVICE = 0

print(f"--- DAC DIRECT HARDWARE CONTROL ---")
print(f"System: Using lgpio (Bookworm Compatible)")
print(f"Reference Voltage: {VREF_VOLTAGE}V")

try:
    # 1. SETUP GPIO (Chip Select)
    # Open the main GPIO chip
    chip = lgpio.gpiochip_open(0)
    
    # Attempt to claim the pin. If it's already claimed by a previous run, 
    # we catch the error and keep going.
    try:
        lgpio.gpio_claim_output(chip, DAC_CS_PIN)
    except:
        pass 
    
    # Set CS High (Idle state) - The DAC waits for Low to listen
    lgpio.gpio_write(chip, DAC_CS_PIN, 1)

    # 2. SETUP SPI (Data Transmission)
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEVICE)
    spi.max_speed_hz = 1000000  # 1MHz speed
    spi.mode = 0b01             # Mode 1 (CPOL=0, CPHA=1) required for DAC8532

    print("\nREADY.")
    print(f"Type a voltage between 0 and {VREF_VOLTAGE} (e.g. 1.5)")
    print("Type 'q' to quit.")
    print("-" * 40)

    while True:
        # --- INPUT STEP ---
        user_input = input(f"Set Voltage > ")

        if user_input.lower() in ['q', 'exit', 'quit']:
            break

        try:
            # Convert text input to float number
            target_volts = float(user_input)

            # --- SAFETY LIMITS ---
            if target_volts < 0:
                print(f" [!] Too low. Setting to 0V")
                target_volts = 0.0
            elif target_volts > VREF_VOLTAGE:
                print(f" [!] Too high. Capping at {VREF_VOLTAGE}V")
                target_volts = VREF_VOLTAGE

            # --- CALCULATE 16-BIT VALUE ---
            # The DAC takes a number from 0 to 65535 (0xFFFF)
            # Formula: (Target / Reference) * Max_Value
            value_16bit = int((target_volts / VREF_VOLTAGE) * 65535)

            # Split into High Byte (MSB) and Low Byte (LSB)
            msb = (value_16bit >> 8) & 0xFF
            lsb = value_16bit & 0xFF

            # --- SEND TO DAC (Channel A) ---
            # 1. Pull CS Low (Wake up DAC)
            lgpio.gpio_write(chip, DAC_CS_PIN, 0)
            
            # 2. Send Data: [Command, MSB, LSB]
            # Command 0x30 = Write to Channel A register and Update Output
            spi.xfer([0x30, msb, lsb]) 
            
            # 3. Pull CS High (Execute Command)
            lgpio.gpio_write(chip, DAC_CS_PIN, 1)

            # --- SEND TO DAC (Channel B) ---
            # Do the same for Channel B (Command 0x34) so both LEDs light up
            lgpio.gpio_write(chip, DAC_CS_PIN, 0) 
            spi.xfer([0x34, msb, lsb])            
            lgpio.gpio_write(chip, DAC_CS_PIN, 1) 

            # Feedback to user
            print(f" -> OK: Output set to {target_volts:.4f} V")

        except ValueError:
            print(" [x] Error: Please enter a valid number.")

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    # Clean up connections
    spi.close()
    lgpio.gpiochip_close(chip)
    print("Cleanup Complete.")

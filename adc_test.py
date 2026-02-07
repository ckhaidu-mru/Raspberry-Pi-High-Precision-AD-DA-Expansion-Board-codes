import ADS1256
import time
import os

try:
    print("--- ADC INPUT TEST ---")
    
    # 1. Initialize the Board
    # This loads the config.py settings automatically
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    print("Reading... (Press Ctrl+C to stop)")

    while True:
        # 2. Read All Channels (0 - 7)
        # The library returns a raw 24-bit integer (0 to 8,388,607)
        
        # AIN0 is connected to the Blue Potentiometer (Jumpers ADJ <-> AD0)
        raw_0 = ADC.ADS1256_GetChannalValue(0)
        
        # AIN1 is connected to the Photoresistor (Jumpers LDR <-> AD1)
        raw_1 = ADC.ADS1256_GetChannalValue(1)
        
        # AIN2 is free for your external sensors
        raw_2 = ADC.ADS1256_GetChannalValue(2)

        # 3. Convert Raw Bits to Voltage
        # Formula: Value * VREF / MAX_BITS
        volt_0 = raw_0 * 5.0 / 0x7fffff
        volt_1 = raw_1 * 5.0 / 0x7fffff
        volt_2 = raw_2 * 5.0 / 0x7fffff

        # 4. Print Results
        # \033c clears the terminal screen so numbers stay in place
        print("\033c", end="") 
        print("==============================")
        print(f"AIN0 (Knob)   : {volt_0:.4f} V")
        print(f"AIN1 (Light)  : {volt_1:.4f} V")
        print(f"AIN2 (Sensor) : {volt_2:.4f} V")
        print("==============================")
        print("Turn the Blue Knob or cover the Light Sensor...")
        
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopped.")

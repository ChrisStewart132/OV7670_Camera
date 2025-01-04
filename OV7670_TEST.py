from machine import Pin, I2C, PWM
import time


# Configure PWM to generate XCLK signal
xclk_pin = Pin(12)  # Choose a GPIO pin for XCLK
pwm = PWM(xclk_pin)
pwm.freq(24000000)  # Set frequency to 24 MHz
pwm.duty_u16(32768)  # Set duty cycle to 50%
print("XCLK signal running...")
time.sleep(0.5)

# OV7670 I2C address
OV7670_I2C_ADDR = 0x21  # Default I2C address for OV7670 (7-bit), 0x42 for writing and 0x43 for reading.

# Pin definitions
RESET_PIN = 13  # Change as needed

# I2C configuration
#i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)  # Adjust pins/frequency as needed
i2c = I2C(1, scl=Pin(15, Pin.PULL_UP), sda=Pin(14, Pin.PULL_UP), freq=100000)

# Reset pin setup
reset = Pin(RESET_PIN, Pin.OUT)

def reset_camera():
    """Reset the OV7670 camera."""
    print("Resetting OV7670...")
    reset.value(0)  # Active low
    time.sleep(0.1)  # Hold reset for 100ms
    reset.value(1)  # Release reset
    time.sleep(0.1)  # Allow camera to stabilize

def read_register(reg):
    """Read a register from the OV7670."""
    try:
        return i2c.readfrom_mem(OV7670_I2C_ADDR, reg, 1)[0]
    except OSError as e:
        print(f"Error reading register {hex(reg)}: {e}")
        return None

def write_register(reg, value):
    """Write a value to a register in the OV7670."""
    try:
        i2c.writeto_mem(OV7670_I2C_ADDR, reg, bytes([value]))
    except OSError as e:
        print(f"Error writing register {hex(reg)}: {e}")

# Main program
def main():
    # Read COM7 register (0x12)
    com7_addr = 0x12
    initial_value = read_register(com7_addr)
    if initial_value is not None:
        print(f"Initial COM7 value: {hex(initial_value)}")
    else:
        print("Failed to read COM7 initially.")
        return

    # Modify COM7 register (example: toggle bit 0)
    new_value = initial_value ^ 0x01  # Flip the first bit as an example
    print(f"Writing new COM7 value: {hex(new_value)}")
    write_register(com7_addr, new_value)

    # Read back COM7 register
    updated_value = read_register(com7_addr)
    if updated_value is not None:
        print(f"Updated COM7 value: {hex(updated_value)}")
        if updated_value == new_value:
            print("I2C write successful!")
        else:
            print("I2C write failed: Mismatch in written value.")
    else:
        print("Failed to read COM7 after writing.")

# Run the main program
reset_camera()  # Ensure the camera is reset
print()
for i in range(3):
    main()
    time.sleep(0.5)



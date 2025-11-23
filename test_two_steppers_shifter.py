# test_two_steppers_shifter.py
#
# Quick test for:
# - SN74HC595 shift register
# - Two 28BYJ-48 stepper motors on one shifter
#
# Motor wiring assumption:
#   Motor 1 (e.g. azimuth)  -> Qe Qf Qg Qh  (upper 4 bits)
#   Motor 2 (e.g. elevation)-> Qa Qb Qc Qd  (lower 4 bits)
#
# Pin assumption (BCM):
#   DATA  -> GPIO16
#   CLOCK -> GPIO20
#   LATCH -> GPIO21

import time
import RPi.GPIO as GPIO
from shifter import Shifter   # from your class repo

# === EDIT THESE IF YOUR PINS ARE DIFFERENT ===
DATA_PIN  = 16
CLOCK_PIN = 20
LATCH_PIN = 21

# 8-step half-step sequence for 28BYJ-48
CYCLE = [
    0b0001,
    0b0011,
    0b0010,
    0b0110,
    0b0100,
    0b1100,
    0b1000,
    0b1001
]

STEPS_PER_REV = 4096
DELAY = 800 / 1e6   # 800 µs between steps (~1.25 kHz)

def move_motor(shifter, offset_bits, steps=512, direction=1):
    """
    Move one motor.

    offset_bits = 0  -> motor on Qa–Qd  (lower 4 bits)
    offset_bits = 4  -> motor on Qe–Qh  (upper 4 bits)
    """
    pos = 0
    for _ in range(steps):
        pos = (pos + direction) % 8
        pattern = CYCLE[pos] << offset_bits
        shifter.shiftByte(pattern)
        time.sleep(DELAY)

def all_off(shifter):
    """Turn off all outputs (no coils energized)."""
    shifter.shiftByte(0)

def main():
    GPIO.setmode(GPIO.BCM)

    # Set up the shifter
    s = Shifter(data=DATA_PIN, clock=CLOCK_PIN, latch=LATCH_PIN)

    print("Starting stepper + shift register test.")
    print("Motor 1 (upper bits) should rotate CW, then CCW.")
    print("Then Motor 2 (lower bits) will do the same.")
    print("Press Ctrl+C to stop.\n")

    try:
        # Motor 1 test (upper nibble: Qe–Qh -> offset 4)
        print("Motor 1: CW about 1/8 turn...")
        move_motor(s, offset_bits=4, steps=STEPS_PER_REV // 8, direction=1)
        time.sleep(0.5)

        print("Motor 1: CCW about 1/8 turn...")
        move_motor(s, offset_bits=4, steps=STEPS_PER_REV // 8, direction=-1)
        time.sleep(1.0)

        # Motor 2 test (lower nibble: Qa–Qd -> offset 0)
        print("Motor 2: CW about 1/8 turn...")
        move_motor(s, offset_bits=0, steps=STEPS_PER_REV // 8, direction=1)
        time.sleep(0.5)

        print("Motor 2: CCW about 1/8 turn...")
        move_motor(s, offset_bits=0, steps=STEPS_PER_REV // 8, direction=-1)
        time.sleep(1.0)

        print("Test finished. If both motors moved as described, wiring is good.")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        # Turn everything off and clean up GPIO
        try:
            all_off(s)
        except Exception:
            pass
        GPIO.cleanup()
        print("GPIO cleaned up.")

if __name__ == "__main__":
    main()

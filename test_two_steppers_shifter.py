# test_shift_outputs.py
#
# Turn on one 74HC595 output at a time (QA..QH)
# so you can see which motor/coil responds.

import time
import RPi.GPIO as GPIO
from shifter import Shifter  # same Shifter class you already use

# === Use the same pins you used before ===
DATA_PIN  = 16
CLOCK_PIN = 20
LATCH_PIN = 21

def main():
    GPIO.setmode(GPIO.BCM)

    s = Shifter(data=DATA_PIN, clock=CLOCK_PIN, latch=LATCH_PIN)

    try:
        while True:
            # bit 0..7 correspond to 8 outputs (in some order QA..QH)
            for bit in range(8):
                pattern = 1 << bit
                print(f"\nActivating bit {bit} (pattern: {pattern:08b})")
                s.shiftByte(pattern)
                print(">> Look which motor/coil moves or clicks now.")
                time.sleep(2.0)   # long enough to see what happens

            # turn everything off
            print("\nAll off")
            s.shiftByte(0)
            time.sleep(3.0)

    except KeyboardInterrupt:
        print("\nExiting test.")

    finally:
        s.shiftByte(0)
        GPIO.cleanup()
        print("GPIO cleaned up.")

if __name__ == "__main__":
    main()

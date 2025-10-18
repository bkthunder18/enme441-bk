"""
Shifter class for SN74HC595-style shift registers on Raspberry Pi.

Requirements from ENME441 Lab 6:
- Instantiate with serial (data), clock, and latch pins.
- Provide a public method `shiftByte()` to shift an 8 bit value into the register.
- Provide a private helper `__ping()` to toggle a pin (clock or latch) with proper timing.

Extras included here for convenience:
- `latch()` to copy the internal register to outputs.
- `write(value, msb_first=True)` which shifts and then latches in one call.
- `clear()` to blank outputs (writes 0x00 and latches).
- `cleanup()` to release GPIO when you're done.

Default bit order is MSB first so the visual order on typical LED bars matches
how binary literals are written (left→right). You can pass `msb_first=False`
if your wiring/example expects LSB first.
"""
from __future__ import annotations

import time
try:
    import RPi.GPIO as GPIO
except RuntimeError as e:
    raise


class Shifter:
    def __init__(self, serialPin: int, clockPin: int, latchPin: int, *,
                 setup_gpio: bool = True, bcm_mode: bool = True,
                 initial_low: bool = True, pulse_delay: float = 0.00005):
        """
        Create a Shifter.

        Args:
            serialPin: GPIO pin for data/serial input (DS/SER).
            clockPin:  GPIO pin for shift clock (SHCP/SRCLK).
            latchPin:  GPIO pin for latch clock (STCP/RCLK).
            setup_gpio: If True, configure GPIO here.
            bcm_mode:   If True, use BCM numbering (recommended).
            initial_low:If True, initialize clock & latch low.
            pulse_delay:Seconds to pause after raising/lowering a control pin.
                         50 µs is conservative and works on most setups.
        """
        self.serialPin = serialPin
        self.clockPin = clockPin
        self.latchPin = latchPin
        self._pulse_delay = float(pulse_delay)

        if setup_gpio:
            if bcm_mode:
                GPIO.setmode(GPIO.BCM)
            else:
                GPIO.setmode(GPIO.BOARD)

            GPIO.setup(self.serialPin, GPIO.OUT)
            if initial_low:
                GPIO.setup(self.clockPin, GPIO.OUT, initial=GPIO.LOW)
                GPIO.setup(self.latchPin, GPIO.OUT, initial=GPIO.LOW)
            else:
                GPIO.setup(self.clockPin, GPIO.OUT)
                GPIO.setup(self.latchPin, GPIO.OUT)

    def __ping(self, pin: int):
        """Private: short HIGH pulse then LOW on the given pin."""
        GPIO.output(pin, GPIO.HIGH)
        if self._pulse_delay:
            time.sleep(self._pulse_delay)
        GPIO.output(pin, GPIO.LOW)
        if self._pulse_delay:
            time.sleep(self._pulse_delay)

    def shiftByte(self, value: int, *, msb_first: bool = True):
        """
        Shift one 8-bit value into the shift register (no latch here).

        Args:
            value:      0..255 integer to shift in.
            msb_first:  If True, shift bit7→bit0; else bit0→bit7.
        """
        value &= 0xFF
        if msb_first:
            bit_range = range(7, -1, -1)
        else:
            bit_range = range(0, 8)

        for i in bit_range:
            bit = (value >> i) & 0x1
            GPIO.output(self.serialPin, GPIO.HIGH if bit else GPIO.LOW)
            # Rising edge clocks the bit into the shift register
            self.__ping(self.clockPin)

    def latch(self):
        """Copy the shifted 8 bits from the internal register to the outputs."""
        self.__ping(self.latchPin)

    def write(self, value: int, *, msb_first: bool = True):
        """Convenience: shift a byte and latch once so outputs update atomically."""
        self.shiftByte(value, msb_first=msb_first)
        self.latch()

    def clear(self):
        """Turn all outputs off (writes 0x00 and latches)."""
        self.write(0x00)

    def cleanup(self):
        """Release GPIO resources."""
        GPIO.cleanup()


if __name__ == "__main__":
    # Simple self-test / example: display 0b01100110 on the LED bar.
    dataPin, clockPin, latchPin = 23, 25, 24
    sh = Shifter(dataPin, clockPin, latchPin)
    try:
        pattern = 0b01100110
        sh.write(pattern, msb_first=True)  # set False if your visual order is mirrored
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sh.clear()
    finally:
        sh.cleanup()

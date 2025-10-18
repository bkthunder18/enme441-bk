"""
bug.py
ENME441 Lab 6 – Steps 4–6

- Uses Shifter to drive an 8-LED bar through a 74HC595.
- Bug class encapsulates movement and timing.
- Main loop monitors three buttons:
    s1 -> ON/OFF (hold to keep ON)
    s2 -> Toggle wrapping on each press (edge-detected)
    s3 -> 3x speed boost while held
"""

import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter

# ---------- Wiring (BCM numbering) ----------
# Shift register pins (match shifter.py demo)
DATA_PIN  = 23
CLOCK_PIN = 25
LATCH_PIN = 24

# Buttons (configure to suit your board)
S1_PIN = 5    # ON/OFF (active HIGH)
S2_PIN = 6    # Toggle wrap on edge
S3_PIN = 13   # 3x speed when HIGH

# Pull-downs assume buttons short pin -> 3.3V when pressed.
# If you wired with pull-ups (to GND on press), invert the reads below.


class Bug:
    """
    Bug class per lab step 5:
        timestep  : float (seconds)
        x         : int (LED position 0..7)
        isWrapOn  : bool (wrap at edges if True)
        __shifter : private Shifter used to drive LEDs

    Methods:
        start(), stop()
        update()  -> call often; advances when its timer elapses
    """
    def __init__(self, timestep: float = 0.1, x: int = 3, isWrapOn: bool = False,
                 shifter: Shifter | None = None):
        self.timestep = float(timestep)
        self.x = int(x)
        self.isWrapOn = bool(isWrapOn)
        self.__shifter = shifter if shifter is not None else Shifter(DATA_PIN, CLOCK_PIN, LATCH_PIN)

        self._running = False
        self._last_step = time.monotonic()
        self._speed_mult = 1.0  # changed by S3

    # Convenience alias, in case you prefer bug.wrap like the handout text
    @property
    def wrap(self) -> bool:
        return self.isWrapOn
    @wrap.setter
    def wrap(self, v: bool):
        self.isWrapOn = bool(v)

    def start(self):
        self._running = True
        self.show()

    def stop(self):
        self._running = False
        self.__shifter.clear()

    def toggle_wrap(self):
        self.isWrapOn = not self.isWrapOn

    def set_speed_multiplier(self, m: float):
        self._speed_mult = max(0.01, float(m))  # avoid zero/negative

    def show(self):
        # Display a single lit LED at position x
        pattern = 1 << max(0, min(7, self.x))
        self.__shifter.write(pattern)

    def step_random(self):
        # Move ±1, honoring wrap or clamping
        step = random.choice([-1, 1])
        if self.isWrapOn:
            self.x = (self.x + step) % 8
        else:
            self.x = min(7, max(0, self.x + step))

    def update(self):
        """Call frequently. If running and its timer elapsed, advance one step."""
        if not self._running:
            return
        interval = self.timestep / self._speed_mult
        now = time.monotonic()
        if now - self._last_step >= interval:
            self.step_random()
            self.show()
            self._last_step = now

    def cleanup(self):
        self.__shifter.cleanup()


def setup_inputs():
    GPIO.setmode(GPIO.BCM)
    for pin in (S1_PIN, S2_PIN, S3_PIN):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def main():
    setup_inputs()
    bug = Bug(timestep=0.05, x=3, isWrapOn=False)

    prev_s2 = GPIO.input(S2_PIN)  # for edge detection

    try:
        while True:
            s1 = GPIO.input(S1_PIN)
            s2 = GPIO.input(S2_PIN)
            s3 = GPIO.input(S3_PIN)

            # s1: ON/OFF (hold to keep ON)
            if s1:
                if not bug.wrap and bug.x not in range(0, 8):
                    bug.x = 3
                bug.start()
            else:
                bug.stop()

            # s2: toggle wrap on edge (press)
            if s2 != prev_s2 and s2 == GPIO.HIGH:
                bug.toggle_wrap()
            prev_s2 = s2

            # s3: 3x speed boost while held
            bug.set_speed_multiplier(3.0 if s3 else 1.0)

            # Update animation
            bug.update()
            time.sleep(0.005)  # light CPU sleep

    except KeyboardInterrupt:
        pass
    finally:
        bug.stop()
        bug.cleanup()


if __name__ == "__main__":
    main()

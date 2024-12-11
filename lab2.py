import RPi.GPIO as GPIO
import time

class Lab2:
    def __init__(self, blue_pins, red_pins):
        """
        Initialize the Lab1 class with the GPIO pins for blue and red LEDs.

        :param blue_pins: List of GPIO pins connected to blue LEDs.
        :param red_pins: List of GPIO pins connected to red LEDs.
        """
        self.blue_pins = blue_pins
        self.red_pins = red_pins

        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setwarnings(False)

        # Set up the GPIO pins as output
        for pin in self.blue_pins + self.red_pins:
            GPIO.setup(pin, GPIO.OUT)

    def blink_pattern1(self, delay=0.5):
        """
        Blink the LEDs in the pattern: all red, then all blue, with a delay between LEDs.

        :param delay: Delay in seconds between each LED blinking.
        """
        try:
            while True:
                # Turn on all red LEDs sequentially
                for pin in self.red_pins:
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(delay)
                # Turn off all red LEDs
                for pin in self.red_pins:
                    GPIO.output(pin, GPIO.LOW)

                # Turn on all blue LEDs sequentially
                for pin in self.blue_pins:
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(delay)
                # Turn off all blue LEDs
                for pin in self.blue_pins:
                    GPIO.output(pin, GPIO.LOW)
        except KeyboardInterrupt:
            print("\nBlinking stopped by user.")
        finally:
            GPIO.cleanup()

    def blink_pattern2(self, delay=0.5):
        """
        Blink the LEDs in a sequential pattern: from the first to the last and then back to the first.

        :param delay: Delay in seconds between each LED blinking.
        """
        all_pins = self.red_pins + self.blue_pins  # Combine red and blue pins for sequential pattern
        try:
            while True:
                # Turn on LEDs from left to right
                for pin in all_pins:
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(delay)
                    GPIO.output(pin, GPIO.LOW)
                # Turn on LEDs from right to left
                for pin in reversed(all_pins):
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(delay)
                    GPIO.output(pin, GPIO.LOW)
        except KeyboardInterrupt:
            print("\nBlinking stopped by user.")
        finally:
            GPIO.cleanup()

    def blink_pattern3(self, delay=0.5):
        """
        Blink the LEDs in a pattern: outer LEDs (1 and 8), then inner pairs, ending with middle LEDs (3 and 4).

        :param delay: Delay in seconds for each step in the pattern.
        """
        all_pins = self.red_pins + self.blue_pins  # Combine red and blue pins for pattern
        pattern_steps = [
            ([0, 7], []),
            ([1, 6], []),
            ([2, 5], []),
            ([0, 7], []),
            ([3, 4], []),
            ([], []),
            ([0, 7], []),
            ([1, 6], []),
            ([2, 5], []),
            ([0, 7], []),
            ([3, 4], []),
            ([], []),
        ]

        try:
            while True:
                for on_indices, _ in pattern_steps:
                    for index in on_indices:
                        GPIO.output(all_pins[index], GPIO.HIGH)
                    time.sleep(delay)
                    for index in on_indices:
                        GPIO.output(all_pins[index], GPIO.LOW)
        except KeyboardInterrupt:
            print("\nBlinking stopped by user.")
        finally:
            GPIO.cleanup()

# Example usage:
# Define GPIO pins for blue and red LEDs
blue_led_pins = [17, 18, 27, 22]  # Replace with your GPIO pin numbers
red_led_pins = [23, 24, 25, 12]  # Replace with your GPIO pin numbers

# Create an instance of the Lab1 class
lab = Lab2(blue_led_pins, red_led_pins)

# Run the blinking pattern
# lab.blink_pattern1(0.5)
# lab.blink_pattern2(0.5)
# Uncomment the line below to run the new pattern
# lab.blink_pattern3(0.5)

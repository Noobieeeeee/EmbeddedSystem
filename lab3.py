import RPi.GPIO as GPIO
import time

class Lab3:
    def __init__(self):
        """
        Initialize the Lab2 class with GPIO pins for traffic signals and 7-segment display.
        """
        # Traffic Signal A (East-West)
        self.red_A = 26
        self.yellow_A = 27
        self.green_A = 28

        # Traffic Signal B (North-South)
        self.red_B = 22
        self.yellow_B = 21
        self.green_B = 20

        # 7-segment display pins
        self.segments = [2, 3, 4, 5, 6, 8, 7, 0]  # Pins A-G, DP

        # Segment digit configurations
        self.digits = [
            [0, 0, 0, 0, 0, 0, 1, 1],  # 0
            [1, 0, 0, 1, 1, 1, 1, 1],  # 1
            [0, 0, 1, 0, 0, 1, 0, 1],  # 2
            [0, 0, 0, 0, 1, 1, 0, 1],  # 3
            [1, 0, 0, 1, 1, 0, 0, 1],  # 4
            [0, 1, 0, 0, 1, 0, 0, 1],  # 5
            [0, 1, 0, 0, 0, 0, 0, 1],  # 6
            [0, 0, 0, 1, 1, 1, 1, 1],  # 7
        ]

        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup pins as output
        self.traffic_pins = [self.red_A, self.yellow_A, self.green_A, self.red_B, self.yellow_B, self.green_B]
        for pin in self.traffic_pins + self.segments:
            GPIO.setup(pin, GPIO.OUT)

        self.reset_display()

    def reset_display(self):
        """Turn off all segments on the 7-segment display."""
        for pin in self.segments:
            GPIO.output(pin, GPIO.HIGH)

    def display_number(self, num):
        """Display a number on the 7-segment display."""
        for i in range(8):
            GPIO.output(self.segments[i], GPIO.LOW if self.digits[num][i] == 0 else GPIO.HIGH)

    def state_S0(self):
        """State S0: Green for Signal A, Red for Signal B."""
        GPIO.output(self.green_A, GPIO.HIGH)
        GPIO.output(self.red_B, GPIO.HIGH)
        GPIO.output(self.red_A, GPIO.LOW)
        for i in range(7, 0, -1):
            self.display_number(i)
            time.sleep(1)
        GPIO.output(self.green_A, GPIO.LOW)

    def state_S1(self):
        """State S1: Yellow for Signal A, Red for Signal B."""
        GPIO.output(self.yellow_A, GPIO.HIGH)
        GPIO.output(self.red_B, GPIO.HIGH)
        for i in range(2, 0, -1):
            self.display_number(i)
            time.sleep(1)
        GPIO.output(self.yellow_A, GPIO.LOW)

    def state_S2(self):
        """State S2: Red for both signals."""
        GPIO.output(self.red_A, GPIO.HIGH)
        GPIO.output(self.red_B, GPIO.HIGH)
        for i in range(2, 0, -1):
            self.display_number(i)
            time.sleep(1)

    def state_S3(self):
        """State S3: Green for Signal B, Red for Signal A."""
        GPIO.output(self.green_B, GPIO.HIGH)
        GPIO.output(self.red_A, GPIO.HIGH)
        GPIO.output(self.red_B, GPIO.LOW)
        for i in range(7, 0, -1):
            self.display_number(i)
            time.sleep(1)
        GPIO.output(self.green_B, GPIO.LOW)

    def state_S4(self):
        """State S4: Yellow for Signal B, Red for Signal A."""
        GPIO.output(self.yellow_B, GPIO.HIGH)
        GPIO.output(self.red_A, GPIO.HIGH)
        for i in range(2, 0, -1):
            self.display_number(i)
            time.sleep(1)
        GPIO.output(self.yellow_B, GPIO.LOW)

    def state_S5(self):
        """State S5: Red for both signals."""
        GPIO.output(self.red_A, GPIO.HIGH)
        GPIO.output(self.red_B, GPIO.HIGH)
        for i in range(2, 0, -1):
            self.display_number(i)
            time.sleep(1)

    def run(self):
        """Run the traffic signal simulation."""
        try:
            while True:
                self.reset_display()
                self.state_S0()
                self.reset_display()
                self.state_S1()
                self.reset_display()
                self.state_S2()
                self.reset_display()
                self.state_S3()
                self.reset_display()
                self.state_S4()
                self.reset_display()
                self.state_S5()
        except KeyboardInterrupt:
            print("\nTraffic signal simulation stopped by user.")
        finally:
            GPIO.cleanup()

# Example usage:
if __name__ == "__main__":
    lab3 = Lab3()
    lab3.run()

"""
# Importing the Lab2 class from lab3.py

from lab2 import Lab2

# Creating an instance of Lab2
lab2_instance = Lab2()

# Running the traffic signal simulation
lab2_instance.run()

"""
from machine import Pin, PWM, ADC
import utime

class Lab6:
    def __init__(self):
        # Joystick setup
        self.xAxis = ADC(Pin(27))
        self.yAxis = ADC(Pin(26))
        self.button = Pin(16, Pin.IN, Pin.PULL_UP)

        # Potentiometer setup for brightness control
        self.potentiometer = ADC(Pin(28))

        # Simulated Hall effect sensor on GPIO 29
        self.hall_effect_sensor = ADC(Pin(29))

        # LED setup
        self.led_red = PWM(Pin(15))
        self.led_green = PWM(Pin(14))
        self.led_blue = PWM(Pin(13))
        for led in [self.led_red, self.led_green, self.led_blue]:
            led.freq(1000)

        # Track selected LED and LED state (on/off)
        self.selected_led = self.led_red  # Default selected LED is red
        self.led_on = False  # LED starts off

    def display_status(self):
        # Read hall effect and potentiometer values
        hall_value = self.hall_effect_sensor.read_u16()
        pot_value = self.potentiometer.read_u16()

        # Calculate voltage from ADC reading (assuming 3.3V reference)
        voltage = pot_value * 3.3 / 65535

        # Display status on the console
        print(f"Hall Effect = {hall_value} | Potentiometer = {pot_value} | Voltage = {voltage:.2f}V")

    def joystick_control(self):
        # Joystick readings
        xValue = self.xAxis.read_u16()
        yValue = self.yAxis.read_u16()
        button_pressed = self.button.value() == 0

        # Joystick controls LED selection
        if xValue <= 600:
            self.selected_led = self.led_red
            print("Selected LED: Red")
        elif xValue >= 60000:
            self.selected_led = self.led_green
            print("Selected LED: Green")
        elif yValue <= 600:
            self.selected_led = self.led_blue
            print("Selected LED: Blue")

        # Toggle selected LED on/off when button is pressed
        if button_pressed:
            self.led_on = not self.led_on  # Toggle LED state
            utime.sleep(0.3)  # Debounce delay

        # Adjust brightness if LED is on
        if self.led_on:
            brightness = self.potentiometer.read_u16()  # Read potentiometer for brightness
            self.selected_led.duty_u16(brightness)  # Set brightness
        else:
            # If LED is off, set brightness to 0
            self.selected_led.duty_u16(0)

    def run(self):
        while True:
            self.joystick_control()
            self.display_status()
            utime.sleep(0.1)  # Delay for stability

# How to use this code if imported into another script:
# 1. Import the Lab6 class into your script: from lab6_joystick_led import Lab6
# 2. Create an instance of the Lab6 class: lab6 = Lab6()
# 3. Call the run() method to start the program: lab6.run()
# Note: Ensure that the hardware setup matches the pin configuration in this code.

# Create an instance of Lab6 and run it
if __name__ == "__main__":
    lab6 = Lab6()
    lab6.run()

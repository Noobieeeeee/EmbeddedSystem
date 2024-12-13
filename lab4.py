from machine import Pin, I2C
import utime
from lcd_api import I2cLcd  # Assuming lcd_api library is used

class Lab4:
    def __init__(self, i2c, lcd_address, button_pins, quiz):
        """
        Initialize the Lab4 quiz game class.

        :param i2c: I2C instance for the LCD.
        :param lcd_address: Address of the I2C LCD.
        :param button_pins: List of GPIO pins for buttons [A, B, C].
        :param quiz: List of quiz questions, options, and correct answers.
        """
        self.lcd = I2cLcd(i2c, lcd_address, 2, 16)  # Initialize LCD (2x16)
        self.buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]
        self.quiz = quiz
        self.current_question = 0
        self.score = 0
        self.incorrect = 0

    def display_question(self):
        """Display the current question and options on the LCD."""
        self.lcd.clear()
        question = self.quiz[self.current_question]
        self.lcd.putstr(question["question"])
        self.lcd.move_to(0, 1)
        self.lcd.putstr(" ".join(question["options"]))

    def display_feedback(self, correct):
        """Display feedback on the LCD based on the correctness of the answer."""
        self.lcd.clear()
        self.lcd.putstr("Correct!" if correct else "Incorrect!")
        utime.sleep(2)

    def get_answer(self):
        """Get the answer selected by the user via the buttons."""
        while True:
            for i, button in enumerate(self.buttons):
                if button.value() == 0:  # Button pressed
                    utime.sleep(0.2)  # Debounce delay
                    return chr(65 + i)  # Return 'A', 'B', or 'C'

    def evaluate_answer(self, answer):
        """Evaluate the user's answer and provide feedback."""
        correct = answer == self.quiz[self.current_question]["correctAnswer"]
        if correct:
            self.score += 1
        else:
            self.incorrect += 1
        self.display_feedback(correct)

    def display_score(self):
        """Display the final score on the LCD."""
        self.lcd.clear()
        self.lcd.putstr(f"Correct: {self.score}")
        self.lcd.move_to(0, 1)
        self.lcd.putstr(f"Wrong: {self.incorrect}")
        utime.sleep(5)

    def run(self):
        """Run the quiz game loop."""
        for self.current_question in range(len(self.quiz)):
            self.display_question()
            answer = self.get_answer()
            self.evaluate_answer(answer)
        self.display_score()

# Example usage:
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = 0x27

button_pins = [2, 3, 4]  # GPIO pins for buttons A, B, and C
quiz = [
    {"question": "3x - 5 = 4", "options": ["A: 3", "B: 2", "C: 1"], "correctAnswer": 'A'},
    {"question": "2x + 3 = 7", "options": ["A: 1", "B: 2", "C: 3"], "correctAnswer": 'B'},
    {"question": "x^2 = 4", "options": ["A: 1", "B: 3", "C: 2"], "correctAnswer": 'C'},
    {"question": "7x - 4 = 3", "options": ["A: 2", "B: 1", "C: 0"], "correctAnswer": 'B'},
    {"question": "6x - 12 = 0", "options": ["A: 1", "B: 2", "C: 3"], "correctAnswer": 'B'},
]

lab4 = Lab4(i2c, I2C_ADDR, button_pins, quiz)
lab4.run()

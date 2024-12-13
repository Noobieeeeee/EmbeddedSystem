from machine import Pin, SPI
from time import sleep

class MAX7219:
    def __init__(self, spi, cs_pin, num_matrices=1):
        self.spi = spi
        self.cs = Pin(cs_pin, Pin.OUT)
        self.num_matrices = num_matrices
        self.init_device()

    def write_cmd(self, address, data):
        self.cs.off()
        for _ in range(self.num_matrices):
            self.spi.write(bytearray([address, data]))
        self.cs.on()

    def init_device(self):
        self.write_cmd(0x09, 0x00)  # Decode mode (no decoding)
        self.write_cmd(0x0A, 0x03)  # Brightness (low)
        self.write_cmd(0x0B, 0x07)  # Scan limit (8 digits)
        self.write_cmd(0x0C, 0x01)  # Shutdown register (normal operation)
        self.write_cmd(0x0F, 0x00)  # Test mode (off)
        self.clear()

    def clear(self):
        for i in range(8):
            self.write_cmd(i + 1, 0x00)

    def display(self, data):
        # Convert the 2D list (8x8) to column data for MAX7219
        for col in range(8):  # There are 8 columns to write to
            column_data = 0
            for row in range(8):  # There are 8 rows in the shape
                if data[row][col] == 1:
                    column_data |= (1 << row)  # Set bit at row position
            self.write_cmd(col + 1, column_data)

# Define Pacman shape as a 2D array (8x8)
pacman = [
    [0, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0]
]

# Initialize SPI
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
cs = 5  # Chip Select (CS) pin

# Initialize MAX7219 with the defined SPI and CS pin
matrix = MAX7219(spi, cs)

# Display Pacman shape
try:
    while True:
        matrix.display(pacman)  # Display the Pacman shape
        sleep(1)  # Display it for 1 second
except KeyboardInterrupt:
    matrix.clear()  # Clear the display when interrupted

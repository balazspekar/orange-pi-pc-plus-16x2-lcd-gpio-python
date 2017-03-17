import time
from pyA20.gpio import gpio
from pyA20.gpio import port


class LCD():
		
	def __init__(self, rs=port.PA6, e=port.PD14, d4=port.PC4, d5=port.PC7, d6=port.PA21, d7=port.PA20):	
		
		# Define gpio to LCD mapping
		self.LCD_RS = rs
		self.LCD_E  = e
		self.LCD_D4 = d4
		self.LCD_D5 = d5
		self.LCD_D6 = d6
		self.LCD_D7 = d7

		# Define some device constants
		self.LCD_WIDTH = 16    # Maximum characters per line
		self.LCD_CHR = True
		self.LCD_CMD = False
		self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
		self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

		# Timing constants
		self.E_PULSE = 0.0005
		self.E_DELAY = 0.0005
		
		# Initialize gpio and lcd
		self.initialize_gpio()
		self.lcd_init()

		
	def initialize_gpio(self):
		gpio.init()
		gpio.setcfg(self.LCD_RS, gpio.OUTPUT)
		gpio.setcfg(self.LCD_E, gpio.OUTPUT)
		gpio.setcfg(self.LCD_D4, gpio.OUTPUT)
		gpio.setcfg(self.LCD_D5, gpio.OUTPUT)
		gpio.setcfg(self.LCD_D6, gpio.OUTPUT)
		gpio.setcfg(self.LCD_D7, gpio.OUTPUT)


	def lcd_init(self):
		# Initialise display
		self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
		self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
		self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
		self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
		self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
		self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
			

	def lcd_byte(self, bits, mode):
		# Send byte to data pins
		# bits = data
		# mode = True  for character
		#        False for command

		gpio.output(self.LCD_RS, mode) # RS

		# High bits
		gpio.output(self.LCD_D4, False)
		gpio.output(self.LCD_D5, False)
		gpio.output(self.LCD_D6, False)
		gpio.output(self.LCD_D7, False)
		if bits&0x10==0x10:
			gpio.output(self.LCD_D4, True)
		if bits&0x20==0x20:
			gpio.output(self.LCD_D5, True)
		if bits&0x40==0x40:
			gpio.output(self.LCD_D6, True)
		if bits&0x80==0x80:
			gpio.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self.lcd_toggle_enable()

		# Low bits
		gpio.output(self.LCD_D4, False)
		gpio.output(self.LCD_D5, False)
		gpio.output(self.LCD_D6, False)
		gpio.output(self.LCD_D7, False)
		if bits&0x01==0x01:
			gpio.output(self.LCD_D4, True)
		if bits&0x02==0x02:
			gpio.output(self.LCD_D5, True)
		if bits&0x04==0x04:
			gpio.output(self.LCD_D6, True)
		if bits&0x08==0x08:
			gpio.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self.lcd_toggle_enable()


	def lcd_toggle_enable(self):
		# Toggle enable
		time.sleep(self.E_DELAY)
		gpio.output(self.LCD_E, True)
		time.sleep(self.E_PULSE)
		gpio.output(self.LCD_E, False)
		time.sleep(self.E_DELAY)


	def lcd_string(self, message, line):
		# Send string to display
		if line == 1:
			line = self.LCD_LINE_1
		if line == 2:
			line = self.LCD_LINE_2
			
		message = message.ljust(self.LCD_WIDTH, " ")
		self.lcd_byte(line, self.LCD_CMD)

		for i in range(self.LCD_WIDTH):
			self.lcd_byte(ord(message[i]), self.LCD_CHR)

			
if __name__ == "__main__":
	screen = LCD() # pass the ports here if the defaults are not suitable for you
	screen.lcd_string("first line", 1) # print some text to the first line
	screen.lcd_string("and the second", 2) # and some to the second
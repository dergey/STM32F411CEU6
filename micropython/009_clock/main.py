import pyb
from machine import Pin, I2C
from ds3231_port import DS3231
from ssd1306 import SSD1306_I2C

i2c = I2C(sda=Pin('PB7'), scl=Pin('PB6'))
oled = SSD1306_I2C(128, 32, i2c)
clock = DS3231(i2c)

while True:
    time_array = clock.get_time()
    year = time_array[0]
    month = time_array[1]
    day = time_array[2]
    hour = time_array[3]
    minute = time_array[4]
    second = time_array[5]

    oled.fill(0)
    oled.text('Current time: ', 0, 0, 1)
    oled.text(str(day) + '.' + str(month) + '.' + str(year), 0, 12, 1)
    oled.text(str(hour) + ':' + str(minute) + ':' + str(second), 0, 24, 1)
    oled.show()
    pyb.delay(1000)

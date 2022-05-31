from pyb import Timer
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

b4 = Pin('PB4', Pin.IN, Pin.PULL_UP)
b5 = Pin('PB5', Pin.IN, Pin.PULL_UP)
a1 = Pin('PA1', Pin.IN, Pin.PULL_UP)
a2 = Pin('PA2', Pin.IN, Pin.PULL_UP)
speaker = Pin('PA10', Pin.OUT)

i2c = I2C(sda=Pin('PB7'), scl=Pin('PB6'))
display = SSD1306_I2C(128, 32, i2c)
numer_sel = 0
numbers = [0, 0, 0, 0]
counter = 0
stated = False


def text_center(s):
    x = 128 // 2 - len(s) * 4
    display.text(s, x, 12, 1)


def draw_initial():
    display.fill(0)
    text_center('00:00')
    display.show()

def a2_press():
    if not stated:
        if numer_sel == 0 and numbers[numer_sel] + 1 >= 3:
            numbers[numer_sel] = 0
        elif numer_sel == 1 and numbers[0] == 2 and numbers[numer_sel] + 1 >= 4:
            numbers[numer_sel] = 0
        elif numer_sel == 2 and numbers[0] == 2 and numbers[numer_sel] + 1 >= 4:
            numbers[numer_sel] += numbers[numer_sel] + 1


def b5_press():
    timer = Timer(1, freq=2)
    timer.callback(lambda t: speaker.value(1) if speaker.value() == 0 else speaker.value(0))


def b4_press():
    global menu_sel
    menu_sel = menu_sel + 1 if menu_sel < 2 else 0
    draw_menu()


b4.irq(lambda e: b4_press(), Pin.IRQ_RISING)
b5.irq(lambda e: b5_press(), Pin.IRQ_RISING)
a1.irq(lambda e: print_display("A1 KEY"), Pin.IRQ_RISING)
a2.irq(lambda e: print_display("A2 KEY"), Pin.IRQ_RISING)
draw_menu()

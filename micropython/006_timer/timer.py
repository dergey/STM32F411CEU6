import adafruit_framebuf
from adafruit_framebuf import FrameBuffer1
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

b4 = Pin('PB4', Pin.IN, Pin.PULL_UP)
b5 = Pin('PB5', Pin.IN, Pin.PULL_UP)
a1 = Pin('PA1', Pin.IN, Pin.PULL_UP)
a2 = Pin('PA2', Pin.IN, Pin.PULL_UP)
speaker = Pin('PA10', Pin.OUT)

speaker_art = bytearray('\x7E\x66\x66\x66\x66\x00')
i2c = I2C(sda=Pin('PB7'), scl=Pin('PB6'))
display = SSD1306_I2C(128, 32, i2c)
fb = display.framebuf
display.pixel()
menu_sel = 0


def print_display(string):
    fb.fill(0)
    fb.text(string, 0, 0, 1)
    display.show()


def draw_art(art, x, y, w, h):
    art = FrameBuffer1(art, w, h, framebuf.MONO_VLSB)
    fb.blit(art, x, y, -1)


def draw_menu_point(s, pos):
    if pos == menu_sel:
        s = ">" + s + "<"
    x = 128 // 2 - len(s) * 4
    y = pos * 12
    fb.text(s, x, y, 1)


def draw_menu():
    fb.fill(0)
    draw_menu_point('start', 0)
    draw_menu_point('record', 1)
    draw_menu_point('option', 2)
    display.show()


def b5_press():
    draw_art(speaker_art, 5, 5, 8, 8)
    # timer = Timer(1, freq=2)
    # timer.callback(lambda t: speaker.value(1) if speaker.value() == 0 else speaker.value(0))


def b4_press():
    global menu_sel
    menu_sel = menu_sel + 1 if menu_sel < 2 else 0
    draw_menu()


b4.irq(lambda e: b4_press(), Pin.IRQ_RISING)
b5.irq(lambda e: b5_press(), Pin.IRQ_RISING)
a1.irq(lambda e: print_display("A1 KEY"), Pin.IRQ_RISING)
a2.irq(lambda e: print_display("A2 KEY"), Pin.IRQ_RISING)
draw_menu()

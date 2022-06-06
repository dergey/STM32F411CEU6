import math

import pyb
from machine import Pin, I2C

import mpu6050
import ssd1306

PRECISION = 500

i2c = I2C(sda=Pin('PB7'), scl=Pin('PB6'))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
display = 0
mpu = mpu6050.accel(i2c)


def draw_pointer(dir, x: int, y: int, frame_buffer):
    if dir == "UP":
        frame_buffer.line(x + 2, y, x + 2, y + 6, 1)
        frame_buffer.pixel(x, y + 2, 1)
        frame_buffer.pixel(x + 1, y + 1, 1)
        frame_buffer.pixel(x + 4, y + 2, 1)
        frame_buffer.pixel(x + 3, y + 1, 1)
        return
    if dir == "DOWN":
        frame_buffer.line(x + 2, y, x + 2, y + 6, 1)
        frame_buffer.pixel(x, y + 4, 1)
        frame_buffer.pixel(x + 1, y + 5, 1)
        frame_buffer.pixel(x + 3, y + 5, 1)
        frame_buffer.pixel(x + 4, y + 4, 1)
        return
    if dir == "LEFT":
        frame_buffer.line(x, y + 3, x + 6, y + 3, 1)
        frame_buffer.pixel(x + 2, y + 1, 1)
        frame_buffer.pixel(x + 1, y + 2, 1)
        frame_buffer.pixel(x + 1, y + 4, 1)
        frame_buffer.pixel(x + 2, y + 5, 1)
        return
    if dir == "RIGHT":
        frame_buffer.line(x, y + 3, x + 6, y + 3, 1)
        frame_buffer.pixel(x + 4, y + 1, 1)
        frame_buffer.pixel(x + 5, y + 2, 1)
        frame_buffer.pixel(x + 5, y + 4, 1)
        frame_buffer.pixel(x + 4, y + 5, 1)
        return
    if dir == "NONE":
        frame_buffer.pixel(x + 2, y + 3, 1)
        return


def average_ac(n):
    list_acx = []
    list_acy = []
    list_acz = []
    for i in range(n):
        mpu_values = mpu.get_values()
        acx = int(mpu_values["AcX"])
        acy = int(mpu_values["AcY"])
        acz = int(mpu_values["AcZ"])
        list_acx.append(acx)
        list_acy.append(acy)
        list_acz.append(acz)
        pyb.delay(5)
    return {
        "acx": sum(list_acx) / len(list_acx),
        "acy": sum(list_acy) / len(list_acy),
        "acz": sum(list_acz) / len(list_acz)
    }


def average_gy(n):
    list_gyx = []
    list_gyy = []
    list_gyz = []
    for i in range(n):
        mpu_values = mpu.get_values()
        gyx = int(mpu_values["GyX"])
        gyy = int(mpu_values["GyY"])
        gyz = int(mpu_values["GyZ"])
        list_gyx.append(gyx)
        list_gyy.append(gyy)
        list_gyz.append(gyz)
        pyb.delay(5)
    return {
        "gyx": int(sum(list_gyx) / len(list_gyx) / PRECISION),
        "gyy": int(sum(list_gyy) / len(list_gyy) / PRECISION),
        "gyz": int(sum(list_gyz) / len(list_gyz) / PRECISION)
    }


def switch_display():
    global display
    display = display + 1 if display < 2 else 0


pyb.Switch().callback(lambda: switch_display())

while True:
    oled.fill(0)
    if display == 0:
        values = average_ac(10)
        oled.text("Position sensor:", 0, 0, 1)
        oled.text("acx = " + str(values["acx"]), 0, 8, 1)
        oled.text("acy = " + str(values["acy"]), 0, 16, 1)
        oled.text("acz = " + str(values["acz"]), 0, 24, 1)
        oled.show()
        continue
    if display == 1:
        values = average_gy(10)
        if math.fabs(values["gyx"]) > math.fabs(values["gyy"]):
            if values["gyx"] > 0:
                direction = "UP"
            elif values["gyx"] < 0:
                direction = "DOWN"
            else:
                direction = "NONE"
        elif math.fabs(values["gyx"]) < math.fabs(values["gyy"]):
            if values["gyy"] > 0:
                direction = "RIGHT"
            elif values["gyy"] < 0:
                direction = "LEFT"
            else:
                direction = "NONE"
        else:
            direction = "NONE"
        draw_pointer(direction, 0, 0, oled.framebuf)
        oled.text("Direction: " + direction, 8, 0, 1)
        oled.text("gyx = " + str(values["gyx"]), 0, 8, 1)
        oled.text("gyy = " + str(values["gyy"]), 0, 16, 1)
        oled.text("gyz = " + str(values["gyz"]), 0, 24, 1)
        oled.show()
        continue
    if display == 2:
        pyb.delay(25)
        tmp = mpu.get_values()["Tmp"]
        oled.text("tmp = " + str(tmp), 0, 0, 1)
        oled.show()
        continue

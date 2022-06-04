import pyb
from machine import Pin, I2C
import ssd1306
import mpu6050

i2c = I2C(sda=Pin('PB7'), scl=Pin('PB6'))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
display = 0
mpu = mpu6050.accel(i2c)


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
        "acx": sum(list_acx) / len(list_acx) / 100,
        "acy": sum(list_acy) / len(list_acy) / 100,
        "acz": sum(list_acz) / len(list_acz) / 100
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
        "gyx": sum(list_gyx) / len(list_gyx) / 100,
        "gyy": sum(list_gyy) / len(list_gyy) / 100,
        "gyz": sum(list_gyz) / len(list_gyz) / 100
    }

def switchDisplay():
    global display
    display = display + 1 if display < 2 else 0


pyb.Switch().callback(lambda: switchDisplay())

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
        oled.text("Gravity sensor:", 0, 0, 1)
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

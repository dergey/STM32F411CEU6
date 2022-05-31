import pyb

hid = pyb.USB_HID()

LEFT_SHIFT = 0x02
LEFT_GUI = 0x08


def release_key_once():
    buf = bytearray(8)  # report is 8 bytes long
    buf[2] = 0
    hid.send(buf)  # key released
    pyb.delay(10)


def press_key_once(key):
    buf = bytearray(8)  # report is 8 bytes long
    buf[2] = key
    hid.send(buf)  # key released
    pyb.delay(10)


def press_modifier_key(mod, key):
    buf = bytearray(8)  # report is 8 bytes long
    buf[0] = mod
    buf[2] = key
    hid.send(buf)
    pyb.delay(10)


def release_modifier_key():
    buf = bytearray(8)  # report is 8 bytes long
    buf[0] = 0
    buf[2] = 0
    hid.send(buf)  # key released
    pyb.delay(10)


def press_2key(key1, key2):
    buf = bytearray(8)  # report is 8 bytes long
    buf[2] = key1
    buf[3] = key2
    hid.send(buf)  # key released
    pyb.delay(10)


def release_2key():
    buf = bytearray(8)  # report is 8 bytes long
    buf[2] = 0
    buf[3] = 0
    hid.send(buf)  # key released
    pyb.delay(10)


pyb.delay(1000)
press_modifier_key(LEFT_GUI, 0x15)  # modifier WIN + button r
release_modifier_key()
pyb.delay(500)
press_key_once(0x06)  # button c
release_key_once()
pyb.delay(50)
press_key_once(0x10)  # button m
release_key_once()
pyb.delay(50)
press_key_once(0x07)  # button d
release_key_once()
pyb.delay(50)
press_key_once(0x28)  # button enter
release_key_once()
pyb.delay(1000)

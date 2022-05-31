from enum import Enum, unique
from typing import Sequence
from pyb import USB_HID
import pyb


@unique
class Key(Enum):
    KEY_A = 0x04
    KEY_B = 0x05
    KEY_C = 0x06
    KEY_D = 0x07
    KEY_E = 0x08
    KEY_F = 0x09
    KEY_G = 0x0A
    KEY_H = 0x0B
    KEY_I = 0x0C
    KEY_J = 0x0D
    KEY_K = 0x0E
    KEY_L = 0x0F
    KEY_M = 0x10
    KEY_N = 0x11
    KEY_O = 0x12
    KEY_P = 0x13
    KEY_Q = 0x14
    KEY_R = 0x15
    KEY_S = 0x16
    KEY_T = 0x17
    KEY_U = 0x18
    KEY_V = 0x19
    KEY_W = 0x1A
    KEY_X = 0x1B
    KEY_Y = 0x1C
    KEY_Z = 0x1D
    KEY_1 = 0x1E
    KEY_2 = 0x1F
    KEY_3 = 0x20
    KEY_4 = 0x21
    KEY_5 = 0x22
    KEY_6 = 0x23
    KEY_7 = 0x24
    KEY_8 = 0x25
    KEY_9 = 0x26
    KEY_0 = 0x27
    KEY_ENTER = 0x28
    KEY_ESCAPE = 0x29
    KEY_DELETE = 0x2A
    KEY_TAB = 0x2B
    KEY_SPACEBAR = 0x2C


@unique
class Modifier(Enum):
    LEFT_CONTROL = 0x01
    LEFT_SHIFT = 0x02
    LEFT_ALT = 0x04
    LEFT_GUI = 0x08
    RIGHT_CONTROL = 0x10
    RIGHT_SHIFT = 0x20
    RIGHT_ALT = 0x40
    RIGHT_GUI = 0x80


class Keyboard:
    def __init__(self, hid: USB_HID):
        self.hid = hid
        self.buf = bytearray(8)
        self.key_index = 2

    def use_modifier(self, modifiers: Sequence[Modifier]):
        modifier_byte = 0x00
        for modifier in modifiers:
            modifier_byte = modifier_byte & modifier.value
        self.buf[0] = modifier_byte

    def reset_modifier(self):
        self.buf[0] = 0x00

    def use_key(self, key: Key):
        if self.key_index < 8:
            self.buf[self.key_index] = key.value
            self.key_index += 1

    def commit(self):
        self.hid.send(self.buf)
        pyb.delay(10)

    def reset(self):
        self.buf = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.key_index = 2
        self.hid.send(self.buf)
        pyb.delay(10)

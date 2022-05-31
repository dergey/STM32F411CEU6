import pyb

from keyboard_lib import Keyboard, Key, Modifier

hid = pyb.USB_HID()
keyboard = Keyboard(hid)

pyb.delay(1000)

keyboard.use_key(Key.KEY_C)
# keyboard.py.use_modifier((Modifier.LEFT_SHIFT, Modifier.LEFT_CONTROL))
keyboard.commit()
keyboard.reset()
pyb.delay(50)

keyboard.use_key(Key.KEY_J)
keyboard.commit()
keyboard.reset()
pyb.delay(50)

keyboard.use_key(Key.KEY_C)
keyboard.commit()
keyboard.reset()
pyb.delay(50)

keyboard.use_key(Key.KEY_B)
keyboard.commit()
keyboard.reset()
pyb.delay(50)

keyboard.use_key(Key.KEY_SPACEBAR)
keyboard.commit()
keyboard.reset()

pyb.delay(1000)

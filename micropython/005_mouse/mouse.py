import math
import pyb

CIRCLE_RADIUS = 10


def osc(n, d):
    step_angle = 6.28319 / n
    for i in range(n):
        pyb.hid((0, int(CIRCLE_RADIUS * math.sin(i * step_angle)), int(CIRCLE_RADIUS * math.cos(i * step_angle)), 0))
        pyb.delay(d)


pyb.delay(1000)
while True:
    osc(200, 10)
    pyb.delay(1000)

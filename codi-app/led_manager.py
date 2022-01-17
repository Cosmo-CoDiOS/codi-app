"""
1 - TAB Led
2 - Right (top)
3 - Left (bottom)
4 - Keyboard backlight
"""

import logging

log = logging.getLogger("codi-app: ({})".format(__name__))


def set_leds(leds):
    for l in leds.keys():
        for c in leds[l]:
            setLed(l, c[0], c[1])


def set_led(ledId, color, enable):
    try:
        if (
            ledId >= 1
            and ledId <= 7
            and color >= 1
            and color <= 3
            and enable >= 0
            and enable <= 7
        ):
            s = str(ledId) + str(color) + str(enable)
            if ledId == 4:
                s = str(ledId) + str(enable)

            with open("/proc/aw9524_led_proc", "w") as f:
                f.write(s)
    except Exception as e:
        print(e)


def leds_incoming_call():
    leds = {2: [[1, 1], [2, 0], [3, 0]], 3: [[1, 0], [2, 1], [3, 0]]}
    setLeds(leds)


def leds_off():
    leds = {
        2: [[1, 0], [2, 0], [3, 0]],
        3: [[1, 0], [2, 0], [3, 0]],
        4: [[1, 0], [2, 0], [3, 0]],
        5: [[1, 0], [2, 0], [3, 0]],
        6: [[1, 0], [2, 0], [3, 0]],
        7: [[1, 0], [2, 0], [3, 0]],
    }

    setLeds(leds)


def leds_blue():
    leds = {2: [[1, 0], [2, 0], [3, 1]], 3: [[1, 0], [2, 0], [3, 1]]}
    setLeds(leds)


def leds_charging(state):
    if state:
        leds = {1: [[1, 1], [2, 0], [3, 0]]}
    else:
        leds = {1: [[1, 0], [2, 0], [3, 0]]}
    setLeds(leds)

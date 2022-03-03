import numpy as np

def block(time):
    t = time
    if t < 2:
        x = 150 - 150 * t
        y = 600
        phi6 = 3 * t

    elif t < 4:
        y = 600 - 150 * (t - 2)
        x = -150
        phi6 = -3 * t

    elif t < 6:
        x = -150 + 150 * (t - 4)
        y = 300
        phi6 = -6 * t
    else:
        y = 300 + 150 * (t - 6)
        x = 150
        phi6 = 0
    return (x, y, phi6)


def sin(time):
    t = time
    x = 500 - 48 * t
    y = 350 + 150 * np.sin(x / 50)
    phi6 = 3 * t

    return (x, y, phi6)

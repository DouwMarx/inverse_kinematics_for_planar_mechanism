import matplotlib.pyplot as plt
import numpy as np


def vel_block(time):
    a = np.array([0, 0, 0])

    mag = 10
    if time < 1:
        a[0] = mag
        a[2] = mag
    elif time < 2:
        a[1] = mag
        a[2] = - mag
    if time < 3:
        a[0] = -mag
    elif time < 4:
        a[1] = -mag
        a[2] = -mag
    return a


def smooth_squiggles(time):
    r = 0.2*(np.sin(10*time))*500 + 500
    omega = 2*np.pi*1
    phi = 2*np.pi*np.sin(time)
    theta = time*omega
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return np.array([x,y,phi])


def block(time):
    t = time
    half_d = 450
    if t < 2:
        x = half_d - half_d * t
        y = half_d
        phi6 = 3 * t

    elif t < 4:
        y = half_d - half_d * (t - 2)
        x = -half_d
        phi6 = -3 * t

    elif t < 6:
        x = -half_d + half_d * (t - 4)
        y = -half_d
        phi6 = -6 * t
    else:
        y = -half_d + half_d * (t - 6)
        x = half_d
        phi6 = 0
    return np.array([x, y, phi6])


def sin(time):
    t = time
    x = 500 - 48 * t
    y = 350 + 150 * np.sin(x / 50)
    phi6 = 3 * t

    return (x, y, phi6)

# t_range = np.linspace(0,7,100)
# coords = np.array([block(t)[0:2] for t in t_range])
# plt.figure()
# plt.scatter(x = coords[:,0],y=coords[:,1])

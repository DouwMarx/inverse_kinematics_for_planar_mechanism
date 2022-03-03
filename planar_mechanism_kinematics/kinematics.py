import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sympy as sp
import numpy as np
from planar_mechanism_kinematics.end_effector_paths import block
from planar_mechanism_kinematics.visualisation import MechanismPlotter

# Define the geometry of the mechanism
# see docs for a sketch descirbing the geometry

# There are 8 different

R1 = 100
R6 = 80
R3 = 800

R2 = 0.5*(R3-R1)
R5 = R2 - 2*R6
R4 = R3 - 2*R6 - 2*R5

L8 = R5 + R6
L7 = R4 + R5

m = 20



n = np.pi / 2
qlist = [0, n, n, n, n, n, n, n, n, 0, L7 + L8] # This is initialisation of important variables

n = 0

plotter_obj = MechanismPlotter()

def f(t):
    phi0, phi1, phi2, phi3, phi4, phi5, phi6, phi7, phi8, x, y = sp.symbols(
        "phi0, phi1, phi2, phi3, phi4, phi5, phi6, phi7, phi8, x, y")

    x, y, phi6 = block(t)  # sin(t)

    Cx = L7 * sp.cos(phi7) + L8 * sp.cos(phi8) - x
    Cy = L7 * sp.sin(phi7) + L8 * sp.sin(phi8) - y

    M = [Cx, Cy]
    V = sp.Matrix([phi7, phi8])
    sol = sp.solve(M, (phi7, phi8))

    phi7 = sol[0][0]
    phi8 = sol[0][1]

    C12 = (phi1 - phi7) * R1 + (phi2 - phi7) * R2
    C23 = (phi2 - phi7) * R2 - (phi3 - phi7) * R3
    C45 = (phi4 - phi7) * R4 + (phi5 - phi7) * R5
    C56 = (phi5 - phi8) * R5 + (phi6 - phi8) * R6
    C62 = (phi6 - phi8) * R6 - (phi2 - phi8) * R2

    PHI = sp.Matrix([C12, C23, C45, C56, C62])
    Var = sp.Matrix([phi1, phi2, phi3, phi4, phi5])
    # Jacobian = PHI.jacobian(Var)
    s = sp.solve(PHI, Var)
    s = list(s.values())
    s.append(phi6)
    s.append(phi7)
    s.append(phi8)
    s.append(x)
    s.append(y)
    s = [0] + s
    for i in range(len(s)): s[i] = float(s[i])

    plotter_obj.plot_mechanism_for_state(s)

    l = list(str(n))
    while len(l) < 3:
        l = ['0'] + l

    # plt.savefig("imagesblock1/" + "image-" + l[0] + l[1] + l[2] + ".png", dpi=300)  # ".png")
    plt.show()

    # return(p)


t_range = np.linspace(0,1,10)
for t in t_range:
    f(t)
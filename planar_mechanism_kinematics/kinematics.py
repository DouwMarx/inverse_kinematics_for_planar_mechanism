import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sympy as sp
import numpy as np
# from planar_mechanism_kinematics.end_effector_paths import block
# from planar_mechanism_kinematics.visualisation import MechanismPlotter

# Define the geometry of the mechanism
# see docs for a sketch descirbing the geometry

# There are 8 different

# Have a look at this
# https://nl.mathworks.com/help/symbolic/derive-and-apply-inverse-kinematics-to-robot-arm.html


L7, L8= sp.symbols("L7, L8")
phi7, phi8, phi6,x,y = sp.symbols("phi7, phi8, phi6, x, y")

# x, y, phi6 = block(t)  # sin(t)

zero_x = x - ( L7 * sp.cos(phi7) + L8 * sp.cos(phi8))
zero_y = y - ( L7 * sp.sin(phi7) + L8 * sp.sin(phi8))

sol_initial_cond = sp.solve([zero_x,zero_y],phi8,phi7)
print(sol_initial_cond)

jacobian = sp.Matrix([zero_x,zero_y]).jacobian([phi7,phi8])

print(jacobian)

# expression_for_phi7_in_terms_of_x = sp.solve(zero_x, phi7)[0]
# expression_for_phi7_in_terms_of_y = sp.solve(zero_y, phi7)[0]
# expression_for_phi8_in_terms_of_x = sp.solve(zero_x, phi8)[0]
# expression_for_phi8_in_terms_of_y = sp.solve(zero_y, phi8)[0]
#
# dphi7_dx = sp.diff(expression_for_phi7_in_terms_of_x,x)
# dphi7_dy = sp.diff(expression_for_phi7_in_terms_of_y,y)
#
# dphi8_dx = sp.diff(expression_for_phi8_in_terms_of_x,x)
# dphi8_dy = sp.diff(expression_for_phi8_in_terms_of_y,y)
#
# dphi6_dphi6 = 1
#
# for expression in [dphi7_dx,dphi7_dy,dphi8_dx,dphi8_dy]:
#     print(expression)
#
#
# phi6 = phi6




# PHI = sp.Matrix([Cx,Cy, C12, C23, C45, C56, C62])
# # Var = sp.Matrix([phi1, phi2, phi3, phi4, phi5])
# Var = sp.Matrix([x, y, phi6])
# Jacobian = PHI.jacobian(Var)

# print(Jacobian)
# s = sp.solve(PHI, Var)


# s = list(s.values())
# s.append(phi6)
# s.append(phi7)
# s.append(phi8)
# s.append(x)
# s.append(y)
# s = [0] + s
# for i in range(len(s)): s[i] = float(s[i])
#
# plotter_obj.plot_mechanism_for_state(s)

# l = list(str(n))
# while len(l) < 3:
#     l = ['0'] + l
#
# # plt.savefig("imagesblock1/" + "image-" + l[0] + l[1] + l[2] + ".png", dpi=300)  # ".png")
# plt.show()
#
# # return(p)
#

# t_range = np.linspace(0,1,10)
# for t in t_range:
#     f(t)
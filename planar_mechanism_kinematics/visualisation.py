import numpy as np
import matplotlib.pyplot as plt
from planar_mechanism_kinematics.mechanism import PlanarMechanism


class MechanismPlotter(PlanarMechanism):
    def __init__(self):
        super().__init__()

    def gearplot(self, x, y, phi, R):
        """
        Plot a single gear
        :param y:
        :param phi:
        :param R:
        :return:
        """

        # TODO: appending to a list is kinda gross
        teeth = int(2 * R / self.m)
        xvals = []
        yvals = []
        for i in np.linspace(0, 2 * np.pi, teeth + 1):
            xvals.append(x + R * np.cos(i + phi))
            yvals.append(y + R * np.sin(i + phi))

        plt.scatter(xvals, yvals, s=2)
        plt.scatter([x + R * np.cos(phi)], [y + R * np.sin(phi)], s=3)

    def plot_mechanism_for_state(self, q):
        # 1
        self.gearplot(0, 0, q[1], self.R1)

        # 2
        self.gearplot(np.cos(q[7]) * self.L7, np.sin(q[7]) * self.L7, q[2],
                      self.R2)  # Make the computation of these positions more clear

        # 3
        self.gearplot(0, 0, q[3], self.R3)

        # 4
        self.gearplot(0, 0, q[4], self.R4)

        # 5
        self.gearplot(np.cos(q[7]) * self.L7, np.sin(q[7]) * self.L7, q[5], self.R5)

        # 6
        self.gearplot(q[-2], q[-1], q[6], self.R6)
        plt.plot([q[-2], q[-2] + np.cos(q[6]) * self.R6], [q[-1], q[-1] + np.sin(q[6]) * self.R6], '-k')
        plt.scatter(q[-2], q[-1], marker="o", color="k")

        # 7
        plt.plot([0, np.cos(q[7]) * self.L7], [0, np.sin(q[7]) * self.L7], "-r")

        # 8
        plt.plot([np.cos(q[7]) * self.L7, q[-2]], [np.sin(q[7]) * self.L7, q[-1]], '-r')

        plt.text(-1300, 800, '$\phi_1$ = ' + str(round(q[1], 3)))
        plt.text(-1300, 700, '$\phi_4$ = ' + str(round(q[4], 3)))
        plt.text(-1300, 600, '$\phi_3$ = ' + str(round(q[3], 3)))
        # plt.text(-1300, 400, 't = ' + str(round(i, 3)))

        plt.text(-20, -820, '$D_1$')
        plt.text(-20, -260, '$D_2$')
        plt.text(-20, -95, '$D_3$')
        plt.axis('equal')
        plt.axis('off')

    # plt.show()

    # TODO:Add function that shows the path
    # # Point
    # pathx.append(q[-2])
    # pathy.append(q[-1])
    # plt.plot(pathx, pathy, "k--")

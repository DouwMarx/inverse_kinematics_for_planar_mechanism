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

    def plot_mechanism_for_state(self, q,name=0):
        # 1 Plot gear 1. it is centered at 0,0
        self.gearplot(0, 0, q[1], self.R1)

        # 2
        gear_2_x = np.cos(q[7]) * self.L7
        gear_2_y = np.sin(q[7]) * self.L7
        self.gearplot(gear_2_x, gear_2_y, q[2],
                      self.R2)  # Make the computation of these positions more clear

        # 3
        self.gearplot(0, 0, q[3], self.R3)

        # 4
        self.gearplot(0, 0, q[4], self.R4)

        # 5
        self.gearplot(np.cos(q[7]) * self.L7, np.sin(q[7]) * self.L7, q[5], self.R5)

        # 6
        # TODO, the plotting states, governing states and the auxilary states are confusing
        # Should have different naming conventinos than q
        x_knee = np.cos(q[7]) * self.L7
        y_knee = np.sin(q[7]) * self.L7

        x_end_effector = x_knee + np.cos(q[8]) * self.L8
        y_end_effector = y_knee + np.sin(q[8]) * self.L8

        self.gearplot(x_end_effector, y_end_effector, q[6], self.R6)
        plt.plot([x_end_effector, x_end_effector + np.cos(q[6]) * self.R6], [y_end_effector, y_end_effector + np.sin(q[6]) * self.R6], '-k')
        plt.scatter(x_end_effector, y_end_effector, marker="o", color="k")

        # 7
        plt.plot([0, x_knee], [0, y_knee], "-r")

        # 8
        plt.plot([x_knee, x_end_effector], [y_knee, y_end_effector], '-r')

        plt.text(-1300, 800, '$\phi_1$ = ' + str(round(q[1], 3)))
        plt.text(-1300, 700, '$\phi_4$ = ' + str(round(q[4], 3)))
        plt.text(-1300, 600, '$\phi_3$ = ' + str(round(q[3], 3)))
        # plt.text(-1300, 400, 't = ' + str(round(i, 3)))

        plt.text(-20, -820, '$D_1$')
        plt.text(-20, -260, '$D_2$')
        plt.text(-20, -95, '$D_3$')
        plt.axis('equal')
        # plt.axis('off')
        # plt.savefig("image-" + str(name) + ".png", dpi=300)  # ".png")
        plt.savefig("image-{0:03d}".format(name) + ".png", dpi=300)  # ".png")
        plt.close()

    def plot_mechanism_for_many_states(self,state_array):
        for i,state in enumerate(state_array.transpose()):
            self.plot_mechanism_for_state(state,name=i)

    def to_gif(self):
        import os

        # ffmpeg_command = "ffmpeg - f image2 - framerate 9 - i image_ % 003 d.jpg - vf scale = 531x299, transpose = 1, crop = 299, 431, 0, 100 out.gif"
        ffmpeg_command = "ffmpeg -i image-%003d.png out.gif"

        os.system(ffmpeg_command)
        os.system("y") # yes to overwrite



    # plt.show()

    # TODO:Add function that shows the path
    # # Point
    # pathx.append(q[-2])
    # pathy.append(q[-1])
    # plt.plot(pathx, pathy, "k--")

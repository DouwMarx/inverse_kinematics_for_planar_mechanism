import numpy as np
from planar_mechanism_kinematics.mechanism import PlanarMechanism
from planar_mechanism_kinematics.visualisation import MechanismPlotter
from planar_mechanism_kinematics.end_effector_paths import block,smooth_squiggles,PathFromArray
from pathlib import Path


# Load the array that defines the desired path.
example_path = np.load("example_path.npy") # load the desired path as a array

mechanism = PlanarMechanism()  # Define the mechanism object
path_function = PathFromArray(example_path,fs=1).get_path # Define an interpolation function based on the desired path provided as array
mechanism.set_desired_path(path_function)  # Assign a function that describes the end effector path with time


time_duration_to_solve_for = [0, 10] # Solve for 0-4 seconds
sol = mechanism.solve(time_duration_to_solve_for, fs=1)
#
# # # Pass the solution of the states to be plotted
plots_dir = Path.cwd().parent.joinpath("plots")
# plotter = MechanismPlotter()
# plotter.plot_mechanism_for_many_states(sol,plots_dir)
# plotter.to_gif(plots_dir)

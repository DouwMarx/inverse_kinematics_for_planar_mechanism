import numpy as np

from planar_mechanism_kinematics.mechanism import PlanarMechanism
from planar_mechanism_kinematics.visualisation import MechanismPlotter
from planar_mechanism_kinematics.end_effector_paths import block,smooth_squiggles
from pathlib import Path


mechanism = PlanarMechanism()  # Define the mechanism object
mechanism.set_desired_path(smooth_squiggles)  # Assign a function that describes the end effector path with time


time_duration_to_solve_for = [0, 1] # Solve for 0-4 seconds
# sol = mechanism.solve(time_duration_to_solve_for, fs=100)
# sol = mechanism.brute_force_solution(np.linspace(0,1,10))
sol = mechanism.solve([0,1],fs=10)

# # Pass the solution of the states to be plotted
plots_dir = Path.cwd().parent.joinpath("plots")
plotter = MechanismPlotter()
plotter.plot_mechanism_for_many_states(sol,plots_dir)
plotter.to_gif(plots_dir)

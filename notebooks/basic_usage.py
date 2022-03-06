from planar_mechanism_kinematics.mechanism import PlanarMechanism
from planar_mechanism_kinematics.visualisation import MechanismPlotter
from planar_mechanism_kinematics.end_effector_paths import block


mechanism = PlanarMechanism()  # Define the mechanism object
mechanism.set_desired_path(block)  # Assign a function that describes the end effector path with time


time_duration_to_solve_for = [0, 8] # Solve for 0-4 seconds
sol = mechanism.solve(time_duration_to_solve_for, fs=100)

# Pass the solution of the states to be plotted
plotter = MechanismPlotter()
plotter.plot_mechanism_for_many_states(sol)
plotter.to_gif()

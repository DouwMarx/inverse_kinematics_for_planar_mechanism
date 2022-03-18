import numpy as np
from scipy.integrate import solve_ivp
import scipy.optimize as opt
from scipy.misc import derivative

class PlanarMechanism(object):
    def __init__(self):
        # Solve for the required geometry
        self.R1 = 100
        self.R6 = 80
        self.R3 = 800

        self.R2 = 0.5 * (self.R3 - self.R1)
        self.R5 = self.R2 - 2 * self.R6
        self.R4 = self.R3 - 2 * self.R6 - 2 * self.R5

        self.L8 = self.R5 + self.R6
        self.L7 = self.R4 + self.R5

        self.m = 20  # Module of the gear teeth

        # Describes relationship between angles of gears in mechanism
        self.A = np.array([[self.R1, self.R2, 0, 0, 0],
                           [0, self.R2, -self.R3, 0, 0],
                           [0, 0, 0, self.R4, self.R5],
                           [0, 0, 0, 0, self.R5],
                           [0, -self.R2, 0, 0, 0]])

        self.end_effector_path = None
        self.end_effector_velocity = None

    # The derivativatives of these input variables are known and therefore your will be able to integrate to find these phi for a given x y and phi6 combo
    def solve_for_required_angles(self,q):
        phi7 = q[0]
        phi8 = q[1]

        phi6 = q[2]

        # C12 = (phi1 - phi7) * self.R1 + (phi2 - phi7) * self.R2
        # C23 = (phi2 - phi7) * self.R2 - (phi3 - phi7) * self.R3
        # C45 = (phi4 - phi7) * self.R4 + (phi5 - phi7) * self.R5
        # C56 = (phi5 - phi8) * self.R5 + (phi6 - phi8) * self.R6
        # C62 = (phi6 - phi8) * self.R6 - (phi2 - phi8) * self.R2

        # Unknowns: phi1,phi2,phi3,phi4,phi5

        # A = np.array([[self.R1, self.R2 , 0       , 0      , 0      ],
        #               [0      , self.R2 , -self.R3, 0      , 0      ],
        #               [0      , 0       , 0       , self.R4, self.R5],
        #               [0      , 0       , 0       , 0      , self.R5],
        #               [0      , -self.R2, 0       , 0      , 0      ]])

        b = np.array([-phi7 * self.R1 - phi7 * self.R2,
                      -phi7 * self.R2 + phi7 * self.R3,
                      -phi7 * self.R4 - phi7 * self.R5,
                      - phi8 * self.R5 + (phi6 - phi8) * self.R6,
                      (phi6 - phi8) * self.R6 + phi8 * self.R2])

        phi1_to_5 = np.linalg.solve(self.A, -b)
        phi6_to_8 = np.array([phi6, phi7, phi8])

        return np.hstack([np.array([0]), phi1_to_5, phi6_to_8])

    def jacobian(self, phi7, phi8):
        return np.array([[self.L7 * np.sin(phi7), self.L8 * np.sin(phi8), 0],
                         [-self.L7 * np.cos(phi7), -self.L8 * np.cos(phi8), 0],
                         [0, 0, 1]])  # dphia6/dphi6 = 1

    def inverse_jacobian(self, phi7, phi8):
        return np.linalg.inv(self.jacobian(phi7, phi8))

    def solve_inverse_problem_for_initial_condition(self, q_initial):
        print("Initial desired end effector location: ", q_initial)
        x = q_initial[0]
        y = q_initial[1]

        def objective(phis):
            return np.linalg.norm(np.array([x - (self.L7 * np.cos(phis[0]) + self.L8 * np.cos(phis[1])),
                             y - (self.L7 * np.sin(phis[0]) + self.L8 * np.sin(phis[1]))]))

        sol = opt.minimize(objective,np.array([-0.1,0.1]),tol=1e-6)
        # print(sol)

        if sol["success"] is not True:
            print("Problems with solving for initial condition: "+sol["message"])

        return np.hstack([sol["x"],q_initial[2]]) # Add the rotation back into the state dict

    def objective_for_inverse_probelm(self,phis,end_effector_position):

        x = end_effector_position[0]
        y = end_effector_position[1]
        # phi6 = end_effector_position[2]

        return np.linalg.norm(np.array([x - (self.L7 * np.cos(phis[0]) + self.L8 * np.cos(phis[1])),
                                        y - (self.L7 * np.sin(phis[0]) + self.L8 * np.sin(phis[1]))]))

    def solve_inverse_problem(self,x,y,phis_guess):
        sol = opt.minimize(self.objective_for_inverse_probelm, phis_guess, tol=1e-1)
        return sol["x"]

    def brute_force_solution(self,t_range):
        states = np.zeros((3,len(t_range)))
        phi_guess = np.array([0,0]) # initial guess
        for i,t in enumerate(t_range):
            end_effector_position = self.end_effector_path(t)
            state_xy = opt.minimize(self.objective_for_inverse_probelm, phi_guess,end_effector_position, tol=1e-4)["x"]
            state = np.hstack([state_xy,np.array([end_effector_position[2]])])
            states[:,i] = state
            phi_guess = state_xy # Current solution acts as optimisation start point for next iteration

        return states




    def dq_dt(self, t, q):
        end_effector_velocity = self.end_effector_velocity(t)
        # This will be array with [x_velocity,y_velocity,rotational_velocity]

        phi7 = q[0]
        phi8 = q[1]

        inv_jac = self.inverse_jacobian(phi7, phi8)

        return np.dot(inv_jac, end_effector_velocity)

    def solve_for_states(self, t_span,fs = 5):

        initial_end_effector_position = self.end_effector_path(0)
        initial_state_vector = self.solve_inverse_problem_for_initial_condition(initial_end_effector_position)

        t_start = t_span[0]
        t_end = t_span[1]
        t_duration = t_end - t_start
        t_range = np.linspace(t_start, t_end, int(t_duration * fs))

        sol = solve_ivp(self.dq_dt, t_span, initial_state_vector, t_eval= t_range,rtol =1e-2, atol = 1e-2)
        return sol["y"]

    def solve_for_auxiliary_states(self, solved_states):
        all_states = np.zeros((9,solved_states.shape[1]))
        for col in range(solved_states.shape[1]):
            all_states[:,col] = self.solve_for_required_angles(solved_states[:,col])
        return all_states

    def solve(self,t_span,fs = 10,method="brute_force"):
        if method=="jacobian":
            sol = self.solve_for_states(t_span,fs=fs)
        elif method=="brute_force":
            t_range = np.linspace(t_span[0],t_span[1],int((t_span[1]-t_span[0])*fs))
            sol = self.brute_force_solution(t_range)
        return self.solve_for_auxiliary_states(sol)

    def set_desired_path(self, end_effector_with_time_function):
        self.end_effector_path = end_effector_with_time_function
        self.end_effector_velocity = lambda eval_at: derivative(self.end_effector_path, eval_at, dx=1e-6)

def f(x):
    return x**2 + 1




def path(t):
    return np.array([t * 0.01, 0.1,1000*t])


def main():
    a = PlanarMechanism()

    q0 = path(0)
    print(q0)
    initial = a.solve_inverse_problem_for_initial_condition(q0)

    # func_to_integrate = a.dq_dt
    #



    a.end_effector_path = path

    t_span = [0, 1]
    initial_condition = np.array([0.1, 0.1,0])
    s = a.solve(t_span)
    return



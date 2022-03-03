class PlanarMechanism(object):
    def __init__(self):
        self.R1 = 100
        self.R6 = 80
        self.R3 = 800

        self.R2 = 0.5 * (self.R3 - self.R1)
        self.R5 = self.R2 - 2 * self.R6
        self.R4 = self.R3 - 2 * self.R6 - 2 * self.R5

        self.L8 = self.R5 + self.R6
        self.L7 = self.R4 + self.R5

        self.m = 20 # Module of the gear teeth


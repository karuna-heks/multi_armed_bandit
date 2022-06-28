"""

"""

import numpy as np


class Probability_fun:
    
    def __init__(self, time_start, time_finish):
        self.time_sim_start = time_start
        self.time_sim_finish = time_finish
        self.time_gen_start = self.time_sim_start - (self.time_sim_finish - self.time_sim_start)*0.1
        # calculate the range of function generation (- 10% of the difference to the start)
        self._generate_coef() # generate function coefficients
        
    def _generate_coef(self):
        # generate function coefficients
        self.tilt_shift = np.random.rand() * 0.0005 # Slope coefficient (m in y=mx+b)
        self.ampl_shift = (np.random.rand() - 0.3)*10 # added height coefficient
        self.time_shift = ((self.time_sim_finish - self.time_gen_start) * np.random.rand()).total_seconds() 
        # time shift coefficient (measured in seconds)
    
    def get_value(self, time):
        # generate function value
        value = -(time - self.time_shift)*self.tilt_shift
        if value > 1:
            return 0
        
        value = value + self.ampl_shift
        
        if value < 0:
            return 0.01
        else:
            return value
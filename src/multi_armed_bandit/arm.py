"""


"""

import numpy as np
import datetime
from .probability_fun import Probability_fun

class Arm:
    
    def __init__(self, 
                 time_start: datetime.datetime, 
                 time_finish: datetime.datetime, 
                 noise_width: float):
        
        self.time_start = time_start # simulation start time
        self.time_finish = time_finish # simulation end time
        
        self.noise_width = noise_width # noise standard deviation value
        self.fun = self._get_fun() # generate function of change probability
    
    def _get_fun(self):
        # prepare a law of change of probability for the arm
        return Probability_fun(self.time_start, self.time_finish)
    
    def get_probability(self, t):
        # calc probability for time t
        value = self.fun.get_value(t)
        if value > 0:
            noise = np.random.normal(0, self.noise_width) # шум
            result = value + noise
            if result < 0:
                return 0
            else:
                return result
        else:
            return 0


if __name__ == '__main__':
    start_dt = datetime.datetime.now()
    finish_dt = start_dt + datetime.timedelta(days=1)
    arm = Arm(time_start=start_dt,
              time_finish=finish_dt,
              noise_width=0.1)
    
    print(arm.get_probability(40))
    # should return 0 or a positive float (more often 0 than float)

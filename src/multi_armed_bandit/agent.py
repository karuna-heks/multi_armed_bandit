"""


"""

from collections import Counter
from math import sqrt, log10


class Agent:
    
    def __init__(self, strategy_num=1):
        self.strategy_num = strategy_num # number of possible strategies to choose from
        self.reward_counter = Counter() # reward sum counter for each arm
        self.selection_counter = Counter() # counter of the number of choices of each strategy
        
    
    def _save_step_results(self, step_results):
        self.arms = step_results['available_arms']
        self.last_reward = step_results['step_reward']
    
    
    def _update(self):
        # adding new arms to counters
        for i in self.arms:
            if i not in self.selection_counter:
                self.selection_counter[i] = 0
                self.reward_counter[i] = 0
        
        # updated counter values
        for key, val in self.last_reward.items():
            self.selection_counter[key] += 1
            self.reward_counter[key] += val
    
    def _calc_value(self, i):
        # calculation of the value for the variable i according to the chosen optimization algorithm
        
        i_count = self.selection_counter[i]
        total_count = sum(self.selection_counter.values())
        average_earn = self.reward_counter[i]/i_count
        
        return average_earn + sqrt( (2*log10(total_count)) / i_count )
    
    def _select_arm(self):
        # select arm(s) based on available data
        
        # select elements with zero selection counter
        select_list = [k for k, v in self.selection_counter.items() if v == 0]
        
        # for the rest: we recalculate their indicators, rank them in descending order
        results = {i:self._calc_value(i) for i in list(set(self.selection_counter.keys()) - set(select_list))}
        results = [k for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)]
        
        # merge lists, but there must be zero elements at the top
        results = select_list + results
        return results[0:self.strategy_num]
        
    
    def run_optimization(self, env_run, env_select):
        # start of the optimization algorithm in order to select the arms that bring the highest reward
        # the input is a method to start the simulation of the environment
        
        for step_results in env_run():
            
            # 1. save the results of the last step
            self._save_step_results(step_results)
            
            # 2. update internal variables to select the optimal hand
            self._update()
            
            # 3. choose the right hand
            selected = self._select_arm()
            env_select(selected)
            
            print("results:", step_results)
            print('reward_c:', self.reward_counter)
            print('selection_c:', self.selection_counter)
            print("selected:", selected)
            print("\n===============================\n")

    

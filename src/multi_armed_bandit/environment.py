"""

"""

from .arm import *
import pandas as pd
from tqdm.notebook import tqdm
from collections import Counter
import numpy as np


class Environment:
    
    def __init__(self, time_start, time_finish, step, earns_per_step):
        self.dt = step # simulation step (seconds)
        self.time_start = time_start # simulation start time
        self.time_finish = time_finish # simulation end time
        
        
        self.earns = earns_per_step # the total number of points that are distributed in 1 step
        self.arms = [] # arms (by the add_arm method will be added)
        self.selected_arms = [] # selected arms (contains only their indices. changed by the select_arms method)
    
    def add_arm(self, arm_type=None):
        if arm_type is None:
            # if the type is not set, then we put the hand "by default"
            self.arms.append(Arm(time_start=self.time_start,
                                 time_finish=self.time_finish,
                                 noise_width=0.1))
            
        elif arm_type in ['default', 'linear']:
            # if the type is set to default or linear, then set "default"
            self.arms.append(Arm(time_start=self.time_start,
                                 time_finish=self.time_finish,
                                 noise_width=0.1))
            
        else:
            # if any other is specified, then set "default"
            self.arms.append(Arm(time_start=self.time_start,
                                 time_finish=self.time_finish,
                                 noise_width=0.1))
     
    def _get_intervals(self, probabilities_list) -> (pd.DataFrame, float):
        # form a list of ranges based on the list of received probabilities
        
        # the input is a list with a set of probabilities for each hand
        
        # at the output, you need to form a dataframe where each line contains
        # a range of values for each probability, each hand
        prob_sum = 0
        output_list = []
        for num, prob in enumerate(probabilities_list):
            if prob < 0.001:
                continue
            
            min_val = prob_sum
            max_val = prob_sum + prob
            output_list.append({"arm_id": num, "min": min_val, "max": max_val})
            prob_sum = max_val
        return pd.DataFrame(output_list), prob_sum
            
    
    
    def run_env_sim(self):
        # running environment simulation (each iteration returns all results)
        each_step_distr = [] # distribution of reward for each step (for the report)
        self.selected_arms = [] # nullify the selected hands. then the first iteration will be without reward
        
        time_range = int((self.time_finish - self.time_start).total_seconds())
        for sim_time_sec in tqdm(range(0, time_range, self.dt)):
            
            intervals, max_prob = self._get_intervals([arm.get_probability(sim_time_sec) for arm in self.arms])
            # sum the probabilities and form the ranges
            
            if max_prob < 0.001:
                each_step_distr.append({"time_sec": sim_time_sec, "arm_reward_counter": Counter()})
                continue
            # if too few rewards have accumulated per step, then skip the step
            
            prob_distr = np.random.rand(int(self.earns*max_prob))*max_prob
            # generate self.earns random numbers in the range of sum of probabilities
            # adding a max_prob multiplier to the number of generated values makes the final distribution more realistic
            
            arm_reward = Counter()
            for prob in prob_distr:
                arm_id = intervals[(intervals['min'] <= prob) & (intervals['max'] > prob)]['arm_id'].iloc[0]
                arm_reward[arm_id] += 1
            # distribute the numbers by ranges and count the points earned
                
            
            step_result = {"time_sec": sim_time_sec, "arm_reward_counter": arm_reward}
            each_step_distr.append(step_result)
            # save the result per step for the full report and for the current step
            
            
            yield step_result
        self.simulation_report_df = pd.DataFrame(each_step_distr)
    
    def select_arms(self, selected_arms: list):
        self.selected_arms = selected_arms
    
    def run_bandit_sim(self):
        # run environment simulation when limited environment information is returned
        sim_time_sec = 0
        each_step_distr = [] # for report (plot)
        each_step_reward = [] # for report (metrics calculation)
        available_arms = [] # for feedback to agent

        time_range = int((self.time_finish - self.time_start).total_seconds())
        for sim_time_sec in tqdm(range(0, time_range, self.dt)):
            
            intervals, max_prob = self._get_intervals([arm.get_probability(sim_time_sec) for arm in self.arms])
            # sum the probabilities and form the ranges
            
            
            if max_prob < 0.001:
                each_step_distr.append({"time_sec": sim_time_sec, "arm_reward_counter": Counter()})
                continue
            # if too few rewards have accumulated per step, then skip the step
            
            prob_distr = np.random.rand(int(self.earns*max_prob))*max_prob
            # generate self.earns random numbers in the range of sum of probabilities
            # adding a max_prob multiplier to the number of generated values makes the final distribution more realistic
            
            arm_reward = Counter()
            for prob in prob_distr:
                arm_id = intervals[(intervals['min'] <= prob) & (intervals['max'] > prob)]['arm_id'].iloc[0]
                arm_reward[arm_id] += 1
            # distribute the numbers by ranges and count the points earned
                
            
            step_result = {"time_sec": sim_time_sec, "arm_reward_counter": arm_reward}
            each_step_distr.append(step_result)
            # save the result for a step for a full report
            
            
            available_arms = list(set(available_arms + list(arm_reward.keys())))
            step_reward = {i:arm_reward[i] for i in self.selected_arms}
            step_result_for_agent = {"time_sec": sim_time_sec, 
                                     "available_arms": available_arms,
                                     "step_reward": step_reward}
            # save the result for the step report

            
            # save the results for later metrics calculation
            best_arms_key_reward = dict(arm_reward.most_common()[0:len(self.selected_arms)])
            actual_earned = sum(step_reward.values())
            could_earned = sum(best_arms_key_reward.values())
            selected_arms = list(step_reward.keys())
            best_arms = list(best_arms_key_reward.keys())
            
            step_result_for_metrics = {"time_sec": sim_time_sec, 
                                       "actual_earned": actual_earned,
                                       "could_be_earned": could_earned,
                                       "selected_arms": selected_arms,
                                       "best_arms": best_arms}
            each_step_reward.append(step_result_for_metrics)
            
            
            
            yield step_result_for_agent
            
        self.simulation_report_df = pd.DataFrame(each_step_distr)
        self.rewards_report_df = pd.DataFrame(each_step_reward)
    
    def get_report_df(self):
        return self.simulation_report_df


if __name__ == "__main__":
    a = Arm(datetime.datetime.now(), datetime.datetime.now(), 3)
    print(type(a))
        
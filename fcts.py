import matplotlib.pyplot as plt
import numpy as np

def step_selector(old,init_val , step):
    if old <= init_val:
        return old
    elif old >= step:
        return old*2
    else:
        return old*5

generate_random_number = lambda lower_bound , higher_bound : lower_bound + (higher_bound-lower_bound)*np.random.random()

generate_random_int = lambda lower_bound , higher_bound : lower_bound + np.random.randint(higher_bound)

def go_2d_figure(x,y):
    plt.plot(x,y)
    plt.show()

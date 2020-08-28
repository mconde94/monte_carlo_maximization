import numpy as np
import sys
sys.path.append(['/home/manuel/Documents/codes/monte_carlo_problems'])
import fcts as fcts


bounds = {
    'x':{'min':0 ,'max':1 },
    'y':{'min':0 ,'max':2 },
    'z':{'min':2 ,'max':3 },
    'init_val' : 5,
    'final_val': 100000,
    'step' : 10000
}

function_to_assess = lambda x, y, z : (np.exp(x) + y)**2 + 3*((1-z)**2)

get_maximum = lambda dict_test : dict_test[max(dict_test.keys())]

get_maximum_value = lambda dict_test: max(dict_test.keys())



def single_iteration(bounds,function , generator):
    """

    :param bounds:
    :return:
    """
    generator_x , generator_y , generator_z = generator(bounds['x']['min'],bounds['x']['max']) , generator(bounds['y']['min'],bounds['y']['max']) ,generator(bounds['z']['min'],bounds['z']['max'])
    return {function(generator_x,generator_y,generator_z):{'x':generator_x,'y':generator_y,'z':generator_z}}


def resolution_test(N):

    results = {}

    for i in range (0,N):
        results.update(single_iteration(bounds , function_to_assess , fcts.generate_random_number))

    return get_maximum_value(results) , N , get_maximum(results)

def evaluation_resolution():
    Zs , Ns , Vectors , N = [], [],[],bounds['init_val']
    while N <= bounds['final_val']:
        N = fcts.step_selector(N,bounds['init_val'],bounds['step'])
        z , n , vs = resolution_test(N)
        Ns.append(n)
        Zs.append(z)
        Vectors.append(vs)
        N = N + 1
    print(z)
    print(vs)
    fcts.go_2d_figure(Ns, Zs)


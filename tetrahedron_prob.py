import numpy as np
import sys
sys.path.append(['/home/manuel/Documents/codes/monte_carlo_problems'])
import fcts as fcts

args = {
    'radius':0.5,
    'center':np.array([0,0,0]),
    'iterations': 100,
    'init_val' : 10,
    'step':6000,
    'final_val':3000,
}

def random_vector_generator(radius):
    theta = np.random.random()*2*np.pi
    phi = np.random.random()*np.pi
    return np.array([radius*np.cos(theta)*np.sin(phi) , radius*np.sin(theta)*np.sin(phi) , radius*np.cos(phi)])

radius = lambda x: np.sqrt(x[0]**2+x[1]**2+x[2]**2)

def build_main_matrix(p1,p2,p3,p4):
    p1 ,p2 , p3 , p4 = np.append(p1, 1) , np.append(p2, 1) , np.append(p3, 1) , np.append(p4, 1)
    return np.array([p1, p2, p3, p4])

def get_matrix(d0 , p0 , n):
    d_out = d0.copy()
    p0 = np.append(p0,1)
    d_out[n] = p0
    return d_out

def get_sign(value):
    if value > 0:
        return 'positive'
    elif value == 0:
        return 'zero'
    else:
        return 'negative'


def one_iteration():
    p1 ,p2 , p3 , p4 = random_vector_generator(args['radius']) , random_vector_generator(args['radius']), random_vector_generator(args['radius']),random_vector_generator(args['radius'])

    matrixes = {0:build_main_matrix(p1, p2, p3, p4)}

    for i in range(1,5):
        matrixes[i] = get_matrix(matrixes[0],args['center'] , i-1)

    flags = []

    for i in matrixes.keys():
        flags.append(get_sign(np.linalg.det(matrixes[i])))

    if len(list(set(flags))) != 1:
        return 0
    else:
        return 1


def iterations(N):
    out = []
    for i in range(1,N):
        out.append(one_iteration())
    return sum(out)/N

def resolution_evaluation(args):
    Ps , Ns , Vectors , N = [], [],[],args['init_val']
    while N <= args['final_val']:
        N = fcts.step_selector(N,args['init_val'],args['step'])
        P = iterations(N)
        Ns.append(N)
        Ps.append(P)
        N = N + 1
    fcts.go_2d_figure(Ns, Ps)

resolution_evaluation(args)
import numpy as np
import sys
sys.path.append(['/home/manuel/Documents/codes/monte_carlo_problems'])
import fcts as fcts
import math

args = {
    'size':1,
    'N_iter' : 10000
}

def get_point_from_cube(size):
    rand1 = fcts.generate_random_number(0,1)
    face = math.floor(rand1*6+1)
    rand1 = rand1*size
    rand2 = fcts.generate_random_number(0,size)
    if face == 1:
        x , y , z = 0 , rand1 , rand2
    elif face == 2:
        x ,y ,z = size , rand1 ,rand2
    elif face == 3:
        x , y, z = rand1 , 0 , rand2
    elif face == 4:
        x , y ,z = rand1 , size , rand2
    elif face == 5:
        x ,y , z = rand1, rand2 , 0
    else:
        x , y, z = rand1, rand2, size
    return np.array([x , y ,z])

def one_iteration(size):
    p1 , p2 = get_point_from_cube(size) , get_point_from_cube(size)
    return np.linalg.norm(p2 - p1)

def multiple_iterations(size , N):
    distances = []
    for i in range(0,N):
        distances.append(one_iteration(size))
    return np.mean(distances)

def main():
    avg_distance = multiple_iterations(args['size'],args['N_iter'])
    print('the average distance on a cube is:')
    print(avg_distance)

if __name__ == "__main__":
    main()

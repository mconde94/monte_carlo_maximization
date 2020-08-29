import numpy as np
import sys
sys.path.append(['/home/manuel/Documents/codes/monte_carlo_problems'])
import fcts as fcts

args = {
    'radius':1,
    'center':np.array([0,0]),
    'N_iter' : 4000
}

def random_vector_generator(radius):
    theta = fcts.generate_random_number(0,2*np.pi)
    return np.array([radius*np.cos(theta), radius*np.sin(theta)])

get_angle_from_vector = lambda v1 , v2 : np.arccos(np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))

def is_triangle_acute(radius):
    p1 , p2 , p3 = random_vector_generator(radius) , random_vector_generator(radius) ,random_vector_generator(radius)
    p12 ,p13 ,p23 = p2 - p1 ,p3 - p1 ,p3 - p2
    theta1 ,theta2 , theta3 = get_angle_from_vector(p12 , p13) , get_angle_from_vector(-p12, p23) , get_angle_from_vector(-p23,-p13)
    angles = np.array([theta1,theta2,theta3])
    if True in (angles >= np.pi/2):
        return 0
    else:
        return 1

def main():
    outcome = 0
    for i in range(0,args['N_iter']):
        outcome = outcome + is_triangle_acute(args['radius'])
    result = outcome / args['N_iter']
    args['prob'] = result
    print('probability is: ' + str(result))

if __name__ == "__main__":
    main()


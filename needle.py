import numpy as np
import sys
sys.path.append(['/home/manuel/Documents/codes/monte_carlo_problems'])
import fcts as fcts

args = {
    'needle_size' : 1,
    'line_spacing' : 1,
    'width' : 17 ,
    'start':0,
    'length' : 30,
    'finish': 27,
    'Niter' : 100
}


def needle_generator(width , length, needle_size):
    p1 = np.array([fcts.generate_random_number(0,width),fcts.generate_random_number(0,length)])
    theta = fcts.generate_random_number(0,2*np.pi)
    p2 = p1 + needle_size*np.array([np.cos(theta), np.sin(theta)])
    return np.array([p1 , p2])

out = needle_generator(args['width'] , args['length'], args['needle_size'])
print(out)

def lines_multiples(line_spacing, length, start = 0 , finish = 0):
    if finish== 0:
        finish = length
    line = start
    multiples = []
    while line <= finish:
        multiples.append(line)
        line = line + line_spacing
    print(multiples)
    return multiples

def one_assessment(points, line):
    assess = np.sort(points[:, 1])
    if line >= assess[0] and line <= assess[1]:
        return True
    else:
        return False

def iteration(N,width, length , needle_size,line_spacing, start, finish):
    Needles = []
    for i in range(0,N):
        Needles.append(needle_generator(width, length , needle_size))
    Lines = lines_multiples(line_spacing, length, start = start , finish = finish )
    count = 0
    for needle in Needles:
        for line in Lines:
            if one_assessment(needle,line):
                count = count +1
                break
    return 1 - count / N

final = iteration(args['Niter'],args['width'], args['length'], args['needle_size'],args['line_spacing'],args['start'],args['finish'])

print(final)
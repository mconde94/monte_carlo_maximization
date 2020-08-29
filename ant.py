import numpy as np
import sys
sys.path.append(['/home/manuel/Documents/codes/monte_carlo_problems'])
import fcts as fcts

args = {
    'starting_point': np.array([0,0]),
    'final_point': np.array([6,6]),
    'N_of_ants' :  1000
}

class Ant:
    def __init__(self, starting_point,final_point):
        self.visited_nodes = [starting_point]
        self.success = False
        self.position = starting_point
        self.starting_point = starting_point
        self.final_point = final_point
        self.in_game = True

    def update_position(self, new_step):
        self.position = new_step
        self.visited_nodes.append(new_step)

    def get_neighbours(self):
        p1 = np.array([self.position[0] - 1 , self.position[1]])
        p2 = np.array([self.position[0] + 1 , self.position[1]])
        p3 = np.array([self.position[0] , self.position[1] -1 ])
        p4 = np.array([self.position[0] , self.position[1] + 1])
        return [p1 , p2 , p3 , p4]

    def is_step_inside_mesh(self, step):
        if self.starting_point[0] <= step[0] <= self.final_point[0] and self.starting_point[0] <= step[1] <= self.final_point[1]:
            return True
        else:
            return False

    def get_possible_steps(self):
        possible_steps = self.get_neighbours()
        indexes_to_remove = []
        for i, step in enumerate(possible_steps, start=0):
            if not self.is_step_inside_mesh(step):
                indexes_to_remove.append(i)
            for old_step in self.visited_nodes:
                if np.array_equal(old_step,step):
                    indexes_to_remove.append(i)
        indexes_to_remove = list(set(indexes_to_remove))
        possible_steps = [i for j, i in enumerate(possible_steps) if j not in indexes_to_remove]
        return possible_steps

    def do_a_step(self):
        possible_nodes = self.get_possible_steps()
        if possible_nodes==[]:
            self.in_game = False
            self.success = False
        elif len(possible_nodes) == 1:
            self.update_position(possible_nodes[0])
        else:
            self.update_position(possible_nodes[fcts.generate_random_int(0,len(possible_nodes))])
        if np.array_equal(self.position, self.final_point):
            self.success = True

    def random_walk(self):
        while (not self.success) and self.in_game:
            self.do_a_step()
        if self.success:
            return 1
        else:
            return 0

def main():
    outcomes = {}
    results = []
    for i in range(0,args['N_of_ants']):
        print('ant number: ' + str(i))
        obj = Ant(args['starting_point'],args['final_point'])
        flag = obj.random_walk()
        results.append(flag)
        outcomes[i] = {
            'outcome': flag,
            'lenght' : len(obj.visited_nodes)
        }
    result = sum(results) / args['N_of_ants']
    print('probability:' + str(result))
    args['probability'] = result
    args['more_stats'] = outcomes

if __name__ == "__main__":
    main()
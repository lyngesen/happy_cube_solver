# from brick_data import all_bricks, brick_colors
import polycubes
import classes 
import solver
import pyomo_implementation 

from brick_data import get_bricks, mirko_bricks
from classes import FigureSpace, Edge, setup_FigureSpace, Brick
from solver import cube_solve
# from polycubes import generate_cube_coords, get_coords, get_coords_cubegrid

# public library imports
from multiprocessing import Pool, Process
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
from pyomo_implementation import solve_happy_problem
from alive_progress import alive_bar
import sys
import os
import numpy as np

import timing
import itertools
from collections import Counter
from simple_term_menu import TerminalMenu




timing.time_object(polycubes)
# timing.time_object(classes)
timing.time_object(solver)
timing.time_object(pyomo_implementation, prefix = 'pyo')


def count_cube_faces(cube):
    cube_cords = np.argwhere(cube == 1)

    adjecent_cubes = 0
    for c1, c2 in itertools.combinations(cube_cords,r=2):
        # print(f"{c1,c2=}, {np.linalg.norm(c1-c2) <= 1}")
        if np.linalg.norm(c1-c2) <= 1:
            adjecent_cubes +=1

    total_faces = cube_cords.shape[0]*6 - adjecent_cubes*2

    # print(f"{total_faces=}")
    return total_faces

def get_valid_k(n,max_cube_size, all_cubes):

    # all_cubes = list(polycubes.generate_polycubes(n))
    # cube_lengths_instances = sorted([cube_length for k, cube_length in enumerate(cube_lengths) if cube_length <= max_cube_size], key= lambda x : cube_lengths[x])
    cube_lengths = [count_cube_faces(cube) for cube in all_cubes]
    cube_lengths_instances = sorted([k for k, cube_length in enumerate(cube_lengths) if cube_length <= max_cube_size], key= lambda x : cube_lengths[x])
    return cube_lengths_instances



def single_run(args):
    ''' function called by each multiprocessing worker '''
    B,n,k,cube_cords = args
    # SKIP if already solved

    F = classes.setup_FigureSpace(0,0, cube_cords, max_faces = len(B))
    F.n = n
    F.k = k
    

    # only solve if there are enough bricks to fill out the figure
    F = pyomo_implementation.solve_happy_problem(F,B)
    return k, F

def main():

    all_bricks, brick_colors = get_bricks()
    B = all_bricks['yellow'] + all_bricks['blue'] + all_bricks['orange'] + all_bricks['red'] + all_bricks['purple'] + all_bricks['green']
    # B = all_bricks['yellow'] + all_bricks['blue'] + all_bricks['orange']




    workers = 4

    print(f"Available bricks: {len(B)}")
    print(f"Available workers/processes: {workers}")
    for n in range(8,9):
        cubes_coords_list = polycubes.generate_cube_coords(n)
        all_cubes = list(polycubes.generate_polycubes(n))
        print(f"possible polycubes of size n={n} is k={len(cubes_coords_list)}")
        # for k, cube_cords in enumerate(cubes_coords_list):
        valid_instances = get_valid_k(n,len(B), all_cubes)
        assert len(valid_instances) >0
        instances = ((B,n,k,cube_cords) for k,cube_cords in enumerate(cubes_coords_list) if k in valid_instances)
        # instances = ((B,n,k,cube_cords) for k,cube_cords in enumerate(cubes_coords_list) )
        print(f"Total valid_instances {len(valid_instances)} out of {len(all_cubes)} polycubes")
        n_feasible = False
        K = len(valid_instances)
        with alive_bar(K, enrich_print=True, manual=False) as bar, Pool(processes=workers) as pool:
            results = pool.imap_unordered(single_run, instances)

            for k, F in results:
                if F: # false if infeasible
                    n_feasible = True
                    F.plot(show=False)
                    plt.savefig(fname = './figures/main_solutions/' + f"main_solution_{F.n}_{F.k}.png")
                    plt.close()
                    # bar(1)
                    if n > 10:
                        break

                # bar(k/K)
                bar()
                # bar.title(f'Just finished {n=}, k={k}')
            else: # finally
                print(f"none of the K={K} possible polycubes of size n={n} was feasible")
                continue
            print(f"n={n} feasible: {n_feasible=}, with k={k}")

def show_single():
    n = int(input('(polycube size) n: '))
    K =  len(list(polycubes.generate_polycubes(n)))
    k = int(input(f'(polycube id of {range(K-1)} possibilities) k: '))
    
    all_bricks, brick_colors = get_bricks()
    brick_colors['Mirko'] = mirko_bricks()
    all_bricks['Mirko'] = mirko_bricks()
    terminal_menu = TerminalMenu(
        brick_colors,
        multi_select=True,
        show_multi_select_hint=True,
    )
    menu_entry_indices = terminal_menu.show()
    
    B = []
    for color in menu_entry_indices:
        B += all_bricks[list(brick_colors)[color]]

    F = classes.setup_FigureSpace(n,k, max_faces = len(B))
    F = pyomo_implementation.solve_happy_problem(F,B)
    if not F:
        print(f" Polycube instance infeasible ")
    else:
        F.plot()
        plt.show()



if __name__ == '__main__':
    if 'show' in sys.argv:
        show_single()
    else:
        main()


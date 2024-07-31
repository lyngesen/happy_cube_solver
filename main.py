# from brick_data import all_bricks, brick_colors
from brick_data import get_bricks
from classes import FigureSpace, Edge, setup_FigureSpace, Brick
from solver import cube_solve
from polycubes import generate_cube_coords, get_coords, get_coords_cubegrid

# public library imports
from multiprocessing import Pool, Process
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
from pyomo_implementation import solve_happy_problem
from alive_progress import alive_bar
import sys
import os


def single_run(args):
    ''' function called by each multiprocessing worker '''
    B,n,k,cube_cords = args
    # SKIP if already solved

    F = setup_FigureSpace(0,0, cube_cords, max_faces = len(B))
    F.n = n
    F.k = k
    

    # only solve if there are enough bricks to fill out the figure
    F = solve_happy_problem(F,B)
    return k, F

def main():

    all_bricks, brick_colors = get_bricks()
    B = all_bricks['yellow'] + all_bricks['blue'] + all_bricks['orange'] + all_bricks['red'] + all_bricks['purple'] + all_bricks['green']
    # B = all_bricks['yellow'] + all_bricks['blue'] + all_bricks['orange']
    workers = 4

    print(f"Available bricks: {len(B)}")
    print(f"Available workers/processes: {workers}")
    for n in range(6,10):
        cubes_coords_list = generate_cube_coords(n)
        print(f"possible polycubes of size n={n} is k={len(cubes_coords_list)}")
        # for k, cube_cords in enumerate(cubes_coords_list):
        instances = ((B,n,k,cube_cords) for k,cube_cords in enumerate(cubes_coords_list))
        n_feasible = False
        K = len(cubes_coords_list)
        with alive_bar(K, enrich_print=True, manual=False) as bar, Pool(processes=workers) as pool:
            results = pool.imap_unordered(single_run, instances)

            for k, F in results:
                if F: # false if infeasible
                    n_feasible = True
                    F.plot(show=False)
                    plt.savefig(fname = './figures/main_solutions/' + f"main_solution_{F.n}_{F.k}.png")
                    plt.close()
                    # bar(1)
                    break

                # bar(k/K)
                bar()
                # bar.title(f'Just finished {n=}, k={k}')
            else: # finally
                print(f"none of the K={K} possible polycubes of size n={n} was feasible")
                continue
            print(f"n={n} feasible: {n_feasible=}, with k={k}")


if __name__ == '__main__':
    main()
    #F = FigureSpace()
    #cube_solve(F, all_bricks['blue'])

    if False:
        F = setup_FigureSpace(1,0)
        B = all_bricks['blue'] 
        B = all_bricks['blue'] + all_bricks['red'] + all_bricks['yellow']
        B = all_bricks['yellow'] + all_bricks['blue'] + all_bricks['orange'] + all_bricks['red'] + all_bricks['purple'] + all_bricks['green']

        F.plot()

        match input('Solve F?  y/Yes: '):
            case 'y':
                solve_happy_problem(F,B)
            case _:
                pass
        

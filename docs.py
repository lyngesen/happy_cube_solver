'''
File used for stuff presented in readme.md
'''

from copy import deepcopy
from brick_data import get_bricks
from classes import FigureSpace, Edge, setup_FigureSpace
import matplotlib.pyplot as plt
from pyomo_implementation import solve_happy_problem
from solver import cube_solve
import math
import os
import imageio.v3 as iio

FIGURES_LOCATION = './figures/'
SAVE_PLOTS = True 
SIZE_STANDARD_FIGURE = (3,3)
gif_dir = './figures/solver_gif/' # show recursive soler
all_bricks, brick_colors = get_bricks()

def plot_or_save(fig, fname: str):
    """ call to plot or save fig """
    if SAVE_PLOTS:
        print(f"{FIGURES_LOCATION=}")
        # fig.savefig(fname = FIGURES_LOCATION + f"{fname}.pgf")
        # fig.savefig(fname = FIGURES_LOCATION + f"{fname}.pdf")
        fig.savefig(fname = FIGURES_LOCATION + f"{fname}.png")
    else:
        plt.title(fname)
        plt.show()


## solver function

def get_gif_id():
    files = os.listdir('./figures/solver_gif/')
    return max([int(file.split('.png')[0].split('_')[-1]) for file in files]) + 1


def cube_solve_plot(F, bricklist, placelist = [None]*6):
    #print(p.name for p in placelist)
    #print([p!= None for p in placelist])
    # Base case, place full and not failed edges
    # if len(bricklist)==0 and F.check_all():
    # print("  "* len(bricklist) + "b")
    if placelist[-1] and F.check_all():
        if F.check_complete() or True:
            print(f"{F.check_complete()=}")
            print('Happy cube solved')
            print(F)
            print(f"{F.check_complete()=}")
            # F.plot()
            # for f in F.faces:
            F.plot(show = False)
            gif_id = get_gif_id()
            plt.savefig(fname = './figures/solver_gif/' + f"gif_plot_{gif_id}.png")
            return True
    if placelist[-1]: return
    current_faceid = placelist.index(None)
    for i, b in enumerate(bricklist):
        for r, b_or in enumerate(b.or_list):
            b_or.name = f'b{i}, r{r}'
            b_or.color = b.color
            # print(b_or.name)
            Fm = deepcopy(F)
            Fm.faces[current_faceid].set_face(b_or)
            #print(Fm)
            # F.plot(show=False)

            # Check if Fm valid
            #print(Fm.check_all())
            if Fm.check_all():

                F.plot(show = False)
                gif_id = get_gif_id()
                plt.savefig(fname = './figures/solver_gif/' + f"gif_plot_{gif_id}.png")


                Bm = deepcopy(bricklist)
                Pm = deepcopy(placelist)
                Pm[current_faceid] = b_or
                #print(f'adding b{i} (or: {r}) to Pm')
                del Bm[i]
                #print([bm.name for bm in Bm])
                solved = cube_solve_plot(Fm, Bm, Pm)
                if solved:
                    return True


# BRICKS

def print_brick(brick):
    chr_dict =  {1:brick_colors[brick.color],0:"  "}
    print("\n".join(["".join([chr_dict[b] for b in row]) + "\t"*3 + str(row) for row in brick.cubegrid])) #return "\n".join(["".join([row]) for row in self.cubegrid]))



if False:
    F = setup_FigureSpace(1,0)

    del F.faces[2:-1]
    del F.faces[0]
    del F.faces[-1]

    f = F.faces[0]
    f.set_face(b)
    
    F.plot()






def dir_to_gif(gif_name: str,  gif_dir: str, string_filter: callable = lambda _ : True):
    images = []
    repeat_last_image = 2
    # for filename in sorted(os.listdir(gif_dir), lambda x : int(x.split('.json')[0].split('_')[-1])):
    for filename in sorted(os.listdir(gif_dir), key =lambda x: int(x.split('.png')[0].split('_')[-1])):
        print(f"{filename=}")
        images.append(iio.imread(gif_dir + filename))

    fps = 5
    duration = 3  # seconds
    last_image = images[-1]
    # Append the last image (fps * duration) times
    for _ in range(math.ceil(fps*duration)):
        images.append(last_image)
    
    # iio.im()
    iio.imwrite('./figures/' + gif_name, images, fps = fps, loop = 0)  # fps = 3

if False:
    
    dir_to_gif('recursive_solver2.gif', gif_dir)

def recursive_gif(F: FigureSpace, B, gif_name: str):
    for file in os.listdir(gif_dir):
        os.remove(gif_dir + file)
        print(f"removing: {gif_dir + file}")


    placelist = [None] * len(F.faces)
    assert len(placelist) <= len(B)
    ######################## Figure gif_plot START ########################
    gif_id = 0
    fig_name = f"gif_plot_{gif_id}"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    F.plot(show=False)
    # save or plot figure
    plt.savefig(fname = gif_dir + f"gif_plot_{gif_id}.png")
    # now save each recursively
    cube_solve_plot(F, B, placelist = placelist)
    dir_to_gif(gif_name, gif_dir)
    for file in os.listdir(gif_dir):
        os.remove(gif_dir + file)
        print(f"removing: {gif_dir + file}")


# all monocube recursive gifs:
def recursive_monocubes():
    for c_id, color in enumerate(list(brick_colors.keys())):
        if color == 'red': continue 
        B = all_bricks[color] 
        F = setup_FigureSpace(1,0)
        recursive_gif(F, B, gif_name = f'monocube_{c_id}.gif')

# also one large example
# if False:
def large_example():
    for (n,k) in [(2,0)]:
        B = all_bricks['blue'] + all_bricks['yellow'] + all_bricks['purple'] + all_bricks['green']
        F = setup_FigureSpace(n,k)
        gif_name = f'large_{n}_{k}.gif'
        recursive_gif(F, B, gif_name = gif_name)
    
        # dir_to_gif(gif_name, gif_dir)
def example_figure_space(examples = [(1,0), (2,0), (4,7)]):
    for (n,k) in examples:
        ######################## Figure faces START ########################
        fig_name = f"faces_{n}_{k}"
        print(f"Plotting figure: {fig_name}")
        # define new figure
        # fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')


        F = setup_FigureSpace(n,k)
        F.plot(show=False)

        # save or plot figure
        plot_or_save(plt, fig_name)
        ######################### Figure faces END #########################

def orientation(b):
    for r, br in enumerate(b.or_list):
        ######################## Figure orientation_{r} START ########################
        fig_name = f"orientation_{r}"
        print(f"Plotting figure: {fig_name}")
        # define new figure

        F = setup_FigureSpace(1,0)

        del F.faces[2:-1]
        del F.faces[0]
        del F.faces[-1]




        # F = setup_FigureSpace(2,0)
        br.color = b.color
        F.faces[0].set_face(br)
        F.plot(show=False)
        # save or plot figure
        plot_or_save(plt, fig_name)
        ######################### Figure orientation_{r} END #########################


def monocube_solved():
    for c_id, color in enumerate(list(brick_colors.keys())):
        ######################## Figure monocube_{c_id} START ########################
        fig_name = f"monocube_{c_id}"
        print(f"{color=}")
        if color=='red': continue
        # TODO: fix all the red bricks data <30-07-24> #

        print(f"Plotting figure: {fig_name}")
        # define new figure
        B = all_bricks[color]
        F = setup_FigureSpace(1,0)
        F = solve_happy_problem(F,B)
        F.plot(show=False)
        # save or plot figure
        plot_or_save(plt, fig_name)
        ######################### Figure monocube_{c_id} END #########################


def main():
    b = all_bricks['blue'][3]
    b.color = 'blue'

    if True:
        print_brick(b)
        print()

    b = all_bricks['yellow'][3]
    b.color = 'yellow'
    if False:
        print_brick(b)


    recursive_monocubes()
    orientation(b)
    monocube_solved()
    example_figure_space()

    pass


if __name__ == "__main__":
    main()

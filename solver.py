from copy import deepcopy
## recursive solver function

solutions = []
def cube_solve(F, bricklist, placelist = [None]*6):
    #print(p.name for p in placelist)
    #print([p!= None for p in placelist])
    # Base case, place full and not failed edges
    # if len(bricklist)==0 and F.check_all():
    if placelist[-1] and F.check_all():
        if F.check_complete() or True:
            print(f"{F.check_complete()=}")
            print('Happy cube solved')
            print(F)
            print(f"{F.check_complete()=}")
            return F
    if placelist[-1]: return
    current_faceid = placelist.index(None)
    for i, b in enumerate(bricklist):
        for r, b_or in enumerate(b.or_list):
            b_or.name = f'b{i}, r{r}'
            b_or.color = b.color
            print(b_or.name)
            Fm = deepcopy(F)
            Fm.faces[current_faceid].set_face(b_or)
            # Check if Fm valid
            #print(Fm.check_all())
            if Fm.check_all():
                Bm = deepcopy(bricklist)
                Pm = deepcopy(placelist)
                Pm[current_faceid] = b_or
                #print(f'adding b{i} (or: {r}) to Pm')
                del Bm[i]
                #print([bm.name for bm in Bm])
                solved = cube_solve(Fm, Bm, Pm)
                if solved:
                    return True

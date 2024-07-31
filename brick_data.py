'''
Simply which contains the Bricks

There might be an error in the red brick
'''

from classes import Brick

def str_to_brick(s):
    ''' read a brick from the easily writable format '''
    rows = s.split('\n')
    del rows[rows.index("")]
    del rows[rows.index("")]

    chr_to_bol = {'x':1,'o':0}
    cubegrid = [[chr_to_bol[row_chr] for row_chr in reversed(row)] for row in rows]
    return Brick(cubegrid)

# Define your hex color
def hex_to_rgb(hex_color):
    '''Convert hex color to RGB'''
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return r, g, b

def generate_shades(hex_color, num_shades=6):
    ''' if shades are not added each brick of a specific color will be indistinguishable from each other when plottet. '''
    r, g, b = hex_to_rgb(hex_color)
    step = 255 // (num_shades - 1)
    shades = []
    for i in range(num_shades):
        new_r = max(0, r - i * (step // 2))  # Adjusted step size
        new_g = max(0, g - i * (step // 2))
        new_b = max(0, b - i * (step // 2))
        shade_hex = "#{:02x}{:02x}{:02x}".format(new_r, new_g, new_b)
        shades.append(shade_hex)
    return shades


def get_bricks(colors = 'all'):

    # brick data
    b1 = Brick(
            [[1,0,1,1,0],
             [1,1,1,1,1],
             [0,1,1,1,0],
             [1,1,1,1,1],
             [1,1,0,0,1]])
    b2 = Brick(
            [[0,1,0,1,1],
             [0,1,1,1,0],
             [1,1,1,1,1],
             [0,1,1,1,0],
             [0,0,0,1,1]])
    b3 = Brick(
            [[0,1,0,0,0],
             [1,1,1,1,0],
             [0,1,1,1,1],
             [1,1,1,1,0],
             [0,1,0,1,0]])

    b4 = Brick(
            [[0,0,1,1,0],
             [0,1,1,1,0],
             [1,1,1,1,1], # evt fejl
             [0,1,1,1,0],
             [1,1,0,1,1]])

    b5 = Brick(
            [[0,1,0,0,0],
             [1,1,1,1,1],
             [0,1,1,1,0],
             [1,1,1,1,1],
             [0,0,1,0,1]])

    b6 = Brick(
            [[0,0,1,0,0],
             [0,1,1,1,1],
             [1,1,1,1,0],
             [0,1,1,1,1],
             [0,0,1,0,0]])


    RedBricks = [b1,b2,b3,b4,b5,b6]

    BlueBricks = [
            [
                [0,0,1,0,0],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [0,0,1,0,0],
            ],[
                [1,0,1,0,1],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [1,0,1,0,1],
            ],[
                [0,0,1,0,0],
                [0,1,1,1,1],
                [1,1,1,1,0],
                [0,1,1,1,1],
                [0,0,1,0,0],
            ],[
                [0,1,0,1,0],
                [1,1,1,1,0],
                [0,1,1,1,1],
                [1,1,1,1,0],
                [1,1,0,1,0],
            ],[
                [0,1,0,1,0],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [1,0,1,0,0],
            ],[
                [0,1,0,1,0],
                [0,1,1,1,1],
                [1,1,1,1,0],
                [0,1,1,1,1],
                [1,1,0,1,1],
            ]]

    BlueBricks = [Brick(b) for b in BlueBricks]


    OrangeBricks = [
"""
xoxox
xxxxx
oxxxo
xxxxx
ooxoo
"""
,
"""
ooxxo
oxxxx
xxxxo
oxxxx
xxoxo
"""
,
"""
oxoxo
oxxxx
xxxxo
oxxxo
ooxoo
"""
,
"""
oxoxo
xxxxo
oxxxo
xxxxx
xoxox
"""
,
"""
ooxoo
xxxxx
xxxxx
oxxxo
ooxoo
"""
,
"""
xxoxx
oxxxo
oxxxx
xxxxo
oxoxx
"""]
    OrangeBricks = [str_to_brick(s) for s in OrangeBricks]


    GreenBricks = [
"""
oxoxx
xxxxo
oxxxx
xxxxo
xxoxx
"""
,
"""
ooxoo
xxxxx
oxxxo
xxxxx
oxoxo
"""
,
"""
ooxoo
oxxxo
xxxxx
oxxxo
xxoxx
"""
,
"""
ooxoo
xxxxo
oxxxx
xxxxo
xxoxx
"""
,
"""
ooxoo
xxxxx
oxxxo
xxxxx
ooxoo
"""
,
"""
ooxoo
oxxxo
xxxxx
oxxxo
xxoxo
"""]
    GreenBricks = [str_to_brick(s) for s in GreenBricks]





    PurpleBricks = [
"""
oooxo
oxxxx
xxxxo
oxxxx
ooxoo
"""
,
"""
xxooo
oxxxx
xxxxx
oxxxo
oxoxo
"""
,
"""
oxoxx
oxxxx
oxxxx
xxxxo
ooxoo
"""
,
"""
xxoxo
oxxxo
xxxxo
oxxxx
oxoxx
"""
,
"""
xoxoo
xxxxo
xxxxx
oxxxx
oxxox
"""
,
"""
xxoxx
xxxxo
oxxxx
oxxxo
oxoxo
"""]
    PurpleBricks = [str_to_brick(s) for s in PurpleBricks]



    YellowBricks = [
"""
xoxoo
xxxxx
oxxxo
xxxxx
xoxox
"""
,
"""
xxoxo
oxxxx
xxxxo
oxxxx
ooxoo
"""
,
"""
oxoxx
oxxxo
xxxxx
oxxxo
oxoxo
"""
,
"""
oxoxo
xxxxo
oxxxx
xxxxo
ooxoo
"""
,
"""
oxoxo
xxxxo
oxxxo
xxxxx
ooxox
"""
,
"""
xoxoo
xxxxx
xxxxo
oxxxx
ooxox
"""]
    YellowBricks = [str_to_brick(s) for s in YellowBricks]


    #for b in PurpleBricks:
    #    print(b)
    #    print('')

    brick_colors = {'blue':'🟦','red':'🟥','orange':'🟧','green':'🟩','purple':'🟪','yellow':'🟨',}

    all_bricks = {'blue': BlueBricks,'red':RedBricks,'orange':OrangeBricks,'green':GreenBricks, 'purple':PurpleBricks,'yellow':YellowBricks}

    for color, brickset in all_bricks.items():
        if color == 'blue':
            hex_color = '#0000FF'
        elif color == 'red':
            hex_color = '#FF00FF'
        elif color == 'yellow':
            hex_color = '#EAFF06'
        elif color == 'purple':
            hex_color = "#B406FF"
        elif color == 'green':
            hex_color = '#63FF3B'
        elif color == 'orange':
            hex_color = '#FFB625'
        else:
            hex_color = '#303030'

        hex_shades = generate_shades(hex_color)
        for i, b in enumerate(brickset):
            b.color = hex_shades[i]
    
    return all_bricks, brick_colors


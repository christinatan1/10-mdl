import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        cmd = command['op']

        if cmd == "push":
            stack.append( [x[:] for x in stack[-1]] )

        elif cmd == "pop":
            stack.pop()

        elif cmd == "move":
            t = make_translate(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif cmd == "rotate":
            theta = float(command['args'][1]) * (math.pi / 180)
            if command['args'][0] == 'x':
                t = make_rotX(theta)
            elif command['args'][0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif cmd == "scale":
            t = make_scale(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif cmd == "box":
            add_box(tmp,
                    float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                    float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            matrix_mult( stack[-1], tmp )
            if command['constants']:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif cmd == "sphere":
            add_sphere(tmp,
                       float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                       float(command['args'][3]), step_3d)
            matrix_mult( stack[-1], tmp)
            if command['constants']:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif cmd == "torus":
            add_torus(tmp,
                      float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                      float(command['args'][3]), float(command['args'][4]), step_3d)
            matrix_mult( stack[-1], tmp )
            if command['constants']:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif cmd == "constants":
            pass

        elif cmd == "line":
            add_edge( tmp,
                      float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                      float(command['args'][3]), float(command['args'][4]), float(command['args'][5]) )
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []

        elif cmd == "save":
            save_extension(screen, command['args'][0]+ ".png")

        elif cmd == "display":
            display(screen)

        else:
            print(command)

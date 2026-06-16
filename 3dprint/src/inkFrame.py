import build123d as b
import ocp_vscode as o

height = 4 # or 5

eink_outer = (171, 111.7)
eink_inner = (165, 100)
eink_border = 2.5
eink_bottom = eink_outer[1] - eink_border - eink_inner[1]
eink_cable = 20
frame = (212, 152.2) # (213, 152.2)

backplate_height = 2
board = (80, 41.3, 1.5)
board_hole = 2.5
board_hole_border = 1.2
board_holes = (board[0] - 2*board_hole_border, board[1] - 2*board_hole_border)
board_connector = 16
board_connector_offset = 22 # 21

battery = (62, 40, 6.5)

########## mat

with b.BuildPart() as mat:
    b.Box(frame[0], frame[1], 2)
    
    # middle eink
    with b.Locations((0,0,-1/2)):
        # eink_inner hole
        b.Box(eink_inner[0], eink_inner[1], 1, mode=b.Mode.SUBTRACT)
    
        # eink holding frame
        eink_holding = (2, 2, 1)
        with b.Locations((0, eink_border/2 - eink_bottom/2, 1/2 + eink_holding[2]/2)):
            b.Box(eink_outer[0], eink_outer[1], eink_holding[2], mode=b.Mode.SUBTRACT)
            for i in (-1, 1):
                for j in (-1, 1):
                    with b.Locations((i*(eink_outer[0]/2-1), j*(eink_outer[1]/2-1))):
                        b.Cylinder(2, 1, mode=b.Mode.SUBTRACT)
            # cable
            with b.Locations((0, -eink_outer[1]/2 - 10/2, 0)):
                b.Box(eink_cable, 10, eink_holding[2], mode=b.Mode.SUBTRACT)

assert mat.part is not None
mat_right = mat.part.intersect( b.Box(frame[0]/2, frame[1], 10).translate((-frame[0]/4, 0, 0)) )
mat_left = mat.part.intersect( b.Box(frame[0]/2, frame[1], 10).translate((frame[0]/4, 0, 0)) )

b.export_step(mat_left, "src/res/inkFrame_mat_left.step")
b.export_step(mat_right, "src/res/inkFrame_mat_right.step")

b.export_stl(mat_left, "src/res/inkFrame_mat_left.stl")
b.export_stl(mat_right, "src/res/inkFrame_mat_right.stl")

o.show_object(mat_left)
o.show_object(mat_right)


####### backplate

with b.BuildPart() as backplate:
    b.Box(frame[0], frame[1], backplate_height)
    
    # middle eink
    with b.Locations((0, eink_border/2 - eink_bottom/2, 0)):
        # cable
        with b.Locations((0, -eink_inner[1]/2 - eink_bottom + 1 - 10/2, 0)):
            b.Box(eink_cable, 10, backplate_height, mode=b.Mode.SUBTRACT)
        # board
        with b.Locations((-board[0]/2 + board_connector_offset + board_connector/2, board[1]/2 -eink_inner[1]/2 - eink_bottom + 15, backplate_height/2 + 4/2)):
            for i in (-1, 1): 
                for j in (-1, 1):
                    with b.Locations((i*(board_holes[0]-board_hole)/2,j*(board_holes[1]-board_hole)/2,0)):
                        b.Cylinder(board_hole/2, 4)

assert backplate.part is not None
backplate_right = backplate.part.intersect( b.Box(frame[0]/2, frame[1], 10).translate((-frame[0]/4, 0, 0)) ).translate((0, 0, 5))
backplate_left = backplate.part.intersect( b.Box(frame[0]/2, frame[1], 10).translate((frame[0]/4, 0, 0)) ).translate((0, 0, 5))

b.export_step(backplate_left, "src/res/inkFrame_backplate_left.step")
b.export_step(backplate_right, "src/res/inkFrame_backplate_right.step")

b.export_stl(backplate_left, "src/res/inkFrame_backplate_left.stl")
b.export_stl(backplate_right, "src/res/inkFrame_backplate_right.stl")

o.show_object(backplate_left)
o.show_object(backplate_right)

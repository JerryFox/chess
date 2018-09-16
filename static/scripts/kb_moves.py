mvs = [['d4', 'f5'], ['e4', 'fxe4'], ['Nc3', 'Nf6'], ['Bg5', 'c6'],
       ['f3', 'e3'], ['Bxe3', 'd5'], ['Bd3', 'g6'], ['Qd2', 'Nbd7'],
       ['O-O-O', 'b5'], ['Bh6', 'Nb6'], ['Nge2', 'b4'], ['Nb1', 'a5'],
       ['b3', 'Qd6'], ['Bf4', 'Qe6'], ['Rde1', 'Qf7'], ['Ng3', 'Bg7'],
       ['Bh6', 'O-O'], ['Bxg7', 'Qxg7'], ['h4', 'c5'], ['dxc5', 'Nbd7'],
       ['Qe3', 'e5'], ['c6', 'a4'], ['cxd7', 'Nxd7'], ['h5', 'axb3'],
       ['axb3', 'Ra2'], ['hxg6', 'e4'], ['fxe4', 'Ba6'], ['exd5', 'Nc5'],
       ['gxh7+', 'Kh8'], ['Bg6', 'Qb2+'], ['Kd1', 'Ra1'], ['Qxc5', 'Rxb1+'],
       ['Kd2', 'Rf2+'], ['Re2', 'Rxh1'], ['Qxb4', '0-1']]

results = ['0-1', '1/2-1/2', '1-0', '*']

def kb_move_analyze(kb_move='Nbd7', color="b"):
    mv = kb_move
    check = False
    shortcut = None
    source = None
    col = None
    row = None
    capture = False
    if mv[-1] == "+":
        check = True
        mv = mv[:-1]
    if mv in ["O-O", "O-O-O"]:
        shortcut = "k"
        row = "1" if color == "w" else "8"
        col = "e"
        dest_row = row
        dest_col = "g" if mv == "O-O" else "c"
        dest = dest_col + dest_row
    else:
        dest = mv[-2:]
        rest = mv[:-2]
        if not rest:
            # simple pawn's move
            shortcut = "p"
        else:
            if rest[-1] == "x":
                # capture
                capture = True
                rest = rest[:-1]
            coordinate = None
            if rest[0] in "BQRNK":
                shortcut = rest[0]
                if len(rest) > 1:
                    coordinate = rest[-1]
            else:
                shortcut = "p"
                coordinate = rest[0]
            if coordinate:
                if coordinate in "abcdefgh":
                    col = coordinate
                else:
                    row = coordinate
    if shortcut:
        shortcut = shortcut.upper() if color == "w" else shortcut.lower()
    print(shortcut, dest, row, col, " - ", capture, check)

for pair in mvs:
    for index, move in enumerate(pair): 
        color = "b" if index % 2 else "w"
        print(move, " ", end="")
        kb_move_analyze(move, color)
    

import requests
search_list=["BFS","DFS","UCS","GS","A*","A*2"]
search="BFS"
target_url="https://www.cmpe.boun.edu.tr/~emre/courses/cmpe480/hw1/input.txt"
txt = requests.get(target_url).text

"""class node:
    def __init__(self, parent, cost, numberOfPins, children, board):
        self.parent = parent
        self.cost = cost
        self.numberOfPins = numberOfPins
        self.children = children
        self.board = board"""

def updateBoard(board, move, pinLoc): #returns the updated version of the board after a given move
    [pin, direction, jump] = move.split()
    r = pinLoc[0]
    c = pinLoc[1]
    board[r][c] = '.'
    if direction == "up":
        board[r - jump][c] = pin
        r = r - 1
        for _ in range(jump - 1):
            board[r][c] = '.'
            r = r - 1
    elif direction == "down":
        board[r + jump][c] = pin
        r = r + 1
        for _ in range(jump - 1):
            board[r][c] = '.'
            r = r + 1
    elif direction == "left":
        board[r][c] = pin
        c = c - 1
        for _ in range(jump - 1):
            board[r][c] = '.'
            c = c - 1
    elif direction == "right":
        board[r][c] = pin
        c = c + 1
        for _ in range(jump - 1):
            board[r][c] = '.'
            c = c + 1

    return board


def getPinsAndLocations(board): #returns pins on the board and their locations

    res = {}
    rows = len(board)
    columns = len(board[0])

    for i in range(rows):
        for j in range(columns):
            if board[i][j] != '.':
                res[board[i][j]] = [i,j]

    return res

def canGo(board, pin, locs, direction): #returns the number of jumps a pin can make to a certain direction. if it cant, returns -1
    if direction == "up":
        r = locs[pin][0]
        c = locs[pin][1]
        jump = 0
        while True:
            r = r - 1
            if r < 0:
                break
            elif board[r][c] != '.':
                jump = jump + 1
            else:
                break

        if jump > 0:
            return jump + 1
        else:
            return -1

    elif direction == "down":
        r = locs[pin][0]
        c = locs[pin][1]
        totalRows = len(board)
        jump = 0
        while True:
            r = r + 1
            if r >= totalRows:
                break
            elif board[r][c] != '.':
                jump = jump + 1
            else:
                break

        if jump > 0:
            return jump + 1
        else:
            return -1

    elif direction == "left":
        r = locs[pin][0]
        c = locs[pin][1]

        jump = 0
        while True:
            c = c - 1
            if c < 0:
                break
            elif board[r][c] != '.':
                jump = jump + 1
            else:
                break

        if jump > 0:
            return jump + 1
        else:
            return -1


    elif direction == "right":
        r = locs[pin][0]
        c = locs[pin][1]

        totalColumns = len(board[0])
        jump = 0
        while True:
            c = c + 1
            if c >= totalColumns:
                break
            elif board[r][c] != '.':
                jump = jump + 1
            else:
                break

        if jump > 0:
            return jump + 1
        else:
            return -1


def findAllMoves(board): #returns all possible moves in a board
    rows = len(board)
    columns = len(board[0])

    moves = []

    locs = getPinsAndLocations(board)

    for pin in locs:
        up = canGo(board, pin, locs, "up")
        down = canGo(board, pin, locs, "down")
        left = canGo(board, pin, locs, "left")
        right = canGo(board, pin, locs, "right")
        if up != -1:
            moves.append(pin + " up " + str(up))
        if down != -1:
            moves.append(pin + " down " + str(down))
        if left != -1:
            moves.append(pin + " left " + str(left))
        if right != -1:
            moves.append(pin + " right " + str(right))

    return moves

    return 0


board = []
for line in txt.splitlines():

    l = []
    line = line.strip()
    s = len(line)
    for j in range(s):
        l.append(line[j])
    board.append(l)

print(txt)

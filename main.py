import requests
from copy import copy, deepcopy
import collections
search_list=["BFS","DFS","UCS","GS","A*","A*2"]
search="BFS"
target_url="https://www.cmpe.boun.edu.tr/~emre/courses/cmpe480/hw1/input.txt"
txt = requests.get(target_url).text


#nodes = []
#nodes.append((cost, node))
#nodes.sort() --> priority yapmak için

class Node2:
    def __init__(self, parent, cost, numberOfPins, board, cumulativeCost, path):
        self.parent = parent
        self.cost = cost
        self.numberOfPins = numberOfPins
        #self.children = children
        self.board = board
        self.cumulativeCost = cumulativeCost
        self.path = path
        self.h1 = h1(board)

class Node:
    def __init__(self, parent, cost, numberOfPins, board, cumulativeCost, path):
        self.parent = parent
        self.cost = cost
        self.numberOfPins = numberOfPins
        #self.children = children
        self.board = board
        self.cumulativeCost = cumulativeCost
        self.path = path

def h1(board):

    r = len(board)
    c = len(board[0])
    columns = 0
    rows = 0

    for i in range(r):
        for j in range(c):
            if board[i][j] != '.':
                rows = rows + 1
                break

    for i in range(c):
        for j in range(r):
            if board[j][i] != '.':
                columns = columns + 1
                break

    return min(rows, columns)

def printBoard(board):
    for row in board:
        s = ""
        for item in row:
            s = s + item
        print(s)

def updateBoard(board, move): #returns the updated version of the board after a given move
    #printBoard(board)
    #print(move)
    pinLoc = getPinsAndLocations(board)
    #print(pinLoc)
    [pin, direction, jump] = move.split()
    board2 = deepcopy(board)
    jump = int(jump)
    r = pinLoc[pin][0]
    c = pinLoc[pin][1]
    board2[r][c] = '.'
    if direction == "up":
        board2[r - jump][c] = pin
        r = r - 1
        for _ in range(jump - 1):
            board2[r][c] = '.'
            r = r - 1
    elif direction == "down":
        board2[r + jump][c] = pin
        r = r + 1
        for _ in range(jump - 1):
            board2[r][c] = '.'
            r = r + 1
    elif direction == "left":
        board2[r][c - jump] = pin
        c = c - 1
        for _ in range(jump - 1):
            board2[r][c] = '.'
            c = c - 1
    elif direction == "right":
        board2[r][c + jump] = pin
        c = c + 1
        for _ in range(jump - 1):
            board2[r][c] = '.'
            c = c + 1

    return board2


def getPinsAndLocations(board): #returns pins on the board and their locations

    res = {}
    rows = len(board)
    columns = len(board[0])

    for i in range(rows):
        for j in range(columns):
            if board[i][j] != '.':
                res[board[i][j]] = [i,j]

    return collections.OrderedDict(sorted(res.items()))

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


"""def sortNodesByH1(nodes):

    nodesAndH1 = {}
    i = 0
    for node in nodes:
        board = node.board
        h = h1(board)
        nodesAndH1[i] = h
        i = i+1

    order = list(dict(sorted(nodesAndH1.items(), key=lambda item: item[1])).keys())

    res = []
    for i in range(len(nodes)):
        res.append(nodes[order[i]])
    return res"""

def allMovesSorted(board): #returns all possible moves but sorted in decreasing order according to path costs
    rows = len(board)
    columns = len(board[0])

    moves = []

    locs = getPinsAndLocations(board)

    ups = []
    rights = []
    downs = []
    lefts = []

    for pin in locs:
        up = canGo(board, pin, locs, "up")
        down = canGo(board, pin, locs, "down")
        left = canGo(board, pin, locs, "left")
        right = canGo(board, pin, locs, "right")
        if up != -1:
            ups.append(pin + " up " + str(up))
        if right != -1:
            rights.append(pin + " right " + str(right))
        if down != -1:
            downs.append(pin + " down " + str(down))
        if left != -1:
            lefts.append(pin + " left " + str(left))

    moves.extend(ups)
    moves.extend(rights)
    moves.extend(downs)
    moves.extend(lefts)
    return moves

def findAllMoves(board): #returns all possible moves in a board EXPAND
    rows = len(board)
    columns = len(board[0])

    moves = []

    locs = getPinsAndLocations(board)


    for pin in locs:
        up = canGo(board, pin, locs, "up")
        down = canGo(board, pin, locs, "down")
        left = canGo(board, pin, locs, "left")
        right = canGo(board, pin, locs, "right")
        if left != -1:
            moves.append(pin + " left " + str(left))
        if down != -1:
            moves.append(pin + " down " + str(down))
        if right != -1:
            moves.append(pin + " right " + str(right))
        if up != -1:
            moves.append(pin + " up " + str(up))


    #print(moves)
    return moves


def getCostOfAMove(move):
    move = move.split()
    direction = move[1]
    switcher = {
        "up": 1,
        "down": 3,
        "left": 4,
        "right": 2,
    }
    return switcher.get(direction)

def BFS(board):

    #printBoard(board)
    queue = []
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node(None, 0, nofPins, board, 0, "")

    queue.append(root)

    while len(queue) > 0:
        node = queue.pop(0)
        board = node.board
        nofPins = node.numberOfPins
        path = node.path
        if nofPins == 1:
            return True, node
        else:
            moves = findAllMoves(board)
            if len(moves) == 0:
                continue
            else:
                for move in moves:
                    removedPins = int(move.split()[2]) - 1
                    board_ = updateBoard(board, move)
                    #printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.append(Node(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost), (path + ", " + move)))

    return False, None


def DFS(board):

    stack = []
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node(None, 0, nofPins, board, 0, "")

    stack.append([root])

    while len(stack) > 0:
        lst = stack.pop()
        if len(lst) == 0:
            continue
        node = lst[0]
        board = node.board
        nofPins = node.numberOfPins
        path = node.path

        if nofPins == 1:
            return True, node

        moves = findAllMoves(board)
        if len(moves) == 0:
            lst.pop(0)
            stack.append(lst)
            continue

        stack.append(lst)
        l = []
        for move in moves:
            removedPins = int(move.split()[2]) - 1
            board_ = updateBoard(board, move)
            # printBoard(board_)
            cost = getCostOfAMove(move)
            l.append(Node(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost), (path + ", " + move)))

        stack.append(l)

    return False, None


def UCS(board):
    queue = []
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node(None, 0, nofPins, board, 0, "")

    queue.append(root)

    while len(queue) > 0:
        node = queue.pop(0)
        board = node.board
        nofPins = node.numberOfPins
        path = node.path
        if nofPins == 1:
            return True, node
        else:
            moves = allMovesSorted(board)
            if len(moves) == 0:
                continue
            else:
                for move in moves:
                    removedPins = int(move.split()[2]) - 1
                    board_ = updateBoard(board, move)
                    # printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.append(Node(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost),
                                      (path + ", " + move)))

    return False, None

def GS(board):

    #printBoard(board)
    queue = []
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node2(None, 0, nofPins, board, 0, "")

    queue.append(root)

    while len(queue) > 0:
        node = queue.pop(0)
        board = node.board
        nofPins = node.numberOfPins
        path = node.path
        if nofPins == 1:
            return True, node
        else:
            moves = findAllMoves(board)
            if len(moves) == 0:
                continue
            else:
                nodes = []
                for move in moves:
                    removedPins = int(move.split()[2]) - 1
                    board_ = updateBoard(board, move)
                    #printBoard(board_)
                    cost = getCostOfAMove(move)
                    nodes.append(Node2(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost), (path + ", " + move)))
                nodes.sort(key=lambda x: x.h1, reverse=False)
                queue.extend(nodes)

    return False, None


board = []
for line in txt.splitlines():

    l = []
    line = line.strip()
    s = len(line)
    for j in range(s):
        l.append(line[j])
    board.append(l)

printBoard(board)
success, node = GS(board)
print(success, node.cumulativeCost, node.path)
"""pinloc = getPinsAndLocations(board)

board2 = updateBoard(board, "d down 4", pinloc)
printBoard(board2)"""

import requests
from copy import copy, deepcopy
import collections
from operator import attrgetter
from queue import PriorityQueue
search_list=["BFS","DFS","UCS","GS","A*","A*2"]
search="BFS"
target_url="https://www.cmpe.boun.edu.tr/~emre/courses/cmpe480/hw1/input1"
txt = requests.get(target_url).text

nOfRemovedNodes = 0


class Node3:
    def __init__(self, parent, cost, numberOfPins, board, cumulativeCost, path, pin, direction):
        self.parent = parent
        self.cost = cost
        self.numberOfPins = numberOfPins
        #self.children = children
        self.board = board
        self.cumulativeCost = cumulativeCost
        self.path = path
        self.h1 = h1(board)
        self.pin = pin
        self.direction = direction

    def __lt__(self, other):
        if self.h1 + self.cumulativeCost < other.h1 + other.cumulativeCost:
            return True
        elif self.h1 + self.cumulativeCost == other.h1 + other.cumulativeCost and self.pin != other.pin:
            return self.pin < other.pin
        elif self.pin == other.pin:
            return directionPrecedence(self.direction, other.direction)


class Node2:
    def __init__(self, parent, cost, numberOfPins, board, cumulativeCost, path, pin, direction):
        self.parent = parent
        self.cost = cost
        self.numberOfPins = numberOfPins
        #self.children = children
        self.board = board
        self.cumulativeCost = cumulativeCost
        self.path = path
        self.h1 = h1(board)
        self.pin = pin
        self.direction = direction

    def __lt__(self, other):
        if self.h1 < other.h1:
            return True
        elif self.h1 == other.h1 and self.pin != other.pin:
            return self.pin < other.pin
        elif self.pin == other.pin:
            return directionPrecedence(self.direction, other.direction)

class Node:
    def __init__(self, parent, cost, numberOfPins, board, cumulativeCost, path, pin, direction):
        self.parent = parent
        self.cost = cost
        self.numberOfPins = numberOfPins
        #self.children = children
        self.board = board
        self.cumulativeCost = cumulativeCost
        self.path = path
        self.pin = pin
        self.direction = direction

    def __lt__(self, other):
        if self.cumulativeCost < other.cumulativeCost:
            return True
        elif self.cumulativeCost == other.cumulativeCost and self.pin != other.pin:
            return self.pin < other.pin
        elif self.pin == other.pin:
            return directionPrecedence(self.direction, other.direction)

def directionPrecedence(first, second):

    #print("aaa")

    if first == second:
        return False

    if first == "left":
        return True

    if first == "down":
        if second == "left":
            return False
        else:
            return True

    if first == "right":
        if second == "left" or second == "down":
            return False
        else:
            return True

    if first == "up":
        return False


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

    global nOfRemovedNodes
    #printBoard(board)
    queue = []
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node(None, 0, nofPins, board, 0, "", None, None)

    queue.append(root)

    while len(queue) > 0:
        node = queue.pop(0)
        nOfRemovedNodes = nOfRemovedNodes + 1
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
                    m = move.split()
                    removedPins = int(m[2]) - 1
                    board_ = updateBoard(board, move)
                    #printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.append(Node(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost), (path + ", " + m[0]+" "+m[1]), m[0], m[1]))

    return False, None


def DFS(board):
    global nOfRemovedNodes
    # printBoard(board)
    queue = []
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node(None, 0, nofPins, board, 0, "", None,None)

    queue.append(root)

    while len(queue) > 0:
        node = queue.pop()
        nOfRemovedNodes = nOfRemovedNodes + 1
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
                    m = move.split()
                    removedPins = int(m[2]) - 1
                    board_ = updateBoard(board, move)
                    # printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.append(Node(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost),
                                      (path + ", " + m[0]+" "+m[1]),m[0], m[1]))

    return False, None


def UCS(board):
    global nOfRemovedNodes
    queue = PriorityQueue()
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node(None, 0, nofPins, board, 0, "", None, None)

    queue.put(root)

    while not queue.empty():
        node = queue.get()
        nOfRemovedNodes = nOfRemovedNodes + 1
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
                    m = move.split()
                    removedPins = int(m[2]) - 1
                    board_ = updateBoard(board, move)
                    # printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.put(Node(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost),
                                      (path + ", " + m[0]+" "+m[1]),m[0], m[1]))

    return False, None

def GS(board):

    global nOfRemovedNodes

    #printBoard(board)
    queue = PriorityQueue()
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node2(None, 0, nofPins, board, 0, "", None, None)

    queue.put(root)

    while not queue.empty():
        node = queue.get()
        nOfRemovedNodes = nOfRemovedNodes + 1
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
                    m = move.split()
                    removedPins = int(m[2]) - 1
                    board_ = updateBoard(board, move)
                    #printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.put(Node2(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost), (path + ", " + m[0]+" "+m[1]),m[0], m[1]))

    return False, None

def A_star(board):
    global nOfRemovedNodes

    # printBoard(board)
    queue = PriorityQueue()
    pinsAndLocs = getPinsAndLocations(board)
    nofPins = len(pinsAndLocs)
    root = Node3(None, 0, nofPins, board, 0, "", None, None)

    queue.put(root)

    while not queue.empty():
        node = queue.get()
        nOfRemovedNodes = nOfRemovedNodes + 1
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
                    m = move.split()
                    removedPins = int(m[2]) - 1
                    board_ = updateBoard(board, move)
                    # printBoard(board_)
                    cost = getCostOfAMove(move)
                    queue.put(Node3(node, cost, (nofPins - removedPins), board_, (node.cumulativeCost + cost),
                                    (path + ", " + m[0] + " " + m[1]), m[0], m[1]))

    return False, None



board = []
for line in txt.splitlines():

    l = []
    line = line.strip()
    s = len(line)
    for j in range(s):
        l.append(line[j])
    board.append(l)

#printBoard(board)
success, node = UCS(board)
if success:
    print("Number of removed nodes:", nOfRemovedNodes)
    print("Path cost:", node.cumulativeCost)
    print("Solution:", node.path[2:] + ",")

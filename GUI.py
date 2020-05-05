import pygame
import time
from random import sample
pygame.font.init()

class Grid:
    def __init__(self, rows, cols, width, height, win):
        board = createBoard(self, rows)
        self.board = board
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.squares = [[Square(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None
        self.updateModel()

    def updateModel(self):
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def drawBoard(self):
        # Draw grid
        gap = self.width / 9

        for i in range(self.rows):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(self.win, (0,0,0), (i*gap, 0), (i*gap, self.height), thickness)
            pygame.draw.line(self.win, (0,0,0), (0,9*gap), (self.width, 9*gap), 4)

        # Draw squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.win)

    def setSquareTemp(self, val):
        row, col = self.selected
        self.squares[row][col].setTemp(val)

    def setSquare(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.updateModel()

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def select(self, row, col):
        # Resets previous selection
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False

        self.squares[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        self.squares[row][col].set(0)
        self.squares[row][col].setTemp(0)

    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.squares[row][col].set(i)
                self.squares[row][col].drawChange(self.win, True)
                self.updateModel()
                pygame.display.update()
                pygame.time.delay(50)

                if self.solve():
                    return True

                self.model[row][col] = 0
                self.squares[row][col].set(0)
                self.updateModel()
                self.squares[row][col].drawChange(self.win, False)
                pygame.display.update()
                pygame.time.delay(50)

        return False
            

class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont('arial', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y+ + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x,y, gap, gap), 3)

    def drawChange(self, win, green=True):
        font = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x+(gap/2-text.get_width()/2), y+(gap/2-text.get_height()/2)))

        if green:
            pygame.draw.rect(win, (0, 255, 0), (x,y,gap,gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x,y,gap,gap), 3)

    def set(self, val):
        self.value = val
    
    def setTemp(self, val):
        self.temp = val

def createBoard(self, rows):
    base = int(rows**0.5)
    side = base**2

    def pattern(row, col):
        return (base*(row%base)+row//base+col)%side

    def shuffle(s):
        return sample(s,len(s))

    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1,base*base+1))

    board = [[nums[pattern(r,c)] for c in cols] for r in rows]

    # Remove squares        
    # number of empty squares
    squares = side*side
    # lose a certain proportion of squares
    empties = squares * 1 // 2

    for p in sample(range(squares),empties):
        board[p//side][p%side] = 0

    return board

def redrawWindow(win, board, time):
    win.fill((255,255,255))
    
    # Draw time
    font = pygame.font.SysFont("arial", 40)
    timeText = font.render("Time: " + formatTime(time), 1, (0,0,0))
    win.blit(timeText, (540-160, 560))

    # Draw board
    board.drawBoard()

def formatTime(secs):
    seconds = secs%60
    minutes = seconds//60

    time = " " + str(minutes) + ":" + str(seconds)

    return time

def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def valid(board, num, pos):
    # check the row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # check the column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    
    return True
        

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    run = True
    start = time.time()

    while run:
        playTime = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.setSquare(board.squares[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if board.isFinished():
                            print("Game Over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None


        if board.selected and key != None:
            board.setSquareTemp(key)

        redrawWindow(win, board, playTime)
        pygame.display.update()

main()
pygame.quit()
import pygame
import time
pygame.font.init()

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
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

    def set(self, val):
        self.value = val
    
    def setTemp(self, val):
        self.temp = val



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
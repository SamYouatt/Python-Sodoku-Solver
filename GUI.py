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

class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def draw(self, win):
        font = pygame.font.SysFont('arial', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value != 0:            
            valueText = font.render(str(self.value), 1, (0,0,0))
            win.blit(valueText, (x + (gap/2 - valueText.get_width()/2), y + (gap/2 - valueText.get_height()/2)))



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


        redrawWindow(win, board, playTime)
        pygame.display.update()

main()
pygame.quit()
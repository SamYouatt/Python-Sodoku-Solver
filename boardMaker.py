# Testing creation function

from random import randint, sample

def createBoard():
    base = 3
    side = base**2

    # 
    def pattern(row, col):
        return (base*(row%base)+row//base+col)%side

    def shuffle(s):
        return sample(s,len(s))

    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1,base*base+1))

    board = [[nums[pattern(r,c)] for c in cols] for r in rows]

    def remove():
        # number of empty squares
        squares = side*side
        # lose 75% of squares
        empties = squares * 3 // 4

        for p in sample(range(squares),empties):
            board[p//side][p%side] = 0

    print(board)
    remove()
    print(board)
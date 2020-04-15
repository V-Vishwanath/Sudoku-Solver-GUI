import tkinter as tk


class SudokuBoard:
    def __init__(self):
        self.selected = None
        self.x = None
        self.y = None
        self.row = None
        self.col = None
        self.solved = False

        self.board = None
        self.keys = None

        root = tk.Tk()
        root.title('Sudoku Solver')
        root.geometry('540x540+100+100')

        self.canvas = tk.Canvas(root, width=540, height=540)
        self.canvas.bind('<Key>', self.get_key)
        self.canvas.bind('<Button-1>', self.set_num)
        self.canvas.pack()

        self.init_board()

        root.mainloop()

    def init_board(self):
        self.selected = None
        self.x = None
        self.y = None
        self.row = None
        self.col = None
        self.solved = False

        self.keys = [[None]*9 for i in range(9)]
        self.board = [[0]*9 for i in range(9)]

        for i in range(0, 541, 60):
            if i % 180 == 0:
                self.canvas.create_line(i, 0, i, 540, width=3)
                self.canvas.create_line(0, i, 540, i, width=3)
            else:
                self.canvas.create_line(i, 0, i, 540)
                self.canvas.create_line(0, i, 540, i)

        self.canvas.focus_set()

    def get_key(self, event):
        key = str(event.char)
        if key.isdigit():
            try:
                if self.board[self.row][self.col] != 0:
                    self.canvas.delete(self.keys[self.row][self.col])

                self.keys[self.row][self.col] = self.canvas.create_text(
                    self.x, self.y, text=key, font=('Comic sans ms', 13, 'bold'))
                self.board[self.row][self.col] = int(key)
            except:
                pass

        elif key == '\b':
            self.canvas.delete(self.keys[self.row][self.col])
            self.board[self.row][self.col] = 0

        elif key == '\r':
            if not self.solved:
                self.canvas.delete(self.selected)
                self.solve()
                for i in range(9):
                    for j in range(9):
                        if self.keys[i][j] is None:
                            x = 60*j + 30
                            y = 60*i + 30
                            self.canvas.create_text(
                                x, y, text=self.board[i][j], font='-size 12 -weight bold', fill='grey')
                self.solved = True

            else:
                self.canvas.delete('all')
                self.init_board()

    def set_num(self, event):
        if not self.solved:
            self.row = event.y // 60
            self.col = event.x // 60

            self.y = (60 * self.row) + 30
            self.x = (60 * self.col) + 30

            self.canvas.delete(self.selected)
            self.selected = self.canvas.create_rectangle(
                self.x-30, self.y-30, self.x+30, self.y+30, outline='green', width=3)

    def empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def validPos(self, n, pos):
        for i in range(9):
            if self.board[i][pos[1]] == n and pos[0] != i:
                return False

            if self.board[pos[0]][i] == n and pos[1] != i:
                return False

        x = (pos[0] // 3) * 3
        y = (pos[1] // 3) * 3
        for i in range(x, x + 3):
            for j in range(y, y + 3):
                if self.board[i][j] == n and (i, j) != pos:
                    return False
        return True

    def solve(self):
        pos = self.empty()

        if not pos:
            self.solved = True
            return True

        for n in range(1, 10):
            if self.validPos(n, pos):
                self.board[pos[0]][pos[1]] = n

                if self.solve():
                    return True

                self.board[pos[0]][pos[1]] = 0

        return False


SudokuBoard()

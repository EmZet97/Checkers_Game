class Pawn:
    _colors = [(255, 255, 255), (0, 0, 0)]

    def __init__(self, size, i, j, team, board, owner):
        self.haveMC = False
        self.alive = True
        self.owner = owner
        self._hc = False
        self.is_clicked = False
        self.size = size
        self.canMove = False
        self.i = i
        self.j = j
        board.pawns[i][j] = self
        self.x = board.fields[i][j].x + int(board.field_size / 2)
        self.y = board.fields[i][j].y + int(board.field_size / 2)
        self.team = team
        self.board = board
        self.color = self._colors[self.team]
        self.modifier = lambda x: self.get_modifier(x)
        self.delete = lambda i, j: self.owner.enemy.delete_pawn(i, j)

    def check_if_clicked(self, x, y, field_size):
        if self.x - field_size < x and self.x + field_size > x and self.y - field_size < y and self.y + field_size > y and self.alive:
            return True

        return False

    def change_color(self, *color):
        self.color = color
        self.is_clicked = True

    def back_last_color(self):
        self.color = self._colors[self.team]
        self.is_clicked = False

    #def delete(self, i, j):
     #   self.owner.enemy.delete_pawn(i, j)

    @staticmethod
    def get_modifier(team):
        if team == 1:
            return -1
        return 1


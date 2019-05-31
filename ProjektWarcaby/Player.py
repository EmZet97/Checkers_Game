import Pawn


class Player:
    lastClicked = -1
    enemy = None

    def __init__(self, team, board):
        self.points = 0
        self.pawns = []
        self.team = team
        self.board = board
        for i in range(team*6, team*6+2):
            for j in range(4):
                self.pawns.append(Pawn.NormalPawn(20, i, j * 2 + 1 - i % 2, self.team, self.board, self))

    def get_points(self):
        return self.points

    def set_enemy(self, enemy):
        self.enemy = enemy

    def draw_pawns(self, screen):
        for pawn in self.pawns:
            if pawn != None:
                pawn.draw(screen)

    def check_if_pawn_clicked(self, x, y, field_size):
        i = -1
        for pawn in self.pawns:
            i += 1
            if pawn.check_if_clicked(x, y, field_size):
                self.lastClicked = i
                return pawn

    def get_clicked_field(self, x, y):
        for i in range(8):
            for j in range(8):
                if(self.board.fields[i][j].check_if_clicked(x, y)):
                    return (i, j)
        return (-1, -1)

    def get_last_clicked(self):
        if self.lastClicked != -1:
            return self.pawns[self.lastClicked]
        else:
            return  None

    def delete_pawn(self, i, j):
        self.board.pawns[i][j].alive = False

    def create_king(self, i, j):
        self.board.pawns[i][j].alive = False
        self.pawns.append(Pawn.King(20, i, j, self.team, self.board, self))


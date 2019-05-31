import pygame
from Pawns.Pawn import Pawn
import Exceptions


class NormalPawn(Pawn):
    def move(self, i, j):
        self.board.pawns[self.i][self.j] = None
        self.board.pawns[i][j] = self
        self.x = self.board.fields[i][j].get_x() + int(self.board.field_size / 2)
        self.y = self.board.fields[i][j].get_y() + int(self.board.field_size / 2)
        self.i = i
        self.j = j
        if self.team == 0 and self.i == 7:
            self.owner.create_king(i, j)
        if self.team == 1 and self.i == 0:
            self.owner.create_king(i, j)

    def draw(self, screen):
        if self.alive:

            #pygame.draw.circle(screen, self.x, self.y, 20, self.color)
            pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
            #pygame.gfxdraw.aacircle(screen, self.x, self.y, 20, self.color)
            #pygame.gfxdraw.filled_circle(screen, self.x, self.y, 20, self.color)
            # pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
            self.show_ways(screen)

    def check_move(self, i, j):
        # team direction var
        md = self.modifier(self.team)

        if self.is_clicked and self.alive:
            # Check if can move left
            if self.check_if_empty(self.i + md,
                                 self.j - 1) and self.i + md == i and self.j - 1 == j and self._hc == False and self.haveMC == False:
                self.move(i, j)
                return 1
            # Check if can move right
            if self.check_if_empty(self.i + md,
                                 self.j + 1) and self.i + md == i and self.j + 1 == j and self._hc == False and self.haveMC == False:
                self.move(i, j)
                return 1

            # Check if can clash left
            if self.check_if_enemy(self.i + md, self.j - 1):
                if self.find_left_clash(self.i, self.j) and self.i + md * 2 == i and self.j - 2 == j:
                    self.delete(self.i + md, self.j - 1)
                    self.move(i, j)
                    return 2

            # Check if can clash right
            if self.check_if_enemy(self.i + md, self.j + 1):
                if self.find_right_clash(self.i, self.j) and self.i + md * 2 == i and self.j + 2 == j:
                    self.delete(self.i + md, self.j + 1)
                    self.move(i, j)
                    return 2

            # Check if can clash left back
            if self.check_if_enemy(self.i - md, self.j - 1):
                if self.find_left_back_clash(self.i, self.j) and self.i - md * 2 == i and self.j - 2 == j:
                    self.delete(self.i - md, self.j - 1)
                    self.move(i, j)
                    return 2

            # Check if can clash right back
            if self.check_if_enemy(self.i - md, self.j + 1):
                if self.find_right_back_clash(self.i, self.j) and self.i - md * 2 == i and self.j + 2 == j:
                    self.delete(self.i - md, self.j + 1)
                    self.move(i, j)
                    return 2
            raise Exceptions.WrongMoveException
            return 0

    def show_ways(self, screen):
        md = self.modifier(self.team)

        if self.is_clicked and self.alive:
            hc = False
            # Check if can clash left
            if self.check_if_enemy(self.i + md, self.j - 1):
                if self.find_left_clash(self.i, self.j):
                    self.draw_way(screen, self.i + md * 2, self.j - 2)
                    hc = True
            # Check if can clash right
            if self.check_if_enemy(self.i + md, self.j + 1):
                if self.find_right_clash(self.i, self.j):
                    self.draw_way(screen, self.i + md * 2, self.j + 2)
                    hc = True

            # Check if can clash left back
            if self.check_if_enemy(self.i - md, self.j - 1):
                if self.find_left_back_clash(self.i, self.j):
                    self.draw_way(screen, self.i - md * 2, self.j - 2)
                    hc = True
            # Check if can clash right back
            if self.check_if_enemy(self.i - md, self.j + 1):
                if self.find_right_back_clash(self.i, self.j):
                    self.draw_way(screen, self.i - md * 2, self.j + 2)
                    hc = True

            # Check if can move left
            if self.check_if_empty(self.i + md, self.j - 1) == True and hc == False and self.haveMC == False:
                # print("W1")
                self.draw_way(screen, self.i + md, self.j - 1)

            # Check if can move right
            if self.check_if_empty(self.i + md, self.j + 1) == True and hc == False and self.haveMC == False:
                self.draw_way(screen, self.i + md, self.j + 1)

            if hc:
                self._hc = True
            else:
                self._hc = False

    def check_if_have_clash(self):
        md = self.modifier(self.team)

        if self.is_clicked and self.alive:
            # Check if can clash left
            if self.check_if_enemy(self.i + md, self.j - 1):
                if self.find_left_clash(self.i, self.j):
                    return True
            # Check if can clash right
            if self.check_if_enemy(self.i + md, self.j + 1):
                if self.find_right_clash(self.i, self.j):
                    return True

            # Check if can clash left back
            if self.check_if_enemy(self.i - md, self.j - 1):
                if self.find_left_back_clash(self.i, self.j):
                    return True
            # Check if can clash right back
            if self.check_if_enemy(self.i - md, self.j + 1):
                if self.find_right_back_clash(self.i, self.j):
                    return True

        return False

    def draw_way(self, screen, i, j):
        p = pygame.Rect(self.board.fields[i][j].x, self.board.fields[i][j].y, 50, 50)
        pygame.draw.rect(screen, (128, 128, 128), p)

    def check_area(self, i, j):
        return self.board.pawns[i][j]

    def check_area_object(self, i, j):
        p = self.check_area(i, j)
        if p != None and p.alive:
            if p.team == self.team:
                #print("My team")
                return 1
            else:
                #print("ENEMY!!!")
                return 0
        else:
            #print("None")
            return -1

    def check_if_enemy(self, i, j):
        if i > -1 and i < 8 and j > -1 and j < 8:
            if self.check_area_object(i, j) == 0:
                # print("Is enemy")
                return True
        #else:
            #print("Bad coordinates: ", i, ", ", j)
        return False

    def check_if_empty(self, i, j):
        if i > -1 and i < 8 and j > -1 and j < 8:
            if self.check_area_object(i, j) == -1:
                return True
        #else:
            #print("Bad coordinates: ", i, ", ", j)
        return False

    def find_left_clash(self, i, j):
        if self.team == 0:
            md = 1
        else:
            md = -1
        if self.check_if_enemy(i + md, j - 1):
            if self.check_if_empty(i + 2 * md, j - 2):
                return True

        return False

    def find_right_clash(self, i, j):
        if self.team == 0:
            md = 1
        else:
            md = -1
        if self.check_if_enemy(i + md, j + 1):
            if self.check_if_empty(i + 2 * md, j + 2):
                return True

        return False

    def find_left_back_clash(self, i, j):
        if self.team == 0:
            md = -1
        else:
            md = 1
        if self.check_if_enemy(i + md, j - 1):
            if self.check_if_empty(i + 2 * md, j - 2):
                return True

        return False

    def find_right_back_clash(self, i, j):
        if self.team == 0:
            md = -1
        else:
            md = 1
        if self.check_if_enemy(i + md, j + 1):
            if self.check_if_empty(i + 2 * md, j + 2):
                return True

        return False

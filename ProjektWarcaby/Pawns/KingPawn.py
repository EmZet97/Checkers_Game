import pygame
import pygame as pg
from Pawns.Pawn import Pawn
import Exceptions


class King(Pawn):
    def move(self, i, j):
        self.board.pawns[self.i][self.j] = None
        self.board.pawns[i][j] = self
        self.x = self.board.fields[i][j].get_x() + int(self.board.field_size / 2)
        self.y = self.board.fields[i][j].get_y() + int(self.board.field_size / 2)
        self.i = i
        self.j = j

    def draw(self, screen):
        if (self.alive):
            if self.team == 0:
                pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 22)
                #pygame.gfxdraw.aacircle(screen, self.x, self.y, 24, (0, 0, 0))
                #pygame.gfxdraw.filled_circle(screen, self.x, self.y, 24, (0, 0, 0))
            else:
                pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 22)
                #pygame.gfxdraw.aacircle(screen, self.x, self.y, 24, (255, 255, 255))
                #pygame.gfxdraw.filled_circle(screen, self.x, self.y, 22, (255, 255, 255))

            pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
            #pygame.gfxdraw.aacircle(screen, self.x, self.y, 20, self.color)
            #pygame.gfxdraw.filled_circle(screen, self.x, self.y, 20, self.color)
            self.show_ways(screen)

    def check_if_have_clash(self):
        if self.team == 0:
            md = 1
        else:
            md = -1
        if (self.is_clicked and self.alive):
            # Check if can clash left
            if (self.check_if_enemy(self.i + md, self.j - 1)):
                if (self.find_left_clash(self.i, self.j)):
                    return True
            # Check if can clash right
            if (self.check_if_enemy(self.i + md, self.j + 1)):
                if (self.find_right_clash(self.i, self.j)):
                    return True

            # Check if can clash left back
            if (self.check_if_enemy(self.i - md, self.j - 1)):
                if (self.find_left_back_clash(self.i, self.j)):
                    return True
            # Check if can clash right back
            if (self.check_if_enemy(self.i - md, self.j + 1)):
                if (self.find_right_back_clash(self.i, self.j)):
                    return True

        return False

    def check_move(self, i, j):
        if self.team == 0:
            md = 1
        else:
            md = -1
        if self.is_clicked and self.alive:
            hc = False

            """NEAR CLASH CLASH CLASH CLASH CLASH"""
            # Check if can clash near left
            t_left = 2
            if (self.check_if_enemy(self.i + md, self.j - 1)):
                if (self.find_left_clash(self.i, self.j)):
                    enemy_i = self.i + md
                    enemy_j = self.j - 1
                    while (self.check_if_empty(self.i + md * t_left, self.j - 1 * t_left)):
                        if (i == self.i + md * t_left and j == self.j - 1 * t_left):
                            self.delete(enemy_i, enemy_j)
                            self.move(i, j)
                            hc = True
                            return 2
                        t_left += 1

            # Check if can clash near right
            t_right = 2
            if (self.check_if_enemy(self.i + md, self.j + 1)):
                if (self.find_right_clash(self.i, self.j)):
                    enemy_i = self.i + md
                    enemy_j = self.j + 1
                    while (self.check_if_empty(self.i + md * t_right, self.j + 1 * t_right)):
                        if (i == self.i + md * t_right and j == self.j + 1 * t_right):
                            self.delete(enemy_i, enemy_j)
                            self.move(i, j)
                            hc = True
                            return 2
                        t_right += 1

            # Check if can clash near left back
            t_left = 2
            if (self.check_if_enemy(self.i + md * (-1), self.j - 1)):
                if (self.find_left_back_clash(self.i, self.j)):
                    enemy_i = self.i + md * (-1)
                    enemy_j = self.j - 1
                    while (self.check_if_empty(self.i + md * (-1) * t_left, self.j - 1 * t_left)):
                        if (i == self.i + md * (-1) * t_left and j == self.j - 1 * t_left):
                            self.delete(enemy_i, enemy_j)
                            self.move(i, j)
                            hc = True
                            return 2
                        t_left += 2

            # Check if can clash near right back
            t_right = 2
            if (self.check_if_enemy(self.i + md * (-1), self.j + 1)):
                if (self.find_right_back_clash(self.i, self.j)):
                    enemy_i = self.i + md * (-1)
                    enemy_j = self.j + 1
                    while (self.check_if_empty(self.i + md * (-1) * t_right, self.j + 1 * t_right)):
                        if (i == self.i + md * (-1) * t_right and j == self.j + 1 * t_right):
                            self.delete(enemy_i, enemy_j)
                            self.move(i, j)
                            hc = True
                            return 2
                        t_right += 1

            """FAR CLASH CLASH CLASH CLASH CLASH"""
            # Check if can clash far left
            t_left = 1
            while (self.check_if_empty(self.i + md * t_left, self.j - 1 * t_left) == True):
                if (self.check_if_enemy(self.i + md * t_left + md, self.j - 1 * t_left - 1)):
                    if (self.find_left_clash(self.i + md * t_left, self.j - 1 * t_left)):
                        enemy_i = self.i + md * t_left + md
                        enemy_j = self.j - 1 * t_left - 1
                        while (self.check_if_empty(self.i + md * t_left + 2 * md, self.j - 1 * t_left - 2)):
                            if (i == self.i + md * t_left + 2 * md and j == self.j - 1 * t_left - 2):
                                self.delete(enemy_i, enemy_j)
                                self.move(i, j)
                                hc = True
                                return 2
                            t_left += 1
                t_left += 1

            # Check if can clash far right
            t_right = 1
            while (self.check_if_empty(self.i + md * t_right, self.j + 1 * t_right) == True):
                if (self.check_if_enemy(self.i + md * t_right + md, self.j + 1 * t_right + 1)):
                    if (self.find_right_clash(self.i + md * t_right, self.j + 1 * t_right)):
                        enemy_i = self.i + md * t_right + md
                        enemy_j = self.j + 1 * t_right + 1
                        while (self.check_if_empty(self.i + md * t_right + 2 * md, self.j + 1 * t_right + 2)):
                            if (i == self.i + md * t_right + 2 * md and j == self.j + 1 * t_right + 2):
                                self.delete(enemy_i, enemy_j)
                                self.move(i, j)
                                hc = True
                                return 2
                            t_right += 1
                t_right += 1

            # Check if can clash far left back
            t_left = 1
            while (self.check_if_empty(self.i + md * (-1) * t_left, self.j - 1 * t_left) == True):
                if (self.check_if_enemy(self.i + md * (-1) * t_left + md * (-1), self.j - 1 * t_left - 1)):
                    if (self.find_left_back_clash(self.i + md * (-1) * t_left, self.j - 1 * t_left)):
                        enemy_i = self.i + md * (-1) * t_left + md * (-1)
                        enemy_j = self.j - 1 * t_left - 1
                        while (
                        self.check_if_empty(self.i + md * (-1) * t_left + 2 * md * (-1), self.j - 1 * t_left - 2)):
                            if (i == self.i + md * (-1) * t_left + 2 * md * (-1) and j == self.j - 1 * t_left - 2):
                                self.delete(enemy_i, enemy_j)
                                self.move(i, j)
                                hc = True
                                return 2
                            t_left += 1
                t_left += 1

            # Check if can clash far right back
            t_right = 1
            while self.check_if_empty(self.i + md * (-1) * t_right, self.j + 1 * t_right) == True:
                if self.check_if_enemy(self.i + md * (-1) * t_right + md * (-1), self.j + 1 * t_right + 1):
                    if self.find_right_back_clash(self.i + md * (-1) * t_right, self.j + 1 * t_right):
                        enemy_i = self.i + md * (-1) * t_right + md * (-1)
                        enemy_j = self.j + 1 * t_right + 1
                        while (
                        self.check_if_empty(self.i + md * (-1) * t_right + 2 * md * (-1), self.j + 1 * t_right + 2)):
                            if (i == self.i + md * (-1) * t_right + 2 * md * (-1) and j == self.j + 1 * t_right + 2):
                                self.delete(enemy_i, enemy_j)
                                self.move(i, j)
                                hc = True
                                return 2
                            t_right += 1
                t_right += 1
            """MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE"""
            # Check if can move left
            t_left = 1
            while self.check_if_empty(self.i + md * t_left,
                                      self.j - 1 * t_left) == True and self._hc == False and self.haveMC == False:
                if i == self.i + md * t_left and j == self.j - 1 * t_left:
                    self.move(i, j)
                    return 1
                t_left += 1

            # Check if can move right
            t_right = 1
            while self.check_if_empty(self.i + md * t_right,
                                      self.j + 1 * t_right) == True and self._hc == False and self.haveMC == False:
                if i == self.i + md * t_right and j == self.j + 1 * t_right:
                    self.move(i, j)
                    return 1
                t_right += 1

            # Check if can move left back
            t_left = 1
            while self.check_if_empty(self.i + md * (-1) * t_left,
                                      self.j - 1 * t_left) == True and self._hc == False and self.haveMC == False:
                if i == self.i + md * (-1) * t_left and j == self.j - 1 * t_left:
                    self.move(i, j)
                    return 1
                t_left += 1

            # Check if can move right back
            t_right = 1
            while self.check_if_empty(self.i + md * (-1) * t_right,
                                      self.j + 1 * t_right) == True and self._hc == False and self.haveMC == False:
                if i == self.i + md * (-1) * t_right and j == self.j + 1 * t_right:
                    self.move(i, j)
                    return 1
                t_right += 1

            """IF HAVE CLASH"""
            if hc:
                self._hc = True
            else:
                self._hc = False

            raise Exceptions.WrongMoveException
            return 0

    def show_ways(self, screen):
        md = self.modifier(self.team)
        if self.is_clicked and self.alive:
            hc = False

            """NEAR CLASH CLASH CLASH CLASH CLASH"""
            # Check if can clash near left
            t_left = 2
            if self.check_if_enemy(self.i + md, self.j - 1):
                if self.find_left_clash(self.i, self.j):
                    while self.check_if_empty(self.i + md * t_left, self.j - 1 * t_left):
                        self.draw_way(screen, self.i + md * t_left, self.j - 1 * t_left)
                        hc = True
                        t_left += 1

            # Check if can clash near right
            t_right = 2
            if self.check_if_enemy(self.i + md, self.j + 1):
                if self.find_right_clash(self.i, self.j):
                    while self.check_if_empty(self.i + md * t_right, self.j + 1 * t_right):
                        self.draw_way(screen, self.i + md * t_right, self.j + 1 * t_right)
                        hc = True
                        t_right += 1

            # Check if can clash near left back
            t_left = 2
            if self.check_if_enemy(self.i - md, self.j - 1):
                if self.find_left_back_clash(self.i, self.j):
                    while self.check_if_empty(self.i + md * (-1) * t_left, self.j - 1 * t_left):
                        self.draw_way(screen, self.i + md * (-1) * t_left, self.j - 1 * t_left)
                        hc = True
                        t_left += 1

            # Check if can clash near right back
            t_right = 2
            if self.check_if_enemy(self.i - md, self.j + 1):
                if self.find_right_back_clash(self.i, self.j):
                    while self.check_if_empty(self.i + md * (-1) * t_right, self.j + 1 * t_right):
                        self.draw_way(screen, self.i + md * (-1) * t_right, self.j + 1 * t_right)
                        hc = True
                        t_right += 1

            """FAR CLASH CLASH CLASH CLASH CLASH"""
            # Check if can clash far left
            t_left = 1
            while self.check_if_empty(self.i + md * t_left, self.j - 1 * t_left):
                if self.check_if_enemy(self.i + md * t_left + md, self.j - 1 * t_left - 1):
                    if self.find_left_clash(self.i + md * t_left, self.j - 1 * t_left):
                        while self.check_if_empty(self.i + md * t_left + 2 * md, self.j - 1 * t_left - 2):
                            self.draw_way(screen, self.i + md * t_left + 2 * md, self.j - 1 * t_left - 2)
                            hc = True
                            t_left += 1
                t_left += 1

            # Check if can clash far right
            t_right = 1
            while self.check_if_empty(self.i + md * t_right, self.j + 1 * t_right):
                if self.check_if_enemy(self.i + md * t_right + md, self.j + 1 * t_right + 1):
                    if self.find_right_clash(self.i + md * t_right, self.j + 1 * t_right):
                        while self.check_if_empty(self.i + md * t_right + 2 * md, self.j + 1 * t_right + 2):
                            self.draw_way(screen, self.i + md * t_right + 2 * md, self.j + 1 * t_right + 2)
                            hc = True
                            t_right += 1
                t_right += 1

            # Check if can clash far left back
            t_left = 1
            while self.check_if_empty(self.i + md * (-1) * t_left, self.j - 1 * t_left):
                if self.check_if_enemy(self.i + md * (-1) * t_left + md * (-1), self.j - 1 * t_left - 1):
                    if self.find_left_back_clash(self.i + md * (-1) * t_left, self.j - 1 * t_left):
                        while self.check_if_empty(self.i + md * (-1) * t_left + 2 * md * (-1), self.j - 1 * t_left - 2):
                            self.draw_way(screen, self.i + md * (-1) * t_left + 2 * md * (-1), self.j - 1 * t_left - 2)
                            hc = True
                            t_left += 1
                t_left += 1

            # Check if can clash far right back
            t_right = 1
            while self.check_if_empty(self.i + md * (-1) * t_right, self.j + 1 * t_right):
                if self.check_if_enemy(self.i + md * (-1) * t_right + md * (-1), self.j + 1 * t_right + 1):
                    if self.find_right_back_clash(self.i + md * (-1) * t_right, self.j + 1 * t_right):
                        while self.check_if_empty(self.i + md * (-1) * t_right + 2 * md * (-1),
                                                  self.j + 1 * t_right + 2):
                            self.draw_way(screen, self.i + md * (-1) * t_right + 2 * md * (-1),
                                          self.j + 1 * t_right + 2)
                            hc = True
                            t_right += 1
                t_right += 1
            """MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE"""
            # Check if can move left
            t_left = 1
            while self.check_if_empty(self.i + md * t_left,
                                      self.j - 1 * t_left) == True and hc == False and self.haveMC == False:
                self.draw_way(screen, self.i + md * t_left, self.j - 1 * t_left)
                t_left += 1

            # Check if can move right
            t_right = 1
            while self.check_if_empty(self.i + md * t_right,
                                      self.j + 1 * t_right) == True and hc == False and self.haveMC == False:
                self.draw_way(screen, self.i + md * t_right, self.j + 1 * t_right)
                t_right += 1

            # Check if can move left back
            t_left = 1
            while self.check_if_empty(self.i + md * (-1) * t_left,
                                      self.j - 1 * t_left) == True and hc == False and self.haveMC == False:
                self.draw_way(screen, self.i + md * (-1) * t_left, self.j - 1 * t_left)
                t_left += 1

            # Check if can move right back
            t_right = 1
            while self.check_if_empty(self.i + md * (-1) * t_right,
                                      self.j + 1 * t_right) == True and hc == False and self.haveMC == False:
                self.draw_way(screen, self.i + md * (-1) * t_right, self.j + 1 * t_right)
                t_right += 1

            """IF HAVE CLASH"""
            if hc:
                self._hc = True
            else:
                self._hc = False

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
        #print("CheckIfEnemy ", i, " ", j)
        if i > -1 and i < 8 and j > -1 and j < 8:
            if self.check_area_object(i, j) == 0:
                #print("Is enemy")
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
        md = self.modifier(self.team)
        if self.check_if_enemy(i + md, j - 1):
            if self.check_if_empty(i + 2 * md, j - 2):
                return True

        return False

    def find_right_clash(self, i, j):
        md = self.modifier(self.team)
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
import sys
import pygame
import Board
import Player
import main
import Text
from pygame import gfxdraw
wp = 6
plansza = None
gracz1 = None
gracz2 = None

text1 = None
text2 = None
endText = Text.Text(300, 300)
restartText = Text.Text(350, 550, 120, 50)

screen = None
playable = False

turn = 0
haveMoreClashes = False


def mouse_pressed():
    restartText.check_if_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    if main.playable:
        game_controller()
    else:
        init_game()


def game_controller():
    t = main.turn
    if t % 2 == 0:
        if gracz1.get_last_clicked() is not None:
            pole = gracz1.get_clicked_field(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            ruch = gracz1.get_last_clicked().check_move(pole[0], pole[1])
            if ruch:
                if ruch == 2:
                    gracz1.points += 1
                if gracz1.get_last_clicked().check_if_have_clash() and ruch == 2:
                    gracz1.get_last_clicked().haveMC = True
                    main.haveMoreClashes = True
                else:
                    t = t + 1
                    main.turn += 1
                    gracz1.get_last_clicked().haveMC = False
                    gracz1.get_last_clicked().back_last_color()
                    main.haveMoreClashes = False
                return
            elif not main.haveMoreClashes:
                gracz1.get_last_clicked().haveMC = False
                gracz1.get_last_clicked().back_last_color()
                main.haveMoreClashes = False
        if not main.haveMoreClashes:
            p = gracz1.check_if_pawn_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 25)
            if p != None:
                p.change_color((60, 60, 60))

    if t % 2 == 1:
        if gracz2.get_last_clicked() != None:
            pole = gracz2.get_clicked_field(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            ruch = gracz2.get_last_clicked().check_move(pole[0], pole[1])
            if ruch:
                if ruch == 2:
                    gracz2.points += 1
                if gracz2.get_last_clicked().check_if_have_clash() and ruch == 2:
                    gracz2.get_last_clicked().haveMC = True
                    main.haveMoreClashes = True
                else:
                    t = t + 1
                    main.turn += 1
                    gracz2.get_last_clicked().haveMC = False
                    gracz2.get_last_clicked().back_last_color()
                    main.haveMoreClashes = False
                return
            elif not main.haveMoreClashes:
                gracz2.get_last_clicked().haveMC = False
                gracz2.get_last_clicked().back_last_color()
                main.haveMoreClashes = False
        if not main.haveMoreClashes:
            p = gracz2.check_if_pawn_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 25)
            if p != None:
                p.change_color((60, 60, 60))

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed()

def init_game():
    print("Init Game")
    restartText.make_clickable(init_game)
    main.turn = 0
    main.plansza = Board.Board(8, 200, 100, 50)
    pygame.display.set_caption("Warcaby")
    logo = pygame.image.load("img/icon.png")
    pygame.display.set_icon(logo)
    main.gracz1 = Player.Player(0, main.plansza)
    main.gracz2 = Player.Player(1, main.plansza)
    main.gracz1.set_enemy(main.gracz2)
    main.gracz2.set_enemy(main.gracz1)
    main.text1 = Text.Text(100, 100)
    main.text2 = Text.Text(100, 450)
    main.playable = True
    main.haveMoreClashes = False

def game_progress():
    #print("Progress ", gracz2.points, " - ", gracz1.points)
    if gracz2.points > wp or gracz1.points > wp:
        #InitGame()
        main.playable = False

def drawStats():
    restartText.write(screen, "Restart")
    if main.turn % 2:
        text1.write(screen, str(gracz1.points))
        text2.write(screen, str(gracz2.points) + " <-")
    else:
        text1.write(screen, str(gracz1.points) + " <-")
        text2.write(screen, str(gracz2.points))

def Update(screen):
    events()
    game_progress()

    pygame.display.flip()
    screen.fill((0, 0, 0))
    if playable:
        plansza.draw(screen)
        gracz1.draw_pawns(screen)
        gracz2.draw_pawns(screen)
        drawStats()
    else:
        if main.gracz1.points > wp:
            endText.write(screen, "Zwyciezyl bialy")
        else:
            endText.write(screen, "Zwyciezyl czarny")


def Start():
    pygame.init()
    size = width, height = 800, 600
    main.screen = pygame.display.set_mode(size)
    init_game()

    while 1:
        Update(screen)
        #pygame.transform.smoothscale(screen, (400, 300))



Start()

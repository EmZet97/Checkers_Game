import sys
import pygame
from Background import Board
import Player
import main
from UI import Text
from UI import UI
import Exceptions


board = None
player1 = None
player2 = None

text1 = None
text2 = None
end_text = Text.Text(300, 300)
info_text = Text.Text(250, 50, 120, 40)
turn_text = Text.Text(300, 10, 120, 60)
restart_text = Text.Text(350, 550, 120, 50)

screen = None
playable = False

turn = 0
haveMoreClashes = False


def mouse_pressed():
    restart_text.check_if_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    if main.playable:
        game_controller()
    else:
        init_game()


def game_controller():
    t = main.turn
    if t % 2 == 0:
        if player1.get_last_clicked() is not None:
            pole = player1.get_clicked_field(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            move = 0
            try:
                move = player1.get_last_clicked().check_move(pole[0], pole[1])
            except Exceptions.WrongMoveException:
                print("Player 1 incorrect move")
                #player1.get_last_clicked().back_last_color()

            if move:
                if move == 2:
                    player1.points += 1
                if player1.get_last_clicked().check_if_have_clash() and move == 2:
                    player1.get_last_clicked().haveMC = True
                    main.haveMoreClashes = True
                else:
                    t = t + 1
                    main.turn += 1
                    player1.get_last_clicked().haveMC = False
                    player1.get_last_clicked().back_last_color()
                    main.haveMoreClashes = False
                return
            elif not main.haveMoreClashes:
                player1.get_last_clicked().haveMC = False
                player1.get_last_clicked().back_last_color()
                main.haveMoreClashes = False
        if not main.haveMoreClashes:
            try:
                p = player1.check_if_pawn_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 25)
            except Exceptions.WrongTeamPickException:
                print("Niepoprawnie wybrany pionek")
            else:
                p.change_color((60, 60, 60))

    if t % 2 == 1:
        if player2.get_last_clicked() != None:
            pole = player2.get_clicked_field(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            move = 0
            try:
                move = player2.get_last_clicked().check_move(pole[0], pole[1])
            except Exceptions.WrongMoveException:
                print("Player 2 incorrect move")
                player2.get_last_clicked().back_last_color()
            if move:
                if move == 2:
                    player2.points += 1
                if player2.get_last_clicked().check_if_have_clash() and move == 2:
                    player2.get_last_clicked().haveMC = True
                    main.haveMoreClashes = True
                else:
                    t = t + 1
                    main.turn += 1
                    player2.get_last_clicked().haveMC = False
                    player2.get_last_clicked().back_last_color()
                    main.haveMoreClashes = False
                return
            elif not main.haveMoreClashes:
                player2.get_last_clicked().haveMC = False
                player2.get_last_clicked().back_last_color()
                main.haveMoreClashes = False
        if not main.haveMoreClashes:
            try:
                p = player2.check_if_pawn_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 25)
            except Exceptions.WrongTeamPickException:
                print("Niepoprawne klikniecie w plansze")
            else:
                p.change_color((60, 60, 60))


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed()


def init_game():
    print("Init Game")
    restart_text.make_clickable(init_game)
    main.turn = 0
    main.board = Board.Board(8, 200, 100, 50)
    pygame.display.set_caption("Warcaby")
    logo = pygame.image.load("UI/img/icon.png")
    pygame.display.set_icon(logo)
    main.player1 = Player.Player(0, main.board)
    main.player2 = Player.Player(1, main.board)
    main.player1.set_enemy(main.player2)
    main.player2.set_enemy(main.player1)
    main.text1 = Text.Text(100, 100)
    main.text2 = Text.Text(100, 450)
    main.playable = True
    main.haveMoreClashes = False


def game_progress():
    #print("Progress ", player2.points, " - ", player1.points)
    if player2.points >= Player.Player.win_points or player1.points >= Player.Player.win_points:
        #InitGame()
        main.playable = False


def draw_stats():
    restart_text.write(screen, "Restart")
    turn_text.write(screen, "Tura numer " + str(main.turn))
    if main.turn % 2:
        info_text.write(screen, "Ruch czarnych pionkow")
        text1.write(screen, str(player1.points))
        text2.write(screen, str(player2.points))# + " <-")
    else:
        info_text.write(screen, "Ruch bialych pionkow")
        text1.write(screen, str(player1.points))# + " <-")
        text2.write(screen, str(player2.points))


def update(screen):
    events()
    game_progress()

    pygame.display.flip()
    screen.fill((0, 0, 0))


    if playable:
        board.draw(screen)
        player1.draw_pawns(screen)
        player2.draw_pawns(screen)
        draw_stats()
    else:
        if main.player1.points >= Player.Player.win_points:
            end_text.write(screen, "Zwyciezyl bialy")
        else:
            end_text.write(screen, "Zwyciezyl czarny")


def start():
    pygame.init()
    size = width, height = 800, 600
    main.screen = pygame.display.set_mode(size)
    init_game()

    while 1:
        update(screen)
        #pygame.transform.smoothscale(screen, (400, 300))



start()

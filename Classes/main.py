import pygame as pg
from game_controller import GameController


def main():
    pg.init()
    # initializes the game controller
    game_controller = GameController()

    # calls the menu from game controller class
    game_controller.main_menu()


if __name__ == "__main__":
    main()

import pygame
from player_controller import Player
from button import Button
from ball import Ball
from obstacle_manager import ObstacleManager


class GameController:
    def __init__(self):  #handles initialization of all variables here
        pygame.init()
        self.screen = pygame.display.set_mode((750, 900))
        self.player = Player(self.screen, 'Assets/Player/Player.png', 50, 15)
        self.obstacle_manager = ObstacleManager(self.screen)
        self.score = 0
        self.ball = Ball(self.screen, self.player, self.score, "ball.png", 25, 25, self.obstacle_manager,
                         game_controller=self)
        self.initial_launch = True
        self.reset_game()

    def get_font(self, size):
        return pygame.font.Font("Assets/Fonts/QuickSand.ttf", size)

    def main_menu(self):
        # shows the MAIN MENU text
        menu_text = self.get_font(100).render("MAIN MENU", True, (182, 143, 64))
        menu_text_rect = menu_text.get_rect(midtop=(self.screen.get_width() // 2, 100))

        while True:
            self.screen.fill((0, 0, 0))

            menu_mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(menu_text, menu_text_rect)

            play_button = Button(image=pygame.image.load("Assets/UI/Pause.png"),
                                 pos=(self.screen.get_width() // 2, 250),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")
            quit_button = Button(image=pygame.image.load("Assets/UI/Exit.png"), pos=(self.screen.get_width() // 2, 550),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")

            for button in [play_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        self.game_loop()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()

            pygame.display.update()

    def reset_game(self):
        # Reset game state
        self.player.reset()  # Reset player state
        self.obstacle_manager.reset()  # Reset obstacle manager state
        self.score = 0  # Reset score

    def return_to_main_menu(self):
        self.reset_game()
        self.main_menu()

    def game_loop(self):  # main game loop
        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        if paused:
                            self.pause_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.initial_launch:
                        self.ball.launch()
                        self.initial_launch = False

            if not paused:
                self.screen.fill((0, 0, 0))
                self.player.move()
                self.screen.blit(self.player.image, self.player.rect)
                self.ball.update()
                self.screen.blit(self.ball.image, self.ball.rect)
                self.obstacle_manager.update()  # Update obstacle positions
                self.obstacle_manager.draw()  # Draw obstacles

                # Display score on the screen
                score_text = self.get_font(36).render("Score: " + str(self.ball.score), True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))

                if self.obstacle_manager.all_destroyed():
                    self.level_complete()  # Display level complete message

                pygame.display.update()

    def level_complete(self):
        # Display the "Level Complete" message
        level_complete_text = self.get_font(72).render("Level Complete!", True, (255, 255, 255))
        level_complete_rect = level_complete_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(level_complete_text, level_complete_rect)
        pygame.display.update()
        pygame.time.delay(5000)  #  Delays message before sending player back to menu
        pygame.quit()

    def pause_game(self):  #pause logic here
        print("Pausing Game")
        pass

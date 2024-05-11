import pygame as pg


class Ball(pg.sprite.Sprite):
    def __init__(self, screen, player, score, image_path, width, height, obstacle_manager, game_controller):
        super(Ball, self).__init__()
        self.game_controller = game_controller
        self.screen = screen
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() * 0.75)
        self.velocity = pg.Vector2(0, 0)  # Initial velocity of the ball
        self.speed = 3.12  # adjust speed of ball
        self.score = score
        self.player = player
        self.game_over_flag = False  # Flag to track game over state
        self.obstacle_manager = obstacle_manager

        # Font for score
        self.font = pg.font.Font(None, 36)

    def reset(self):
        # Reset ball
        self.rect.center = (self.screen.get_width() / 2, self.screen.get_height() * 0.75)
        self.velocity = pg.Vector2(0, 0)
        self.score = 0
        self.game_over_flag = False

    def update(self):
        if not self.game_over_flag:  # Only update if the game is not over
            self.rect.move_ip(self.velocity)  # Update the position of the ball

            # Bounce off the top and sides of the screen
            if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
                self.velocity.y *= -1
            if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
                self.velocity.x *= -1

            # Check if the ball has hit the floor
            if self.rect.bottom >= self.screen.get_height():
                # Keep the ball at the bottom of the screen
                self.rect.bottom = self.screen.get_height()
                # Stop the ball by setting its velocity to zero
                self.velocity = pg.Vector2(0, 0)
                if not self.game_over_flag:  # Check if the game over flag is not set
                    self.game_over()

            # Checks any collision with the paddle
            if self.rect.colliderect(self.player.rect):
                # Calculates the angle of reflection
                collision_offset = self.rect.centerx - self.player.rect.centerx
                reflection_angle = collision_offset / (self.player.rect.width / 2)
                self.velocity = pg.Vector2(reflection_angle * self.speed, -self.speed)

            # Checks any collision with obstacles
            for i, obstacle_rect in enumerate(self.obstacle_manager.obstacle_rects):
                if self.rect.colliderect(obstacle_rect):
                    self.score += 100
                    # Remove the obstacle at index i from both lists
                    del self.obstacle_manager.obstacle_imgs[i]
                    del self.obstacle_manager.obstacle_rects[i]
                    break  # Exit the loop after removing the obstacle

    def launch(self):
        # Launch the ball straight up
        self.velocity = pg.Vector2(0, -self.speed)

    def game_over(self):  # Handles the logic for when the player loses GAMEOVER!
        self.game_over_flag = True

        # Display the final score
        score_text = self.font.render("Score: " + str(self.score), True, pg.Color('white'))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 50))
        self.screen.blit(score_text, score_rect)

        # Display "GAME OVER" text
        game_over_text = self.font.render("GAME OVER", True, pg.Color('white'))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        pg.display.update()

        # Delay before exiting the game
        pg.time.delay(3000)
        self.game_controller.return_to_main_menu()


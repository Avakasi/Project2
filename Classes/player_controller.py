import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, screen, image_path, width, height):  #initialize of variables
        pg.sprite.Sprite.__init__(self)
        original_image = pg.image.load('Assets/Player/Player.png')
        self.image = pg.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() * 0.85)
        self.speed = 3.1  # Adjust the speed of paddle/player
        self.initial_x = self.rect.x
        self.initial_y = self.rect.y

    def move(self):
        current_pos = self.rect.topleft
        keys = pg.key.get_pressed()

        # Adjusts the paddle position based on the keys
        if keys[pg.K_LEFT]:
            current_pos = (current_pos[0] - self.speed, current_pos[1])
        if keys[pg.K_RIGHT]:
            current_pos = (current_pos[0] + self.speed, current_pos[1])

        # Keeps the player on the screen
        if current_pos[0] < 0:
            current_pos = (0, current_pos[1])
        elif current_pos[0] + self.rect.width > pg.display.get_surface().get_width():
            current_pos = (pg.display.get_surface().get_width() - self.rect.width, current_pos[1])

        self.rect.topleft = current_pos

    def reset(self):
        # Reset player
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y

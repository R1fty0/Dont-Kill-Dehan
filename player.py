import pygame

class Collider:
    def __init__(self, x, y, width, height):
        """ Creates a collider anchored to the provided x and y coordinates. """
        self.collider = pygame.Rect(x, y, width, height)  # collider
        self.x = x  # current x-position of collider
        self.y = y  # current y-position of collider

    def is_colliding(self, game_object) -> bool:
        """ Returns true if this collider is colliding with a given collider.  """
        if self.collider.colliderect(game_object):
            return True
        else:
            return False







class Player(Collider):
    def __init__(self, speed, image, jump_key, x, y, width, height):
        Collider.__init__(self, x, y, width, height)
        self.speed = speed  # player speed
        self.image = image  # player image
        self.jump_key = jump_key  # player jump bind
        self.vel_x = 0  # player velocity on x-axis
        self.vel_y = 0  # player velocity on y-axis
        self.is_grounded = True # whether the player is grounded or not.

    def jumping(self):
        """ Makes the player jump upon key pressed. """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[self.jump_key]:
            self.vel_y -= self.speed

    def gravity(self):
        """ Simulates gravity effects on the player when they are in the air. """
        if not self.is_grounded:
            self.vel_y += self.speed * 0.1

    def update(self):
        self.jumping()
        self.gravity()


import pygame
from constants import COLS, ROWS

class Player:
    def __init__(self, row, col, tile_size):
        self.row = row
        self.col = col
        self.pos = row, col
        self.x = col * tile_size
        self.y = row * tile_size
        self.tile_size = tile_size
        self.image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.move_progress = 0
        self.target_x = self.x
        self.target_y = self.y
        self.is_moving = False

    def move(self, direction):
        if self.is_moving:
            return
        if direction == "UP" and self.row > 0:
            self.target_y = self.y - self.tile_size
            self.row -= 1
        elif direction == "DOWN" and self.row < ROWS - 1:
            self.target_y = self.y + self.tile_size
            self.row += 1
        elif direction == "LEFT" and self.col > 0:
            self.target_x = self.x - self.tile_size
            self.col -= 1
        elif direction == "RIGHT" and self.col < COLS - 1:
            self.target_x = self.x + self.tile_size
            self.col += 1
        self.is_moving = True  

    def update(self):
        if self.is_moving:
            speed = 10
            if abs(self.x - self.target_x) > speed:
                self.x += speed if self.x < self.target_x else -speed
            else:
                self.x = self.target_x
            if abs(self.y - self.target_y) > speed:
                self.y += speed if self.y < self.target_y else -speed
            else:
                self.y = self.target_y
            if self.x == self.target_x and self.y == self.target_y:
                self.is_moving = False
                
    # Kutuya çarptı mı kontorl et
    def collision(self, direction, boxes):
        for box in boxes:
            if direction == "UP" and self.row - 1 == box.row and self.col == box.col:
                return box
            elif direction == "DOWN" and self.row + 1 == box.row and self.col == box.col:
                return box 
            elif direction == "LEFT" and self.row == box.row and self.col - 1 == box.col:
                return box
            elif direction == "RIGHT" and self.row == box.row and self.col + 1 == box.col:
                return box
        return None

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def clone(self):
        new_player = Player(self.row, self.col, self.tile_size)
        new_player.x = self.x
        new_player.y = self.y
        new_player.target_x = self.target_x
        new_player.target_y = self.target_y
        new_player.is_moving = self.is_moving
        return new_player

    def simulate_move(self, direction):
        if direction == "UP" and self.row > 0:
            self.row -= 1
        elif direction == "DOWN" and self.row < ROWS - 1:
            self.row += 1
        elif direction == "LEFT" and self.col > 0:
            self.col -= 1
        elif direction == "RIGHT" and self.col < COLS - 1:
            self.col += 1
        self.x = self.col * self.tile_size
        self.y = self.row * self.tile_size 
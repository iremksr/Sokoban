import pygame
import random
from box import Box

class GameMap:
    def __init__(self, rows, cols, tile_size):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.map = [
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '@', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.']
        ]
        self.targets = []
        self.boxes = []

    # Hedefleri yerlerini random bir şekilde belirle
    def generate_targets(self, num_boxes):
        empty_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.map[r][c] == "."]
        self.targets = random.sample(empty_positions, num_boxes)
        for row, col in self.targets:
            self.map[row][col] = "+" 
        return self.targets
    
    # Kutuların yerlerini random bir şekilde belirle 
    def generate_boxes(self, num_boxes, targets):
        # Hedeflerle aynı yerde olmasın
        empty_positions = [(r, c) for r in range(1, self.rows - 1) for c in range(1, self.cols - 1)
                          if self.map[r][c] == '.' and (r, c) not in targets]
        if len(empty_positions) < num_boxes:
            raise ValueError("Yeterli alan yok!")
        box_positions = random.sample(empty_positions, num_boxes)
        self.boxes = []
        for row, col in box_positions:
            self.boxes.append(Box(row, col, self.tile_size))
            self.map[row][col] = "#"
        return self.boxes

    # Haritayı çiz
    def draw_map(self, window):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                x = col * self.tile_size
                y = row * self.tile_size
                pygame.draw.rect(window, (216, 191, 216), (x, y, self.tile_size, self.tile_size))

    # Hedefleri çiz
    def draw_targets(self, window):
        for row, col in self.targets:
            x = col * self.tile_size
            y = row * self.tile_size
            pygame.draw.rect(window, (102, 78, 123), (x, y, self.tile_size, self.tile_size), 10)

    # Oyun ızgarasını çiz
    def draw_grid(self, window, outline_color, outline_thickness):
        for row in range(1, self.rows):
            y = row * self.tile_size
            pygame.draw.line(window, outline_color, (0, y), (self.cols * self.tile_size, y), outline_thickness)
        for col in range(1, self.cols):
            x = col * self.tile_size
            pygame.draw.line(window, outline_color, (x, 0), (x, self.rows * self.tile_size), outline_thickness)
        pygame.draw.rect(window, outline_color, (0, 0, self.cols * self.tile_size, self.rows * self.tile_size), outline_thickness)

    # Oyun bitti mi kontolü (tüm kutular hedeflerde ise bitti)
    def is_game_end(self):
        for box in self.boxes:
            if not box.target_reached:
                return False
        return True 
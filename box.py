import pygame
from constants import ROWS, COLS

class Box:
    def __init__(self, row, col, tile_size):
        self.row = row
        self.col = col
        self.position = (row, col)
        self.x = col * tile_size
        self.y = row * tile_size
        self.tile_size = tile_size
        self.target_reached = False
        self.target_x = self.x
        self.target_y = self.y
        self.is_moving = False
        self.image = pygame.image.load("box.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.move_progress = 0

    def get_position(self):
        return self.position
    
    # Kutu hedefte mi diye kontrol et
    def check_target(self, targets):
        for target in targets:
            if (self.row, self.col) == target:
                self.target_reached = True

    # Kutunun diğer kutularla temas halinde mi  
    def collision(self, direction, boxes):
        for box in boxes:
            if box == self:
                continue
            if direction == "UP" and self.row - 1 == box.row and self.col == box.col:
                return True
            if direction == "DOWN" and self.row + 1 == box.row and self.col == box.col:
                return True
            if direction == "LEFT" and self.col - 1 == box.col and self.row == box.row:
                return True
            if direction == "RIGHT" and self.col + 1 == box.col and self.row == box.row:
                return True
        return False

    # Kutu hareket ettirilebilir mi
    def can_push(self, direction, boxes):
        new_row, new_col = self.row, self.col
        if direction == "UP":
            new_row -= 1
        elif direction == "DOWN":
            new_row += 1
        elif direction == "LEFT":
            new_col -= 1
        elif direction == "RIGHT":
            new_col += 1
        # Haritanın sınırları ile kontrol sağla
        if new_row < 0 or new_row >= ROWS or new_col < 0 or new_col >= COLS:
            return False
        # Dİğer kutularla collisionu var mı diye kontol sağla
        for box in boxes:
            if box != self and box.row == new_row and box.col == new_col:
                return False
        return True

    def move(self, direction, boxes, targets):
        if self.target_reached:
            return
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
 
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    # Kutunun kopyasını oluştur(greedy yaklaşımda bu kopya üzerinden hareket edeceğiz)
    def clone(self):
        new_box = Box(self.row, self.col, self.tile_size)
        new_box.x = self.x
        new_box.y = self.y
        new_box.target_x = self.target_x
        new_box.target_y = self.target_y
        new_box.is_moving = self.is_moving
        new_box.target_reached = self.target_reached
        return new_box
    
    # Hareket simulasyonu yap(clone üzerinden yapılan işlemlerde kullanılacak)
    def simulate_move(self, direction):
        if self.target_reached:
            return
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
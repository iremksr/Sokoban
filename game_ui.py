import pygame
import sys

class GameUI:
    def __init__(self, screen_width, screen_height, tile_size, outline_color, outline_thickness):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Sokoban")

    def draw(self, game_map, player, boxes):
        self.window.fill((255, 255, 255))
        game_map.draw_map(self.window)
        game_map.draw_grid(self.window, self.outline_color, self.outline_thickness)
        player.draw(self.window)
        for box in boxes:
            box.draw(self.window)
        game_map.draw_targets(self.window)
        pygame.display.update()

    def draw_success_screen(self):
        # Renk paleti
        background_color = (216, 191, 216)  
        box_color = (186, 150, 186)         
        text_color = (255, 255, 255)        
        button_color = (186, 150, 186)      
        button_text_color = (255, 255, 255) 

        # Yazı tipi ve fontlar
        title_font = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
        button_font = pygame.font.SysFont("Comic Sans MS", 32, bold=True)

        self.window.fill(background_color)

        # Başlık kutusu
        title_text = title_font.render("Görev Tamamlandı", True, text_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        pygame.draw.rect(self.window, box_color, (title_rect.x - 20, title_rect.y - 10,
                                         title_rect.width + 40, title_rect.height + 20), border_radius=15)
        self.window.blit(title_text, title_rect)

        # Buton kutusu
        button_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2, 300, 60)
        pygame.draw.rect(self.window, button_color, button_rect, border_radius=20)
        button_text = button_font.render("Yeni Oyun", True, button_text_color)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.window.blit(button_text, button_text_rect)

        pygame.display.update()
        return button_rect

    def choose_method(self):
        # Fontlar
        font_title = pygame.font.SysFont("Segoe UI", 36, bold=True)
        font_option = pygame.font.SysFont("Segoe UI", 28)

        # Renk paleti
        background_color = (216, 191, 216)      
        text_color = (255, 255, 255)              
        box_color = (186, 150, 186)             
        border_color = (200, 180, 210)         

        while True:
            self.window.fill(background_color)

            # Başlık kutusu
            title_box = pygame.Rect(self.screen_width // 2 - 220, self.screen_height // 4 - 50, 440, 70)
            pygame.draw.rect(self.window, box_color, title_box, border_radius=16)
            pygame.draw.rect(self.window, border_color, title_box, 3, border_radius=16)

            title_text = font_title.render("Çözüm Yöntemini Seçin", True, text_color)
            title_text_rect = title_text.get_rect(center=title_box.center)
            self.window.blit(title_text, title_text_rect)

            # Kutu boyutları
            box_width = 400
            box_height = 60
            box_margin = 20

            # Greedy kutusu
            greedy_rect = pygame.Rect(
                (self.screen_width - box_width) // 2,
                self.screen_height // 2 - box_height - box_margin,
                box_width,
                box_height
            )
            pygame.draw.rect(self.window, box_color, greedy_rect, border_radius=15)
            pygame.draw.rect(self.window, border_color, greedy_rect, 3, border_radius=15)

            greedy_text = font_option.render("1. Greedy Best-First Search", True, text_color)
            greedy_text_rect = greedy_text.get_rect(center=greedy_rect.center)
            self.window.blit(greedy_text, greedy_text_rect)

            # A* kutusu
            astar_rect = pygame.Rect(
                (self.screen_width - box_width) // 2,
                self.screen_height // 2 + box_margin,
                box_width,
                box_height
            )
            pygame.draw.rect(self.window, box_color, astar_rect, border_radius=15)
            pygame.draw.rect(self.window, border_color, astar_rect, 3, border_radius=15)

            astar_text = font_option.render("2. A* Search", True, text_color)
            astar_text_rect = astar_text.get_rect(center=astar_rect.center)
            self.window.blit(astar_text, astar_text_rect)

            # BFS kutusu 
            bfs_rect = pygame.Rect(
                (self.screen_width - box_width) // 2,
                self.screen_height // 2 + box_margin * 2 + box_height,
                box_width,
                box_height
            )
            pygame.draw.rect(self.window, box_color, bfs_rect, border_radius=15)
            pygame.draw.rect(self.window, border_color, bfs_rect, 3, border_radius=15)

            bfs_text = font_option.render("3. BFS (Breadth-First Search)", True, text_color)
            bfs_text_rect = bfs_text.get_rect(center=bfs_rect.center)
            self.window.blit(bfs_text, bfs_text_rect)

            pygame.display.update()

            # Olay kontrolü
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "greedy"
                    elif event.key == pygame.K_2:
                        return "astar"
                    elif event.key == pygame.K_3:
                        return "bfs" 